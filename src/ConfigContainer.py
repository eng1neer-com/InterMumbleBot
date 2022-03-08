import os
from configparser import ConfigParser
from os.path import exists
from Constants import *


class ConfigError(Exception):
    pass


class ConfigContainer:
    def __init__(self, filename):
        self.bot_certificate = None
        self.pw2 = None
        self.pw1 = None
        self.port2 = None
        self.port1 = None
        self.hostname1 = None
        self.hostname2 = None
        self.bot_name = None
        self.public_reply = None
        self.broadcast_changes = None
        self.filename = filename

    def __check_filename(self):
        if not exists(self.filename):
            print(self.filename)
            raise ConfigError(CC_EXCEPT_NO_INI_FILE)

    def read_config(self):
        self.__check_filename()
        try:
            conf_parser = ConfigParser()
            conf_parser.read(self.filename)
            self.bot_name = conf_parser.get('bot-settings', 'bot-client-name')
            self.hostname1 = conf_parser.get('bot-settings', 'hostname_server1')
            self.hostname2 = conf_parser.get('bot-settings', 'hostname_server2')
            self.port1 = conf_parser.getint('bot-settings', 'port1')
            self.port2 = conf_parser.getint('bot-settings', 'port2')
            self.pw1 = conf_parser.get('bot-settings', 'pw1')
            self.pw2 = conf_parser.get('bot-settings', 'pw2')
            self.public_reply = conf_parser.getboolean('bot-settings', 'public_reply')
            self.broadcast_changes = conf_parser.getboolean('bot-settings', 'broadcast_changes')
            bot_cert_temp = conf_parser.get('bot-settings', 'certificate')
            if bot_cert_temp:
                self.bot_certificate = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', bot_cert_temp)
        except ValueError:
            raise ConfigError(CC_EXCEPT_INI_NOT_VALID)
        self.__check_config()

    def __check_config(self):
        if not self.bot_name or not self.hostname1 or not self.hostname2:
            raise ConfigError(CC_EXCEPT_EMPTY_HOST_OR_NAME)
        if self.port1 == 0 or self.port2 == 0:
            raise ConfigError(CC_EXCEPT_PORT_ZERO)


