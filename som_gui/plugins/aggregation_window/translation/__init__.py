from PySide6.QtCore import QCoreApplication, QTranslator
import os
import logging


def load_language(application, language="de"):
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, f"translation_{language}.qm")
    translator = QTranslator(application)
    if translator.load(path):
        application.installTranslator(translator)
