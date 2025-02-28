from __future__ import annotations

import logging
import os
from dataclasses import fields
from typing import TYPE_CHECKING

import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.bsdd.prop import BsddProperties
import som_gui.core.tool
import som_gui
from som_gui.module.bsdd import ui
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QWidget,
    QToolBox,
    QLineEdit,
    QLabel,
)
from PySide6.QtGui import QAction
from som_gui.module.bsdd import trigger, constants

import SOMcreator.exporter.bsdd.transformer
from SOMcreator.exporter.bsdd import Dictionary


class Bsdd(som_gui.core.tool.Bsdd):

    @classmethod
    def get_properties(cls) -> BsddProperties:
        return som_gui.BsddProperties

    @classmethod
    def create_window(cls):
        """
        :return: BsDD Window
        """
        widget = ui.Widget()
        cls.get_properties().widget = widget
        widget.ui.bu_select_path.clicked.connect(trigger.path_button_clicked)
        widget.ui.bu_run.clicked.connect(trigger.run_clicked)
        cls.clear_toolbox()
        return widget

    @classmethod
    def clear_toolbox(cls):
        """
        remove all Widgets of Toolbox
        :return:
        """
        tb = cls.get_toolbox()
        for index in reversed(range(tb.count())):
            widget = tb.widget(index)
            tb.removeItem(index)
            widget.deleteLater()

    @classmethod
    def create_dictionary_widget(cls) -> ui.DictionaryWidget:
        """
        Create Widget for Dictionary Settings and fills QFormLayout
        Makes widget creation modular. If you add a field to the dictionary in its definition,
        a line will be added to the widget. As far as the datatype is string bool oder datetime others need to be implemented.
        :return: DictionaryWidget
        """
        # add Layout to Widget
        widget = cls.get_properties().dictionary_widget = ui.DictionaryWidget()
        widget.setLayout(QFormLayout())
        layout: QFormLayout = widget.layout()

        # list all Attributes which aren't lists of elements
        presets = cls.get_dict_presets()
        attributes = [
            (f.name, f.type, presets.get(f.name))
            for f in fields(Dictionary)
            if f.name not in ["Classes", "Properties"]
        ]

        # Fill QFormLayout
        for index, (name, datatype, preset) in enumerate(
            attributes
        ):  # Iterate over all attributes
            if datatype == "str":
                if preset is None:
                    # create input line
                    w = QLineEdit()
                    w.textChanged.connect(
                        lambda text, n=name: trigger.dict_attribute_changed(text, n)
                    )
                else:
                    # create text dropdown
                    w = QComboBox()
                    w.addItems(preset)
                    w.currentTextChanged.connect(
                        lambda text, n=name: trigger.dict_attribute_changed(text, n)
                    )

            # create checkbox
            elif datatype == "bool":
                w = QCheckBox()
                w.checkStateChanged.connect(
                    lambda state, n=name: trigger.dict_attribute_changed(state, n)
                )

            # create input line
            elif datatype == "datetime":
                w = QLineEdit()
                w.textChanged.connect(
                    lambda text, n=name: trigger.dict_attribute_changed(text, n)
                )

            # handle exceptions
            else:
                logging.info(f"Datatype: '{datatype}' not supported")
                w = QLineEdit()
                w.textChanged.connect(
                    lambda text, n=name: trigger.dict_attribute_changed(text, n)
                )

            # fill line of QFormLayout
            cls.set_linked_attribute_name(w, name)
            layout.setWidget(index, QFormLayout.ItemRole.FieldRole, w)
            layout.setWidget(index, QFormLayout.ItemRole.LabelRole, QLabel(name))
        return widget

    @classmethod
    def add_widget_to_toolbox(cls, name, widget):
        """
        Adds widget to list which gets called on Toolbox creation. Needs to be called on Boot
        :param name:
        :param widget:
        :return:
        """
        cls.get_properties().tab_list.append((name, widget))

    @classmethod
    def transform_project_to_dict(cls, proj: SOMcreator.SOMProject):
        """
        Grabs Project Settings and writes them into the BsDD Dictionary
        Won't write Object Classes or Attributes
        :param proj:
        :return:
        """
        d = SOMcreator.exporter.bsdd.transform_project_to_dict(proj)
        cls.get_properties().dictionary = d
        return d

    # Getter & Setter

    @classmethod
    def get_path_line_edit(cls):
        return cls.get_window().ui.le_export_path

    @classmethod
    def set_tabs(cls, tab_list: list[tuple[str, QWidget]]):
        """
        adds tabs defined in tab_list to toolbox
        :param tab_list:
        :return:
        """
        for name, widget in tab_list:
            cls.get_toolbox().addItem(widget, name)

    @classmethod
    def get_dictionary_widget(cls):
        return cls.get_properties().dictionary_widget

    @classmethod
    def reset_classes(cls):
        cls.get_properties().dictionary.Classes = list()

    @classmethod
    def reset_properties(cls):
        cls.get_properties().dictionary.Properties = list()

    @classmethod
    def reset_dictionary(cls):
        cls.get_properties().dictionary = None

    @classmethod
    def add_objects_to_dictionary(cls, project: SOMcreator.SOMProject):
        dictionary = cls.get_dictionary()
        objects = list(project.get_objects(filter=True))
        predefined_psets = list(project.get_predefined_psets(filter=False))
        SOMcreator.exporter.bsdd.transform_objects_to_classes(
            dictionary, objects, predefined_psets
        )

    @classmethod
    def export_to_json(cls, path: str | os.PathLike):
        dictionary = cls.get_dictionary()
        SOMcreator.exporter.bsdd.export_dict(dictionary, path)

    @classmethod
    def get_tab_list(cls):
        return cls.get_properties().tab_list

    @classmethod
    def get_dictionary(cls) -> Dictionary:
        return cls.get_properties().dictionary

    @classmethod
    def get_dict_presets(cls):
        return {
            "OrganizationCode": None,
            "DictionaryCode": None,
            "DictionaryName": None,
            "DictionaryVersion": None,
            "LanguageIsoCode": constants.LANGUAGE_ISO_CODES,
            "LanguageOnly": None,
            "UseOwnUri": None,
            "DictionaryUri": None,
            "License": None,
            "LicenseUrl": None,
            "ChangeRequestEmailAddress": None,
            "ModelVersion": ["1.0", "2.0"],
            "MoreInfoUrl": None,
            "QualityAssuranceProcedure": None,
            "QualityAssuranceProcedureUrl": None,
            "ReleaseDate": None,
            "Status": ["Preview", "Active", "Inactive"],
        }

    @classmethod
    def get_linked_attribute_name(cls, item: QWidget):
        return item.property(constants.POPERTY_KEY)

    @classmethod
    def set_linked_attribute_name(cls, item: QWidget, value):
        return item.setProperty(constants.POPERTY_KEY, value)

    @classmethod
    def is_update_blocked(cls):
        layout: QFormLayout = cls.get_dictionary_widget().layout()
        for row in range(layout.rowCount()):
            item = layout.itemAt(
                row * 2
            ).widget()  # get Value Widget "*2" is needed because QFormLayout item handling
            if not isinstance(item, QLineEdit):
                continue
            if item.hasFocus():
                logging.debug(f"{cls.get_linked_attribute_name(item)} has focus.")
                return True

        return False

    @classmethod
    def get_export_path(cls) -> str:
        return cls.get_path_line_edit().text()

    @classmethod
    def trigger_retranslation(cls):
        trigger.retranslate_ui()

    @classmethod
    def get_open_window_trigger(cls):
        return trigger.open_window

    @classmethod
    def set_action(cls, name: str, action: QAction) -> None:
        """
        add QAction to list of actions That exist. Mostly used for retranslate_ui
        """
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name) -> QAction:
        """
        :param name: name of action
        :return: QAction from list of actions That exist by name
        """
        return cls.get_properties().actions[name]

    @classmethod
    def get_window(cls) -> ui.Widget:
        """
        :return: BsDD Settings Window
        """
        return cls.get_properties().widget

    @classmethod
    def get_toolbox(cls) -> QToolBox:
        """

        :return: Toolbox of BsDD Window
        """
        return cls.get_window().ui.toolBox
