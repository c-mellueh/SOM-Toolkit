from __future__ import annotations
import logging
import os
from typing import TYPE_CHECKING
import SOMcreator
from dataclasses import fields
if TYPE_CHECKING:
    from som_gui.module.bsdd.prop import BsddProperties
import som_gui.core.tool
import som_gui
from som_gui.module.bsdd import ui
from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QWidget, QToolBox, QLineEdit, QLabel
from som_gui.module.bsdd import trigger
from SOMcreator import bsdd
import SOMcreator.bsdd.transformer

LANGUAGE_ISO_CODES = ['EN', 'en-GB', 'nl-NL', 'nb-NO', 'nl-BE', 'fr-BE', 'de-DE', 'it-IT', 'sv-SE', 'fr-FR', 'es-ES',
                      'en-AU', 'fa-IR', 'pl-PL', 'lv-LV', 'en-NZ', 'sr-SP', 'zh-CN', 'ru-RU', 'vi-VN', 'bg-BG', 'kr-KR',
                      'ar-SA', 'el-GR', 'de-AT', 'mn-MN', 'en-CA', 'lt-LT', 'da-DK', 'de-CH', 'et-EE', 'cs-CZ', 'nn-NO',
                      'en-US', 'pt-BR', 'fi-FI', 'ja-JP', 'no-NO', 'pt-PT']


class Bsdd(som_gui.core.tool.Bsdd):

    @classmethod
    def get_properties(cls) -> BsddProperties:
        return som_gui.BsddProperties

    @classmethod
    def get_window(cls) -> ui.Widget:
        return cls.get_properties().widget

    @classmethod
    def get_ui(cls):
        return cls.get_window().ui

    @classmethod
    def create_window(cls):
        widget = ui.Widget()
        cls.get_properties().widget = widget
        widget.ui.bu_select_path.clicked.connect(trigger.path_button_clicked)
        widget.ui.bu_run.clicked.connect(trigger.run_clicked)
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
        presets = cls.get_dict_presets()
        attributes = [(f.name, f.type, presets.get(f.name)) for f in fields(Dictionary) if
                      f.name not in ["Classes", "Properties"]]

        for index, (name, datatype, preset) in enumerate(attributes):
            if datatype == "str":
                if preset is None:
                    w = QLineEdit()
                    w.textChanged.connect(lambda text, wid=w: trigger.dict_attribute_changed(text, wid))
                else:
                    w = QComboBox()
                    w.addItems(preset)
                    w.currentTextChanged.connect(lambda text, wid=w: trigger.dict_attribute_changed(text, wid))
            elif datatype == "bool":
                w = QCheckBox()
                w.checkStateChanged.connect(lambda state, wid=w: trigger.dict_attribute_changed(state, wid))
            elif datatype == "datetime":
                w = QLineEdit()
                w.textChanged.connect(lambda text, wid=w: trigger.dict_attribute_changed(text, wid))
            else:
                logging.info(f"Datatype: '{datatype}' not supported")
                w = QLineEdit()
                w.textChanged.connect(lambda text, wid=w: trigger.dict_attribute_changed(text, wid))

            w.setProperty("attribute_name", name)
            layout.setWidget(index, QFormLayout.ItemRole.FieldRole, w)
            layout.setWidget(index, QFormLayout.ItemRole.LabelRole, QLabel(name))
        return widget

    @classmethod
    def get_path_line_edit(cls):
        return cls.get_ui().le_export_path

    @classmethod
    def add_widget_to_toolbox(cls, name, widget):
        cls.get_properties().tab_list.append((name, widget))

    @classmethod
    def get_tab_list(cls):
        return cls.get_properties().tab_list

    @classmethod
    def transform_project_to_dict(cls, proj: SOMcreator.Project):
        d = SOMcreator.bsdd.transformer.transform_project_to_dict(proj)
        cls.get_properties().dictionary = d
        return d

    @classmethod
    def get_dictionary(cls) -> bsdd.Dictionary:
        return cls.get_properties().dictionary

    @classmethod
    def reset_dictionary(cls):
        cls.get_properties().dictionary = None

    @classmethod
    def add_objects_to_dictionary(cls, project: SOMcreator.Project):
        dictionary = cls.get_dictionary()
        objects = list(project.objects)
        predefined_psets = list(project.get_predefined_psets(filter=False))
        SOMcreator.bsdd.transformer.transform_objects_to_classes(dictionary, objects, predefined_psets)

    @classmethod
    def export_to_json(cls, path: str | os.PathLike):
        dictionary = cls.get_dictionary()
        SOMcreator.bsdd.export(dictionary, path)

    @classmethod
    def get_dict_presets(cls):
        return {
            'OrganizationCode':             None,
            'DictionaryCode':               None,
            'DictionaryName':               None,
            'DictionaryVersion':            None,
            'LanguageIsoCode':              LANGUAGE_ISO_CODES,
            'LanguageOnly':                 None,
            'UseOwnUri':                    None,
            'DictionaryUri':                None,
            'License':                      None,
            'LicenseUrl':                   None,
            'ChangeRequestEmailAddress':    None,
            'ModelVersion':                 ["1.0", "2.0"],
            'MoreInfoUrl':                  None,
            'QualityAssuranceProcedure':    None,
            'QualityAssuranceProcedureUrl': None,
            'ReleaseDate':                  None,
            'Status':                       ["Preview", "Active", "Inactive"],
        }
