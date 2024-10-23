import os
from PySide6.QtCore import QTranslator


def load_language(application, language="en"):
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, f"translation_{language}.qm")
    translator = QTranslator(application)
    print(translator.load(path))
    if translator.load(path):
        print(application.installTranslator(translator))
