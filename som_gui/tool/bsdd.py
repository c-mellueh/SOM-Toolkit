from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

import SOMcreator
import datetime
if TYPE_CHECKING:
    from som_gui.module.bsdd.prop import BsddProperties
import som_gui.core.tool
import som_gui
from som_gui.module.bsdd import ui
from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QWidget, QToolBox, QLineEdit, QLabel
from SOMcreator.bsdd import Dictionary
from som_gui.module.bsdd import trigger

class Bsdd(som_gui.core.tool.Bsdd):

    @classmethod
    def get_properties(cls) -> BsddProperties:
        return som_gui.BsddProperties

    @classmethod
    def get_window(cls) -> ui.Widget:
        return cls.get_properties().widget

    @classmethod
    def create_window(cls):
        widget = ui.Widget()
        cls.get_properties().widget = widget
        cls.clear_toolbox()
        return widget

    @classmethod
    def get_toolbox(cls) -> QToolBox:
        return cls.get_window().ui.toolBox

    @classmethod
    def clear_toolbox(cls):
        tb = cls.get_toolbox()
        for index in reversed(range(tb.count())):
            widget = tb.widget(index)
            tb.removeItem(index)
            widget.deleteLater()

    @classmethod
    def set_tabs(cls, tab_list: list[tuple[str, QWidget]]):
        for name, widget in tab_list:
            cls.get_toolbox().addItem(widget, name)

    @classmethod
    def get_dictionary_widget(cls):
        return cls.get_properties().dictionary_widget

    @classmethod
    def create_dictionary_widget(cls):
        from SOMcreator.bsdd import Dictionary

        widget = cls.get_properties().dictionary_widget = ui.DictionaryWidget()
        widget.setLayout(QFormLayout())
        layout: QFormLayout = widget.layout()
        attributes = Dictionary.attributes()

        for index, (name, datatype, preset) in enumerate(attributes):
            if datatype == str:
                if preset is None:
                    w = QLineEdit()
                    w.textChanged.connect(lambda text, wid=w: trigger.dict_attribute_changed(text, wid))
                else:
                    w = QComboBox()
                    w.addItems(preset)
                    w.currentTextChanged.connect(lambda text, wid=w: trigger.dict_attribute_changed(text, wid))
            elif datatype == bool:
                w = QCheckBox()
                w.checkStateChanged.connect(lambda state, wid=w: trigger.dict_attribute_changed(state, wid))
            else:
                logging.warning(f"Datatype: {datatype} not supported")
                w = QLineEdit()
            w.setProperty("attribute_name", name)
            layout.setWidget(index, QFormLayout.ItemRole.FieldRole, w)
            layout.setWidget(index, QFormLayout.ItemRole.LabelRole, QLabel(name))
        return widget

    @classmethod
    def add_widget_to_toolbox(cls, name, widget):
        cls.get_properties().tab_list.append((name, widget))

    @classmethod
    def get_tab_list(cls):
        return cls.get_properties().tab_list

    @classmethod
    def transform_project_to_dict(cls, proj: SOMcreator.Project):
        d = Dictionary("", proj.name, proj.name, proj.version, "de-DE", False, False)
        d.License = "MIT"
        d.LicenseUrl = "https://www.mit.edu/~amini/LICENSE.md"
        d.ReleaseDate = str(datetime.datetime.now().replace(microsecond=0).isoformat())
        cls.get_properties().dictionary = d
        return d

    @classmethod
    def get_dictionary(cls) -> Dictionary:
        return cls.get_properties().dictionary

    @classmethod
    def reset_dictionary(cls):
        cls.get_properties().dictionary = None
