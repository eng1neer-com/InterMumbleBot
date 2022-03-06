import unittest
import pytest
import mock
from pymumble_py3.constants import PYMUMBLE_CONN_STATE_CONNECTED, PYMUMBLE_CONN_STATE_NOT_CONNECTED
from ..src.Constants import *
from ..src.InterMumbleBotClient import get_real_users, update_channel_name, send_multi_line_msg

dummy = ""


def dummy_ret_func(arg):
    global dummy
    dummy = arg


class TestInterMumbleBotClient(unittest.TestCase):

    def test_get_real_users(self):
        bot_name = "SecretName"

        # all names containing 'bot' and the own bot name shall not be detected as real users
        users = {1: {'name': 'bot'},
                 2: {'name': 'myBotName'},
                 3: {'name': 'mybotName'},
                 4: {'name': 'Real_User'},
                 5: {'name': bot_name}
                 }
        real_users = get_real_users(users, bot_name)
        assert real_users == ["Real_User"]

    def test_update_channel_name(self):
        bot_name = "bot"
        users = {1: {'name': 'bot'},
                 2: {'name': 'myBotName'},
                 3: {'name': 'mybotName'},
                 4: {'name': 'Real_User'},
                 }
        ch_name = update_channel_name(PYMUMBLE_CONN_STATE_NOT_CONNECTED, users, bot_name)
        assert ch_name == IMB_NO_CONN_CH_NAME

        ch_name = update_channel_name(PYMUMBLE_CONN_STATE_CONNECTED, users, bot_name)
        assert ch_name == IMB_NORMAL_CH_NAME_PREFIX + " 1 " + IMB_NORMAL_CH_NAME_POSTFIX

    def test_send_multi_line_msg(self):
        global dummy
        msgs = ["line 1", "line2", "line3"]
        send_multi_line_msg(dummy_ret_func, msgs)
        assert dummy == "<br>".join(str(x) for x in msgs)
