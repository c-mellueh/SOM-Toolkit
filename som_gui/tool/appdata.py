from __future__ import annotations
import som_gui.core.tool
from som_gui.module.settings.paths import *
import som_gui
from configparser import ConfigParser
import os
import appdirs
from som_gui import tool


class Appdata(som_gui.core.tool.Appdata):

    @classmethod
    def get_export_path(cls, ) -> str:
        return cls.get_path(EXPORT_PATH)

    @classmethod
    def set_export_path(cls, path) -> None:
        cls.set_path(EXPORT_PATH, path)

    @classmethod
    def get_seperator(cls) -> str:
        return cls.get_string_setting(SEPERATOR_SECTION, SEPERATOR, ",")

    @classmethod
    def set_seperator_status(cls, value: bool) -> None:
        cls.set_setting(SEPERATOR_SECTION, SEPERATOR_STATUS, value)

    @classmethod
    def set_seperator(cls, value: str) -> None:
        cls.set_setting(SEPERATOR_SECTION, SEPERATOR, value)

    @classmethod
    def get_seperator_status(cls) -> bool:
        return cls._get_bool_setting(SEPERATOR_SECTION, SEPERATOR_STATUS)

    @classmethod
    def get_path(cls, value: str) -> str | list | set:
        path = cls.get_string_setting(PATHS_SECTION, value)
        if not path:
            return ""
        if PATH_SEPERATOR in path:
            return path.split(PATH_SEPERATOR)
        return path

    @classmethod
    def set_path(cls, path, value: str | list | set) -> None:
        if isinstance(value, (list, set)):
            value = PATH_SEPERATOR.join(value)
        cls.set_setting(PATHS_SECTION, path, value)


    @classmethod
    def get_issue_path(cls) -> str:
        return cls.get_path(ISSUE_PATH)

    @classmethod
    def set_issue_path(cls, path) -> None:
        cls.set_path(ISSUE_PATH, path)

    @classmethod
    def get_group_folder(cls) -> str:
        return cls.get_path(GROUP_FOLDER)

    @classmethod
    def set_group_folder(cls, value) -> None:
        cls.set_path(GROUP_FOLDER, value)

    @classmethod
    def set_group_pset(cls, value: str) -> None:
        cls.set_setting(IFC_MOD, GROUP_PSET, value)

    @classmethod
    def set_group_attribute(cls, value: str) -> None:
        cls.set_setting(IFC_MOD, GROUP_ATTRIBUTE, value)

    @classmethod
    def get_group_pset(cls, ) -> str:
        return cls.get_string_setting(IFC_MOD, GROUP_PSET)

    @classmethod
    def get_group_attribute(cls, ) -> str:
        return cls.get_string_setting(IFC_MOD, GROUP_ATTRIBUTE)

    @classmethod
    def set_setting(cls, section: str, path: str, value):
        config_parser = cls._get_config()
        if not config_parser.has_section(section):
            config_parser.add_section(section)
        config_parser.set(section, path, str(value))
        cls._write_config(config_parser)

    @classmethod
    def get_string_setting(cls, section: str, path: str, default="") -> str:
        config_parser = cls._get_config()
        if config_parser.has_option(section, path):
            path = config_parser.get(section, path)
            if path is not None:
                return path
        return default

    @classmethod
    def get_settings_path(cls):
        return os.path.join(appdirs.user_config_dir(som_gui.__name__), "config.ini")

    @classmethod
    def _write_config(cls, config_parser) -> None:
        with open(cls.get_settings_path(), "w") as f:
            config_parser.write(f)

    @classmethod
    def _get_config(cls, ) -> ConfigParser:
        config = ConfigParser()
        config_path = cls.get_settings_path()
        parent_folder = os.path.dirname(config_path)
        if not os.path.exists(parent_folder):
            tool.Util.create_directory(parent_folder)
            return config
        if not os.path.exists(config_path):
            return config
        with open(config_path, "r") as f:
            config.read_file(f)
        return config

    @classmethod
    def _get_bool_setting(cls, section: str, path: str) -> bool:
        config_parser = cls._get_config()
        if config_parser.has_option(section, path):
            path = config_parser.get(section, path)
            if path is not None:
                return eval(path)
        return False

    @classmethod
    def is_plugin_activated(cls, name):
        config_parser = cls._get_config()
        if not config_parser.has_option(PLUGINS, name):
            cls.set_setting(PLUGINS, name, True)
            return True
        return cls._get_bool_setting(PLUGINS, name)
