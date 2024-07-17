from __future__ import annotations

import os
from configparser import ConfigParser

DIR_PATH = os.path.dirname(__file__)
LOG_CONFIG_PATH = os.path.join(DIR_PATH, "logging.conf")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")
PATHS_SECTION = "paths"
OPEN_PATH = "open_path"
SAVE_PATH = "save_path"
EXPORT_PATH = "export_path"
IFC_PATH = "ifc_path"
ISSUE_PATH = "issue_path"
SEPERATOR_SECTION = "seperator"
SEPERATOR_STATUS = "seperator_status"
SEPERATOR = "seperator"
GROUP_FOLDER = "group_folder_path"
ATTRIBUTE_IMPORT_SECTION = "attribute_import"
EXISTING_ATTRIBUTE_IMPORT = "existing"
REGEX_ATTRIBUTE_IMPORT = "regex"
RANGE_ATTRIBUTE_IMPORT = "range"
COLOR_ATTTRIBUTE_IMPORT = "color"
PATH_SEPERATOR = " ;"
IFC_MOD = "ifc_modification"
GROUP_PSET = "group_pset"
GROUP_ATTRIBUTE = "group_attribute"
CREATE_EMPTY = "create_empty"
PLUGINS = "plugins"


def _get_config() -> ConfigParser:
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


def _get_path(value: str) -> str | list | set:
    path = _get_string_setting(PATHS_SECTION, value)
    if not path:
        return ""
    if PATH_SEPERATOR in path:
        return path.split(PATH_SEPERATOR)
    return path


def _set_path(path, value: str | list | set) -> None:
    if isinstance(value, (list, set)):
        value = PATH_SEPERATOR.join(value)
    set_setting(PATHS_SECTION, path, value)


def _write_config(config_parser) -> None:
    with open(CONFIG_PATH, "w") as f:
        config_parser.write(f)


def _get_bool_setting(section: str, path: str) -> bool:
    config_parser = _get_config()
    if config_parser.has_option(section, path):
        path = config_parser.get(section, path)
        if path is not None:
            return eval(path)
    return False


def set_setting(section: str, path: str, value) -> None:
    config_parser = _get_config()
    if not config_parser.has_section(section):
        config_parser.add_section(section)
    config_parser.set(section, path, str(value))
    _write_config(config_parser)


def _get_string_setting(section: str, path: str, default="") -> str:
    config_parser = _get_config()
    if config_parser.has_option(section, path):
        path = config_parser.get(section, path)
        if path is not None:
            return path
    return default


def get_setting_attribute_import_existing() -> bool:
    return _get_bool_setting(ATTRIBUTE_IMPORT_SECTION, EXISTING_ATTRIBUTE_IMPORT)


def set_setting_attribute_import_existing(value: bool) -> None:
    set_setting(ATTRIBUTE_IMPORT_SECTION, EXISTING_ATTRIBUTE_IMPORT, value)


def get_setting_attribute_import_regex() -> bool:
    return _get_bool_setting(ATTRIBUTE_IMPORT_SECTION, REGEX_ATTRIBUTE_IMPORT)


def set_setting_attribute_import_regex(value: bool) -> None:
    set_setting(ATTRIBUTE_IMPORT_SECTION, REGEX_ATTRIBUTE_IMPORT, value)


def get_setting_attribute_import_range() -> bool:
    return _get_bool_setting(ATTRIBUTE_IMPORT_SECTION, RANGE_ATTRIBUTE_IMPORT)


def set_setting_attribute_import_range(value: bool) -> None:
    set_setting(ATTRIBUTE_IMPORT_SECTION, RANGE_ATTRIBUTE_IMPORT, value)


def get_setting_attribute_color() -> bool:
    return _get_bool_setting(ATTRIBUTE_IMPORT_SECTION, COLOR_ATTTRIBUTE_IMPORT)


def set_setting_attribute_color(value: bool) -> None:
    set_setting(ATTRIBUTE_IMPORT_SECTION, COLOR_ATTTRIBUTE_IMPORT, value)


def reset_save_path():
    path = get_save_path()
    if os.path.isfile(path):
        path = os.path.dirname(path)
    set_save_path(path)


def get_seperator_status() -> bool:
    return _get_bool_setting(SEPERATOR_SECTION, SEPERATOR_STATUS)


def set_seperator_status(value: bool) -> None:
    set_setting(SEPERATOR_SECTION, SEPERATOR_STATUS, value)


def get_seperator() -> str:
    return _get_string_setting(SEPERATOR_SECTION, SEPERATOR, ",")


def set_seperator(value: str) -> None:
    set_setting(SEPERATOR_SECTION, SEPERATOR, value)


def get_export_path() -> str:
    return _get_path(EXPORT_PATH)


def set_export_path(path) -> None:
    _set_path(EXPORT_PATH, path)


def get_open_path() -> str:
    return _get_path(OPEN_PATH)


def set_open_path(path) -> None:
    _set_path(OPEN_PATH, path)


def get_save_path() -> str:
    return _get_path(SAVE_PATH)


def set_save_path(path) -> None:
    _set_path(SAVE_PATH, path)


def get_ifc_path() -> str:
    return _get_path(IFC_PATH)


def set_ifc_path(path) -> None:
    _set_path(IFC_PATH, path)


def get_issue_path() -> str:
    return _get_path(ISSUE_PATH)


def set_issue_path(path) -> None:
    _set_path(ISSUE_PATH, path)


def set_group_create_empty_attributes(value: bool) -> None:
    set_setting(IFC_MOD, CREATE_EMPTY, value)


def get_group_create_empty_attributes() -> bool:
    return _get_bool_setting(IFC_MOD, CREATE_EMPTY)


def get_setting_plugin_activated(name: str) -> bool:
    config_parser = _get_config()
    if not config_parser.has_option(PLUGINS, name):
        set_setting(PLUGINS, name, True)
        return True
    return _get_bool_setting(PLUGINS, name)


def set_settings_plugin_activated(name: str, value: bool) -> None:
    set_setting(PLUGINS, name, value)
