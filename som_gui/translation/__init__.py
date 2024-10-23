import os
from PySide6.QtCore import QTranslator,QLocale
from PySide6.QtWidgets import QApplication

translator = QTranslator()


def load_language(application: QApplication, language="en"):
    global translator
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, f"translation_{language}.qm")
    application.removeTranslator(translator)
    locale = QLocale(language)

    if translator.load(locale, 'qtbase', '_', 'PySide6/translations/'):
        application.installTranslator(translator)
    translator = QTranslator(application)
    if translator.load(path):
        application.installTranslator(translator)
