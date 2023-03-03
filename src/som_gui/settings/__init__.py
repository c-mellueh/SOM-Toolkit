import os
from configparser import ConfigParser
CONFIG_PATH =  os.path.join(os.path.dirname(__file__),"config.ini")

def set_file_path(path:str):
    config_path = CONFIG_PATH
    parent_folder = os.path.dirname(config_path)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
    config = ConfigParser()
    config.read(config_path)
    if not config.has_section("paths"):
        config.add_section("paths")
    config.set("paths", "file_path", path)

    with open(CONFIG_PATH,"w") as f:
        config.write(f)

def get_file_path():
    config_path = CONFIG_PATH
    if config_path is None:
        return ""
    config = ConfigParser()
    if not os.path.exists(str(CONFIG_PATH)):
        return ""
    config.read(CONFIG_PATH)
    if config.has_section("paths"):
        return config.get("paths", "file_path")
    return ""
