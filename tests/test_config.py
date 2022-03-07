import pytest
import unittest
import mock
from src.ConfigContainer import ConfigContainer, ConfigError
from configparser import ConfigParser
from src.Constants import *


class TestConfigContainer(unittest.TestCase):
    def setup_module(self):
        pass

    def teardown_module(self):
        pass

    def test_config_container_invalid_name(self):
        with pytest.raises(ConfigError) as e:
            ConfigContainer('invalidName.ini')
        assert str(e.value) == CC_EXCEPT_NO_INI_FILE

    def test_config_empty_strings(self):
        with mock.patch.object(ConfigParser, 'get', return_value=''), \
                mock.patch.object(ConfigParser, 'getint', return_value=42), \
                mock.patch.object(ConfigParser, 'getboolean', return_value=False):
            with pytest.raises(ConfigError) as e:
                ConfigContainer('settings.ini')
            assert str(e.value) == CC_EXCEPT_EMPTY_HOST_OR_NAME

    def test_config_int_zeros(self):
        with mock.patch.object(ConfigParser, 'get', return_value='foo'), \
                mock.patch.object(ConfigParser, 'getint', return_value=0), \
                mock.patch.object(ConfigParser, 'getboolean', return_value=False):
            with pytest.raises(ConfigError) as e:
                ConfigContainer('settings.ini')
            assert str(e.value) == CC_EXCEPT_PORT_ZERO
