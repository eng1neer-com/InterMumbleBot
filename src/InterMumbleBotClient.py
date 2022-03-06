from pymumble_py3 import Mumble
from pymumble_py3.constants import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, PYMUMBLE_CLBK_USERCREATED, \
    PYMUMBLE_CLBK_USERREMOVED, PYMUMBLE_CLBK_CONNECTED, PYMUMBLE_CONN_STATE_CONNECTED
from pymumble_py3.errors import UnknownChannelError
from pymumble_py3.mumble_pb2 import TextMessage as Message
from Constants import *
import time


def send_multi_line_msg(send_function, messages):
    # use html command "<br>" between lines to send multiline messages as one command to decrease delay
    send_function("<br>".join(str(x) for x in messages))


def broadcast_userchange(users_left, users_joined, channels):
    broadcast_msg = [IMB_CHAT_BROADCAST_UPDATE]
    if users_left:
        broadcast_msg.append(IMB_CHAT_BROADCAST_USR_LEFT + " " + ",".join(str(x) for x in users_left))
    if users_joined:
        broadcast_msg.append(IMB_CHAT_BROADCAST_USR_JOINED + " " + ",".join(str(x) for x in users_joined))
    if len(broadcast_msg) > 1:
        for channel in channels:
            if channels[channel].get_users():
                send_multi_line_msg(channels[channel].send_text_message, broadcast_msg)
        return broadcast_msg
    else:
        return None


def get_real_users(users, bot_name):
    real_users = []
    for user in users:
        username = users[user]['name']
        if not username.lower().__contains__('bot') and not username == bot_name:
            real_users.append(username)
    return real_users


def update_channel_name(connected, users, bot_name):
    if connected == PYMUMBLE_CONN_STATE_CONNECTED:
        real_users = get_real_users(users, bot_name)
        channel_name = IMB_NORMAL_CH_NAME_PREFIX + " " + str(len(real_users)) + " " + IMB_NORMAL_CH_NAME_POSTFIX
    else:
        channel_name = IMB_NO_CONN_CH_NAME
    return channel_name


def channel_exists(channels, own_channel_id):
    exists = True
    try:
        channels[own_channel_id]
    except KeyError:
        exists = False
    return exists


def handle_message(message, remote_users, my_channel, users, channels, public_reply):
    output = []
    if message.channel_id:  # request from channel
        send_function = my_channel.send_text_message  # normal operation: send answer to channel
    else:  # request from user via private message
        if not public_reply:
            send_function = users[message.actor].send_text_message  # send answer to user directly
        else:
            origin_channel = users[message.actor]['channel_id']
            send_function = channels[origin_channel].send_text_message  # send answer to channel of user
    message = message.message.strip()

    if message == IMB_CMD_USERS:
        if len(remote_users) > 0:
            output.append(IMB_CHAT_USERS_HEADING)
            for user in remote_users:
                output.append(user)
        else:
            output.append(IMB_CHAT_NO_USERS_FEEDBACK)
    elif message == IMB_CMD_HELP:
        output.append(IMB_CHAT_HELP_MSG_PREFIX + " " + IMB_CMD_USERS + " " + IMB_CHAT_HELP_MSG_POSTFIX)

    send_multi_line_msg(send_function, output)


def recreate_channel(channels, channel_name):
    ch_exists = True
    try:
        channel = channels.find_by_name(channel_name)  # check if channel already exists
        channel.move_in(session=None)
    except UnknownChannelError:
        ch_exists = False

    if not ch_exists:
        channels.new_channel(0, channel_name, True)  # create temporary channel
        time.sleep(1)
    try:
        own_channel_id = channels.find_by_name(channel_name)['channel_id']
    except UnknownChannelError:
        own_channel_id = 0
    return own_channel_id


class InterMumbleBotClient:

    def __init__(self, bot_num, settings):
        self.bot_name = settings.bot_name
        self.bot_num = bot_num
        self.message = Message()
        self.new_message = False  # user sent message on local server
        self.user_changed = False  # user joined/left on local server
        self.channel_name = IMB_INITIAL_CH_NAME
        self.remote_user_list = {}
        self.fresh_connect = False
        self.broadcast_changes = settings.broadcast_changes
        self.public_reply = settings.public_reply
        self.own_channel_id = -1  # ID of created channel
        if bot_num == 1:
            hostname = settings.hostname1
            port = settings.port1
            pw = settings.pw1
        elif bot_num == 2:
            hostname = settings.hostname2
            port = settings.port2
            pw = settings.pw2
        else:
            raise Exception(IBM_EXCEPT_INVALID_BOT_NR)

        self.mumble = Mumble(hostname, settings.bot_name, port=port, password=pw, certfile=settings.bot_certificate,
                             keyfile=None, reconnect=True, tokens=[], stereo=False,
                             debug=False)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, self.msg_received)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_USERCREATED, self.user_added)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_USERREMOVED, self.user_removed)
        self.mumble.callbacks.set_callback(PYMUMBLE_CLBK_CONNECTED, self.connected)

    def start(self):
        self.mumble.start()
        self.mumble.is_ready()
        if self.mumble.connected == PYMUMBLE_CONN_STATE_CONNECTED:
            self.mumble.users.myself.register()

    def stop(self):
        self.mumble.stop()

    def msg_received(self, data):
        self.new_message = True
        self.message = data

    def user_added(self, *_):
        self.user_changed = True

    def user_removed(self, *_):
        self.user_changed = True

    def connected(self):
        self.fresh_connect = True

    def loop(self, remote_mumble):
        if self.mumble.connected == PYMUMBLE_CONN_STATE_CONNECTED:
            if self.fresh_connect:
                self.fresh_connect = False
                self.remote_user_list = get_real_users(remote_mumble.users, self.bot_name)
                self.channel_name = update_channel_name(remote_mumble.connected, remote_mumble.users, self.bot_name)
                self.own_channel_id = recreate_channel(self.mumble.channels, self.channel_name)
            else:
                # handle user update
                remote_user_list = get_real_users(remote_mumble.users, self.bot_name)
                if remote_user_list != self.remote_user_list:
                    users_left = list(set(self.remote_user_list) - set(remote_user_list))
                    users_joined = list(set(remote_user_list) - set(self.remote_user_list))
                    self.remote_user_list = remote_user_list  # store users of other server in case list is requested
                    if self.broadcast_changes and (users_left or users_joined):
                        broadcast_userchange(users_left, users_joined, self.mumble.channels)

                # handle channel update
                channel_name = update_channel_name(remote_mumble.connected, remote_mumble.users, self.bot_name)
                if channel_name != self.channel_name or not channel_exists(self.mumble.channels, self.own_channel_id):
                    self.channel_name = channel_name
                    self.own_channel_id = recreate_channel(self.mumble.channels, self.channel_name)
                    time.sleep(1)

                # handle commands received via chat
                if self.new_message:
                    self.new_message = False
                    handle_message(self.message, self.remote_user_list, self.mumble.my_channel(),
                                   self.mumble.users, self.mumble.channels, self.public_reply)
