import time
import os
import threading

from pymumble_py3.constants import PYMUMBLE_CONN_STATE_CONNECTED

from InterMumbleBotClient import InterMumbleBotClient
from ConfigContainer import ConfigContainer


class InterMumbleBot:
    def __init__(self, settings, task_rate):
        self.task_rate = task_rate
        self.bot1 = InterMumbleBotClient(1, settings)
        self.bot2 = InterMumbleBotClient(2, settings)

        # use threads for the start routines to avoid waiting for one bot in case of long connection times
        self.t1 = threading.Thread(target=self.bot1.start)
        self.t2 = threading.Thread(target=self.bot2.start)
        self.t1.start()
        self.t2.start()

    def loop(self):
        while True:
            if not self.t1.is_alive() and self.bot1.mumble.connected == PYMUMBLE_CONN_STATE_CONNECTED:
                self.bot1.loop(self.bot2.mumble)
            if not self.t2.is_alive() and self.bot2.mumble.connected == PYMUMBLE_CONN_STATE_CONNECTED:
                self.bot2.loop(self.bot1.mumble)
            time.sleep(self.task_rate)


if __name__ == '__main__':
    config = ConfigContainer(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'settings.ini'))
    config.read_config()
    myInterMumbleBot = InterMumbleBot(config, 2)
    myInterMumbleBot.loop()



