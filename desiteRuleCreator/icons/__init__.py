import os
from PySide6.QtGui import QIcon

def get_icon():
    icon_path = os.path.join(ICON_PATH, ICON_DICT["icon"])
    print(icon_path)
    return QIcon(icon_path)

ICON_PATH = os.path.dirname(__file__)
ICON_DICT = {"icon": "icon.ico",
             "link": "link.png"}