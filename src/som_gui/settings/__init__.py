import os
from configparser import ConfigParser
CONFIG_PATH =  os.path.join(os.path.dirname(__file__),"config.ini")
PATHS_SECTION = "paths"
OPEN_PATH = "open_path"
SAVE_PATH = "save_path"

def get_config() -> ConfigParser:
    config = ConfigParser()
    parent_folder = os.path.dirname(CONFIG_PATH)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
        return config
    if not os.path.exists(CONFIG_PATH):
        return config
    with open(CONFIG_PATH,"r") as f:
        config.read_file(f)
    return config

def write_config(config_parser):
    with open(CONFIG_PATH,"w") as f:
        config_parser.write(f)

def set_open_path(path):
    config_parser = get_config()
    if not config_parser.has_section(PATHS_SECTION):
        config_parser.add_section(PATHS_SECTION)
    config_parser.set(PATHS_SECTION,OPEN_PATH,path)
    write_config(config_parser)


def set_save_path(path):
    config_parser = get_config()
    if not config_parser.has_section(PATHS_SECTION):
        config_parser.add_section(PATHS_SECTION)
    config_parser.set(PATHS_SECTION,SAVE_PATH,path)
    write_config(config_parser)

def get_open_path():
    config_parser = get_config()
    if config_parser.has_option(PATHS_SECTION,OPEN_PATH):
        path = config_parser.get(PATHS_SECTION,OPEN_PATH)
        if path is not None:
            return path
    return ""

def get_save_path():
    config_parser = get_config()
    if config_parser.has_option(PATHS_SECTION,SAVE_PATH):
        path = config_parser.get(PATHS_SECTION,SAVE_PATH)
        if path is not None:
            return path
    return ""