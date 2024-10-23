from PySide6.QtCore import QCoreApplication, QTranslator
from PySide6.QtWidgets import QApplication
import os
import logging

translator = QTranslator()


def load_language(application: QApplication, language="de"):
    global translator
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, f"translation_{language}.qm")
    application.removeTranslator(translator)
    translator = QTranslator(application)
    if translator.load(path):
        application.installTranslator(translator)
