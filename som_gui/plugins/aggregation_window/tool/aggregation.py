import logging

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QHBoxLayout, QLineEdit

import SOMcreator
import som_gui.plugins.aggregation_window.core.tool
from som_gui import tool
from som_gui.module.object import OK
from som_gui.plugins.aggregation_window.module.aggregation import ui as ui_aggregation
from som_gui.plugins.aggregation_window.module.aggregation.prop import (
    AggregationProperties,
)

ABBREV_ISSUE = 2
from SOMcreator.exporter.desite import building_structure
from PySide6.QtGui import QAction
from PySide6.QtCore import QCoreApplication


class Aggregation(som_gui.plugins.aggregation_window.core.tool.Aggregation):
    @classmethod
    def get_properties(cls) -> AggregationProperties:
        return som_gui.AggregationProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

    @classmethod
    def export_building_structure(cls, project: SOMcreator.Project, path):
        building_structure.export_bs(project, path)

    @classmethod
    def create_abbreviation_line_edit(cls, layout: QHBoxLayout) -> QLineEdit:
        le = QLineEdit()
        text = QCoreApplication.translate("Aggregation", "Abbreviation")
        le.setPlaceholderText(text)
        layout.insertWidget(-1, le)
        return le

    @classmethod
    def object_info_line_edit_paint(cls, data_dict, abbrev_filter):
        abbreviation = data_dict["abbreviation"]
        if not cls.is_abbreviation_allowed(abbreviation, abbrev_filter):
            cls.oi_set_abbrev_value_color("red")
        else:
            cls.oi_set_abbrev_value_color(QPalette().color(QPalette.Text).name())

    @classmethod
    def test_abbreviation(cls, abbreviation: str, obj: SOMcreator.SOMClass) -> int:
        ignore_text = obj.abbreviation if obj is not None else None
        if tool.Object.oi_get_mode() == 2:
            ignore_text = None
        if abbreviation is not None and not cls.is_abbreviation_allowed(
            abbreviation, ignore_text
        ):
            text = QCoreApplication.translate(
                "Aggregation", "Abbreviation exists already"
            )
            tool.Popups.create_warning_popup(text)
            return ABBREV_ISSUE
        return OK

    @classmethod
    def is_abbreviation_allowed(cls, abbreviation, ignore=None):
        abbreviations = cls.get_existing_abbriviations()
        if ignore is not None:
            abbreviations = list(filter(lambda a: a != ignore, abbreviations))
        if abbreviation in abbreviations:
            return False
        else:
            return True

    @classmethod
    def oi_set_abbrev_value_color(cls, color: str):
        widget = cls.get_properties().object_info_line_edit
        style = widget.style()
        widget.setStyleSheet(f"QLineEdit {{color:{color};}}")

    @classmethod
    def get_existing_abbriviations(cls) -> set[str]:
        proj = tool.Project.get()
        abbreviations = set()
        for obj in proj.get_objects(filter=False):
            if obj.abbreviation:
                abbreviations.add(obj.abbreviation)
        return abbreviations

    @classmethod
    def set_object_abbreviation(cls, obj: SOMcreator.SOMClass, abbreviation: str):
        obj.abbreviation = abbreviation

    @classmethod
    def create_oi_line_edit(cls):
        cls.get_properties().object_info_line_edit = ui_aggregation.ObjectInfoLineEdit()
        return cls.get_properties().object_info_line_edit

    @classmethod
    def abbreviation_check(cls, data_dict: dict):
        value = data_dict.get("abbreviation")
        if value is None:
            return True
        if not cls.is_abbreviation_allowed(value):
            text = QCoreApplication.translate(
                "Aggregation", "Abbreviation exists already"
            )
            logging.error(text)
            tool.Popups.create_warning_popup(text)
            return False
        return True
