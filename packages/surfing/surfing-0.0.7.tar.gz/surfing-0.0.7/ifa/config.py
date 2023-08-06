from .util import Singleton
import platform
import json

CURRENT_PLATFORM = platform.system()
DEFAULT_CONFIG_PATH = '/shared/etc/ifa/config.json'

class MessageSenderSetting(object):

    def __init__(self, data_json):
        assert 'corp_id' in data_json, 'could not find corp_id in config file'
        assert 'app_id' in data_json, 'could not find app_id in config file'
        assert 'app_secret' in data_json, 'could not find add_secret in config file'

        self.corp_id = data_json['corp_id']
        self.app_id = data_json['app_id']
        self.app_secret = data_json['app_secret']

class Configurator(metaclass=Singleton):

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        with open(config_path) as f:
            self.config = json.load(f)

    def get_message_sender_setting(self):
        settings = MessageSenderSetting(self.config['wxwork_app'])
        return settings
