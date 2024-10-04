from __future__ import annotations
from som_gui import tool
import logging
from typing import TYPE_CHECKING
from PySide6.QtCore import QRunnable, Signal, QObject, QThreadPool
import som_gui
from som_gui.plugins.ifc_tools.module.move import ui, trigger
import ifcopenshell
import os

if TYPE_CHECKING:
    from som_gui.plugins.ifc_tools.module.move.prop import MoveProperties
    from som_gui.tool.ifc_importer import IfcImportRunner

FACTOR_DICT = {
    "EXA":   10 ^ 18,
    "PETA":  10 ^ 15,
    "TERA":  10 ^ 12,
    "GIGA":  10 ^ 9,
    "MEGA":  10 ^ 6,
    "KILO":  10 ^ 3,
    "HECTO": 10 ^ 2,
    "DECA":  10,
    "DECI":  10 ^ -1,
    "CENTI": 10 ^ -2,
    "MILLI": 10 ^ -3,
    "MICRO": 10 ^ -6,
    "NANO":  10 ^ -9,
    "PICO":  10 ^ -12,
    "FEMTO": 10 ^ -15,
    "ATTO":  10 ^ -18,
}


class Signaller(QObject):
    finished = Signal()
    status = Signal(str)
    progress = Signal(int)


class MoveRunner(QRunnable):
    def __init__(self, ifc_file: ifcopenshell.file, path: str):
        super().__init__()
        self.file = ifc_file
        self.path = path
        self.signaller = Signaller()

    def run(self):
        trigger.move_started(self.file, self.path)
        self.signaller.finished.emit()


class Move:
    @classmethod
    def get_properties(cls) -> MoveProperties:
        return som_gui.MoveProperties

    @classmethod
    def create_widget(cls):
        widget = ui.MoveWidget()
        cls.get_properties().widget = widget
        widget.ui.buttonBox.clicked.connect(trigger.button_box_clicked)
        return widget

    @classmethod
    def reset_buttons(cls):
        bb = cls.get_widget().ui.buttonBox
        bb.setStandardButtons(bb.StandardButton.Close | bb.StandardButton.Apply)

    @classmethod
    def get_widget(cls):
        return cls.get_properties().widget

    @classmethod
    def get_coordinate_values(cls) -> tuple[float, float, float]:
        widget_ui = cls.get_widget().ui
        return widget_ui.dsb_x.value(), widget_ui.dsb_y.value(), widget_ui.dsb_z.value()

    @classmethod
    def set_coordinate_values(cls, values: tuple[float, float, float]):
        widget_ui = cls.get_widget().ui
        widget_ui.dsb_x.setValue(values[0]), widget_ui.dsb_y.setValue(values[1]), widget_ui.dsb_z.setValue(values[2])

    @classmethod
    def connect_runner(cls, runner: IfcImportRunner):
        runner.signaller.started.connect(lambda: trigger.ifc_import_started(runner))
        runner.signaller.finished.connect(lambda: trigger.ifc_import_finished(runner))

    @classmethod
    def create_move_runner(cls, ifc_file: ifcopenshell.file, path: str):
        runner = MoveRunner(ifc_file, path)
        runner.signaller.finished.connect(trigger.move_finished)
        return runner

    @classmethod
    def get_threadpool(cls):
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
            tp.setMaxThreadCount(1)
        return cls.get_properties().thread_pool

    @classmethod
    def set_status(cls, status_text: str, progress_value: int = None):
        progressbar = cls.get_widget().ui.widget_progress_bar.ui.progressBar
        status_label = cls.get_widget().ui.widget_progress_bar.ui.label
        if progress_value is not None:
            progressbar.setValue(progress_value)
        if status_text is not None:
            status_label.setText(status_text)

    @classmethod
    def move_ifc(cls, ifc: ifcopenshell.file, export_path: str, coordinates: tuple[float, float, float]):

        projects = ifc.by_type("IfcProject")
        if len(projects) > 1:
            logging.error(f"Projektanzahl in IFC > 1 -> Abbruch")
            return
        project: ifcopenshell.entity_instance = projects[0]
        length_units = [u for u in project.UnitsInContext.Units if u.UnitType == "LENGTHUNIT"]
        if len(length_units) > 1:
            logging.error(f"Anzahl definierter Längeneinheiten in IFC > 1 -> Abbruch")
            return
        length_unit = length_units[0]
        if length_unit.Name != "METRE":
            logging.error(f"LenghtUnit is not METRE -> Abbruch")
            return
        factor = 1
        if length_unit.Prefix is not None:
            factor = 1 / FACTOR_DICT[length_unit.Prefix]
        logging.info(f"MoveFactor = {factor}")
        sites = [x for xs in [aggregation.RelatedObjects for aggregation in project.IsDecomposedBy] for x in xs]
        for site in sites:
            old_placement = site.ObjectPlacement
            if old_placement.PlacementRelTo:
                logging.warning(f"Siteplacement {old_placement} references to different placement")
            old_coordinates = old_placement.RelativePlacement.Location.Coordinates
            new_coordinates = [o + n * factor for o, n in zip(old_coordinates, coordinates)]
            logging.info(f"New Site coordinates = {new_coordinates}")
            point = ifc.create_entity("IfcCartesianPoint", Coordinates=new_coordinates)
            axis_placement = ifc.create_entity("IfcAxis2Placement3D", Location=point)
            site.ObjectPlacement.RelativePlacement = axis_placement

        folder, path = os.path.split(export_path)
        path = f"moved_{path}"
        cls.set_status(f"Save IFC to '{path}'", 50)

        ifc.write(os.path.join(folder, path))
