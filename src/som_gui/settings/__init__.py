import os
from configparser import ConfigParser
CONFIG_PATH =  os.path.join(os.path.dirname(__file__),"config.ini")

def set_file_path(path:str):
    config_path = CONFIG_PATH
    config = ConfigParser()
    config.read(config_path)
    config.set("paths", "file_path", path)
    with open(CONFIG_PATH,"w") as f:
        config.write(f)

def get_file_path():
    config_path = CONFIG_PATH
    config = ConfigParser()
    config.read(config_path)
    return config.get("paths", "file_path")
