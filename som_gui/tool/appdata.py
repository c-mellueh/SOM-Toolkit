from __future__ import annotations

import logging
import os
from configparser import ConfigParser

import appdirs

import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.util.constants import PATH_SEPERATOR

PATHS_SECTION = "paths"


class Appdata(som_gui.core.tool.Appdata):

    @classmethod
    def get_path(cls, value: str) -> str | list | set:
        logging.info(f"Appdata Path '{value}' requested")
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
    def set_setting(cls, section: str, path: str, value):
        config_parser = cls._get_config()
        if not config_parser.has_section(section):
            config_parser.add_section(section)
        if type(value) in (list,set,tuple):
            value = PATH_SEPERATOR.join([str(v) for v in value])
        config_parser.set(section, path, str(value))
        cls._write_config(config_parser)


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
    def get_bool_setting(cls, section: str, path: str, default=False) -> bool:
        config_parser = cls._get_config()
        if config_parser.has_option(section, path):
            path = config_parser.get(section, path)
            if path is not None:
                return eval(path)
        cls.set_setting(section, path, default)
        return default

    @classmethod
    def get_string_setting(cls, section: str, path: str, default="") -> str:
        config_parser = cls._get_config()
        if config_parser.has_option(section, path):
            value = config_parser.get(section, path)
            if value is not None:
                return value
        cls.set_setting(section, path, default)
        return default

    @classmethod
    def get_int_setting(cls, section: str, path: str, default=0) -> int:
        config_parser = cls._get_config()
        if config_parser.has_option(section, path):
            path = config_parser.get(section, path)
            if path is not None:
                return int(path)
        cls.set_setting(section, path, default)
        return default

    @classmethod
    def get_float_setting(cls, section: str, path: str, default=0) -> float:
        config_parser = cls._get_config()
        if config_parser.has_option(section, path):
            path = config_parser.get(section, path)
            if path is not None:
                return float(path)
        cls.set_setting(section, path, default)
        return default
    
    @classmethod
    def get_list_setting(cls,section:str,path:str,default = []) -> list[str]:
        config_parser = cls._get_config()
        if config_parser.has_option(section, path):
            value = config_parser.get(section, path)
            value = None if value == "None" else value
            if value is not None:
                return value.split(PATH_SEPERATOR)        
        cls.set_setting(section, path, default)
        return default