from __future__ import annotations
from PySide6.QtCore import QCoreApplication
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.module.language import ui
import som_gui

SECTION = "langugage"
PATH = "current_language"


def settings_widget_created(widget: ui.SettingsWidget, language: Type[tool.Language]):
    language.set_widget(widget)
    retranslate_ui(language)


def settings_accepted(language: Type[tool.Language]):
    from som_gui.module.language import trigger
    widget = language.get_widget()
    cb = widget.ui.comboBox
    code = cb.currentData()
    trigger.set_language(code)


def set_language(code: str | None, language: Type[tool.Language], appdata: Type[tool.Appdata],
                 main_window: Type[tool.MainWindow],
                 plugings: Type[tool.Plugins]):
    """
    Sets UI Language
    if code is None checks last unsed language or System-Language
    """
    if code is None:
        system_lang = language.get_system_language()
        code = appdata.get_string_setting(SECTION, PATH, system_lang)

    language.set_language(code)
    appdata.set_setting(SECTION, PATH, code)

    app = main_window.get_app()
    language.translate_main_ui(app, code)

    plugin_names = [n for n in plugings.get_available_plugins() if plugings.is_plugin_active(n)]
    language.translate_plugins(plugin_names, app, code)
    som_gui.retranslate_ui()


def retranslate_ui(language: Type[tool.Language]):
    widget = language.get_widget()
    if not widget:
        return
    widget.ui.retranslateUi(widget)
    combobox = widget.ui.comboBox
    combobox.clear()
    combobox.addItem(QCoreApplication.translate("Settings", "German"), "de")
    combobox.addItem(QCoreApplication.translate("Settings", "English"), "en")
    current_lang = language.get_language()
    for item in range(combobox.count()):
        if combobox.itemData(item) == current_lang:
            combobox.setCurrentIndex(item)
