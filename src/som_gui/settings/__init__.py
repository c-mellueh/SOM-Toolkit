import os
from configparser import ConfigParser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")
PATHS_SECTION = "paths"
OPEN_PATH = "open_path"
SAVE_PATH = "save_path"
IFC_PATH = "ifc_path"
ISSUE_PATH = "issue_path"


def get_config() -> ConfigParser:
    config = ConfigParser()
    parent_folder = os.path.dirname(CONFIG_PATH)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
        return config
    if not os.path.exists(CONFIG_PATH):
        return config
    with open(CONFIG_PATH, "r") as f:
        config.read_file(f)
    return config


def get_path( path):
    section = PATHS_SECTION
    config_parser = get_config()
    if config_parser.has_option(section, path):
        path = config_parser.get(section, path)
        if path is not None:
            return path
    return ""


def set_path(path, value):
    section = PATHS_SECTION
    if isinstance(value, (list,set)):
        value = value[0]
    if os.path.isfile(value):
        value = os.path.dirname(value)
    config_parser = get_config()
    if not config_parser.has_section(section):
        config_parser.add_section(section)
    config_parser.set(section, path, value)
    write_config(config_parser)


def write_config(config_parser):
    with open(CONFIG_PATH, "w") as f:
        config_parser.write(f)


def get_open_path():
    return get_path( OPEN_PATH)


def set_open_path(path):
    set_path( SAVE_PATH, path)


def get_save_path():
    return get_path( SAVE_PATH)


def set_save_path(path):
    set_path( SAVE_PATH, path)


def get_ifc_path():
    return get_path( IFC_PATH)


def set_ifc_path(path):
    set_path( IFC_PATH, path)


def get_issue_path():
    return get_path( ISSUE_PATH)


def set_issue_path(path):
    set_path( ISSUE_PATH, path)
