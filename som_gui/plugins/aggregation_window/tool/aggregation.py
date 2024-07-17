import som_gui.plugins.aggregation_window.core.tool
from PySide6.QtWidgets import QHBoxLayout, QLineEdit
from som_gui.plugins.aggregation_window.module.aggregation.prop import AggregationProperties
import SOMcreator
from som_gui import tool
from som_gui.module.object import OK
from som_gui.plugins.aggregation_window.module.aggregation import ui as ui_aggregation
import logging
ABBREV_ISSUE = 2
from SOMcreator.external_software.desite import building_structure

class Aggregation(som_gui.plugins.aggregation_window.core.tool.Aggregation):
    @classmethod
    def export_building_structure(cls, project: SOMcreator.Project, path):
        building_structure.export_bs(project, path)

    @classmethod
    def get_properties(cls) -> AggregationProperties:
        return som_gui.AggregationProperties

    @classmethod
    def create_abbreviation_line_edit(cls, layout: QHBoxLayout) -> QLineEdit:
        le = QLineEdit()
        le.setPlaceholderText(le.tr("Abkürzung"))
        cls.get_properties().abbreviation_line_edit = le
        layout.insertWidget(-1, le)
        return le

    @classmethod
    def object_info_line_edit_paint(cls, data_dict, abbrev_filter):
        abbreviation = data_dict["abbreviation"]
        if not cls.is_abbreviation_allowed(abbreviation, abbrev_filter):
            cls.oi_set_abbrev_value_color("red")
        else:
            cls.oi_set_abbrev_value_color("black")

    @classmethod
    def test_abbreviation(cls, abbreviation: str, obj: SOMcreator.Object) -> int:
        ignore_text = obj.abbreviation if obj is not None else None
        if tool.Object.oi_get_mode() == 2:
            ignore_text = None
        if abbreviation is not None and not cls.is_abbreviation_allowed(abbreviation, ignore_text):
            text = u"Abkürzung existiert bereits!"
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
        widget.setStyleSheet(f"color:{color}")

    @classmethod
    def get_existing_abbriviations(cls) -> set[str]:
        proj = tool.Project.get()
        abbreviations = set()
        for obj in proj.get_all_objects():
            if obj.abbreviation:
                abbreviations.add(obj.abbreviation)
        return abbreviations

    @classmethod
    def set_object_abbreviation(cls, obj: SOMcreator.Object, abbreviation: str):
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
            text = "Abkürzung existiert bereits!"
            logging.error(text)
            tool.Popups.create_warning_popup(text)
            return False
        return True

