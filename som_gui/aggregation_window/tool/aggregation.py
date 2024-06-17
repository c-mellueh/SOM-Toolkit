import som_gui.aggregation_window.core.tool
from PySide6.QtWidgets import QHBoxLayout, QLineEdit
from som_gui.aggregation_window.module.aggregation.prop import AggregationProperties


class Aggregation(som_gui.aggregation_window.core.tool.Aggregation):
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
