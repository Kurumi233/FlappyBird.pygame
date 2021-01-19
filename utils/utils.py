import os
import yaml


DEFAULT_CONFIG_PATH = 'utils/config.yaml'
USER_CONFIG_PATH = 'utils/user.yaml'


def load_config():
    config_path = DEFAULT_CONFIG_PATH
    if(os.path.exists(USER_CONFIG_PATH)):
        config_path = USER_CONFIG_PATH

    with open(config_path, 'r', encoding='utf-8')as f:
        args = yaml.load(f.read(), Loader=yaml.FullLoader)

    return args