import os
from configparser import ConfigParser
CONFIG_PATH =  os.path.join(os.path.dirname(__file__),"config.ini")

def get_config() -> ConfigParser:
    config = ConfigParser()
    parent_folder = os.path.dirname(CONFIG_PATH)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
        return config
    with open(CONFIG_PATH,"r") as f:
        config.read_file(f)
    return config

def write_config(config_parser):
    with open(CONFIG_PATH,"w") as f:
        config_parser.write(f)

def set_open_path(path):
    config_parser = get_config()
    config_parser.set("paths","open_path",path)
    write_config(config_parser)


def set_save_path(path):
    config_parser = get_config()
    config_parser.set("paths","save_path",path)
    write_config(config_parser)

def get_open_path():
    config_parser = get_config()
    if config_parser.has_option("paths","open_path"):
        path = config_parser.get("paths","open_path")
        if path is not None:
            return path
    return ""

def get_save_path():
    config_parser = get_config()
    if config_parser.has_option("paths","save_path"):
        path = config_parser.get("paths","save_path")
        if path is not None:
            return path
    return ""
def get_file_path():

    config_path = CONFIG_PATH
    if config_path is None:
        return ""
    config = ConfigParser()
    if not os.path.exists(str(CONFIG_PATH)):
        return ""
    config.read(CONFIG_PATH)
    if config.has_section("paths"):
        if config.has_option("paths","file_path"):
            return config.get("paths", "file_path")
    return ""