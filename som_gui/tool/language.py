from __future__ import annotations

import importlib
import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QApplication

import som_gui
import som_gui.core.tool

if TYPE_CHECKING:
    from som_gui.module.language.prop import LanguageProperties
    from som_gui.module.language import ui

from som_gui.resources.translation import load_language


class Language(som_gui.core.tool.Language):
    @classmethod
    def get_properties(cls) -> LanguageProperties:
        return som_gui.LanguageProperties

    @classmethod
    def set_widget(cls, widget: ui.SettingsWidget):
        cls.get_properties().widget = widget

    @classmethod
    def get_widget(cls) -> ui.SettingsWidget:
        return cls.get_properties().widget

    @classmethod
    def set_language(cls, code: str):
        cls.get_properties().current_language = code

    @classmethod
    def get_language(cls) -> str:
        return cls.get_properties().current_language

    @classmethod
    def get_system_language(cls) -> str:
        return QLocale.system().countryToCode(QLocale.system().country()).lower()

    @classmethod
    def translate_main_ui(cls, app: QApplication, lang_code: str):
        load_language(app, lang_code)

    @classmethod
    def translate_plugins(cls, plugin_names: list[str], app: QApplication, lang_code: str):
        for plugin_name in plugin_names:
            module_text = f"som_gui.plugins.{plugin_name}"
            try:
                text = f"{module_text}.resources.translation"
                module = importlib.import_module(text)
                module.load_language(app, lang_code)
            except ModuleNotFoundError:
                logging.warning(f"Plugin '{plugin_name}' has no translation")
