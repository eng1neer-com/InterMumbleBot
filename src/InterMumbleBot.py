from InterMumbleBotClient import InterMumbleBotClient
from ConfigContainer import ConfigContainer
import time
import os


class InterMumbleBot:
    def __init__(self, settings, task_rate):
        self.task_rate = task_rate
        self.bot1 = InterMumbleBotClient(1, settings)
        self.bot2 = InterMumbleBotClient(2, settings)
        self.bot1.start()
        self.bot2.start()

    def loop(self):
        while True:
            self.bot1.loop(self.bot2.mumble)
            self.bot2.loop(self.bot1.mumble)
            time.sleep(self.task_rate)


if __name__ == '__main__':
    config = ConfigContainer(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'settings.ini'))
    config.read_config()
    myInterMumbleBot = InterMumbleBot(config, 2)
    myInterMumbleBot.loop()



