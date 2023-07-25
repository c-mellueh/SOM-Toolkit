import os
from configparser import ConfigParser

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")
PATHS_SECTION = "paths"
OPEN_PATH = "open_path"
SAVE_PATH = "save_path"
IFC_PATH = "ifc_path"
ISSUE_PATH = "issue_path"
SEPERATOR_SECTION = "seperator"
SEPERATOR_STATUS = "seperator_status"
SEPERATOR = "seperator"


def reset_save_path():
    path = get_save_path()
    if os.path.isfile(path):
        path = os.path.dirname(path)
    set_save_path(path)


def get_seperator_status() -> bool:
    config_parser = get_config()
    if config_parser.has_option(SEPERATOR_SECTION, SEPERATOR_STATUS):
        value = config_parser.get(SEPERATOR_SECTION, SEPERATOR_STATUS)
        if value is not None:
            return eval(value)
    return True


def set_seperator_status(value: bool) -> None:
    config_parser = get_config()
    if not config_parser.has_section(SEPERATOR_SECTION):
        config_parser.add_section(SEPERATOR_SECTION)
    config_parser.set(SEPERATOR_SECTION, SEPERATOR_STATUS, str(value))
    write_config(config_parser)


def get_seperator() -> str:
    config_parser = get_config()
    if config_parser.has_option(SEPERATOR_SECTION, SEPERATOR):
        value = config_parser.get(SEPERATOR_SECTION, SEPERATOR)
        if value is not None:
            return value
    return ","


def set_seperator(value: str) -> None:
    config_parser = get_config()
    if not config_parser.has_section(SEPERATOR_SECTION):
        config_parser.add_section(SEPERATOR_SECTION)
    config_parser.set(SEPERATOR_SECTION, SEPERATOR, str(value))
    write_config(config_parser)


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


def get_path(path: str) -> str:
    section = PATHS_SECTION
    config_parser = get_config()
    if config_parser.has_option(section, path):
        path = config_parser.get(section, path)
        if path is not None:
            return path
    return ""


def set_path(path, value: str) -> None:
    section = PATHS_SECTION
    if isinstance(value, (list, set)):
        value = value[0]
    config_parser = get_config()
    if not config_parser.has_section(section):
        config_parser.add_section(section)
    config_parser.set(section, path, value)
    write_config(config_parser)


def write_config(config_parser) -> None:
    with open(CONFIG_PATH, "w") as f:
        config_parser.write(f)


def get_open_path() -> str:
    return get_path(OPEN_PATH)


def set_open_path(path) -> None:
    set_path(OPEN_PATH, path)


def get_save_path() -> str:
    return get_path(SAVE_PATH)


def set_save_path(path) -> None:
    set_path(SAVE_PATH, path)


def get_ifc_path() -> str:
    return get_path(IFC_PATH)


def set_ifc_path(path) -> None:
    set_path(IFC_PATH, path)


def get_issue_path() -> str:
    return get_path(ISSUE_PATH)


def set_issue_path(path) -> None:
    set_path(ISSUE_PATH, path)
