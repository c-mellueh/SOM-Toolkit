from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import pandas as pd
import ifcopenshell
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Qt, Signal
from PySide6.QtGui import QAction, QBrush, QPalette
from PySide6.QtWidgets import QCheckBox, QComboBox, QTableWidget, QTableWidgetItem
from ifcopenshell.util import element as ifc_element_util

import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.attribute_import import trigger, ui
from som_gui.module.attribute_import.constants import *

if TYPE_CHECKING:
    from som_gui.module.attribute_import.prop import (
        PropertyImportProperties,
        PropertyImportSQLProperties,
    )
    from som_gui.module.ifc_importer.ui import IfcImportWidget
    from som_gui.tool.ifc_importer import IfcImportRunner
    from som_gui.module.util.ui import Progressbar

import sqlite3


class PropertyImportRunner(QRunnable):
    def __init__(self, runner: IfcImportRunner, progress_bar=None):
        super().__init__()
        self.file: ifcopenshell.file = runner.ifc
        self.path = runner.path
        self.signaller = Signaller()
        self.progress_bar: Progressbar = progress_bar

    def run(self):
        trigger.start_attribute_import(self)
        self.signaller.finished.emit()


class Signaller(QObject):
    finished = Signal()
    status = Signal(str)
    progress = Signal(int)


class PropertyImportResults(som_gui.core.tool.PropertyImportResults):

    @classmethod
    def get_properties(cls) -> PropertyImportProperties:
        return som_gui.PropertyImportProperties

    @classmethod
    def checkstate_to_int(cls, checkstate: Qt.CheckState) -> int:
        return (
            1
            if checkstate in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked)
            else 0
        )

    @classmethod
    def get_ifctype_combo_box(cls) -> QComboBox:
        return cls.get_properties().ifc_combobox

    @classmethod
    def get_somtype_combo_box(cls) -> QComboBox:
        return cls.get_properties().som_combobox

    @classmethod
    def connect_trigger(cls, property_widget: ui.PropertyImportResultWindow):

        prop = cls.get_properties()
        ui = property_widget.ui
        update_trigger = trigger.update_import_window
        prop.ifc_combobox.currentIndexChanged.connect(update_trigger)
        prop.som_combobox.currentIndexChanged.connect(update_trigger)

        ui.table_widget_property_set.itemSelectionChanged.connect(
            trigger.pset_table_selection_changed
        )
        ui.table_widget_property.itemSelectionChanged.connect(
            trigger.property_table_selection_changed
        )
        cls.get_properties().all_checkbox.checkStateChanged.connect(
            trigger.all_checkbox_checkstate_changed
        )
        ui.buttonBox.accepted.connect(trigger.result_acccept_clicked)
        ui.buttonBox.rejected.connect(trigger.result_abort_clicked)
        ui.button_settings.clicked.connect(trigger.settings_clicked)
        ui.button_download.clicked.connect(trigger.download_clicked)
        ui.combo_box_ifc_type.currentIndexChanged.connect(
            trigger.update_identifier_combobox
        )

    @classmethod
    def update_combobox(cls, combobox: QComboBox, allowed_values: set[str]):
        cls.lock_updating("IfcType ComboBox")
        existing_ifc_types = set(tool.Util.get_combobox_values(combobox))
        add_items = allowed_values.difference(existing_ifc_types)
        delete_items = existing_ifc_types.difference(allowed_values)
        combobox.addItems(list(add_items))
        for item in delete_items:
            combobox.removeItem(combobox.findText(item))
        if add_items or delete_items:
            combobox.mod().sort(0)
        cls.unlock_updating()

    @classmethod
    def update_som_combobox(
        cls,
        combobox: QComboBox,
        allowed_values: set[str],
        object_list: list[SOMcreator.SOMClass],
    ):
        cls.lock_updating("SOM ComboBox")
        all_keyword = cls.get_all_keyword()
        object_dict = {obj.ident_value: obj for obj in object_list}
        allowed_objects = set(object_dict.get(v) for v in allowed_values)
        existing_objects = {
            combobox.itemData(index, Qt.ItemDataRole.UserRole)
            for index in range(combobox.count())
            if combobox.itemText(index) != all_keyword
        }

        add_items = allowed_objects.difference(existing_objects)
        delete_items = existing_objects.difference(allowed_objects)
        if None in add_items:
            add_items.remove(None)
        if not (add_items or delete_items):
            cls.unlock_updating()
            return

        for obj in delete_items:
            combobox.removeItem(combobox.findData(obj, Qt.ItemDataRole.UserRole))

        for obj in add_items:
            combobox.addItem(f"{obj.name} ({obj.ident_value})", userData=obj)

        if combobox.findText(all_keyword) == -1:
            combobox.addItem(all_keyword, userData=all_keyword)
        if add_items or delete_items:
            combobox.mod().sort(0)
        cls.unlock_updating()

    @classmethod
    def get_all_keyword(cls) -> str:
        return cls.get_properties().all_keyword

    @classmethod
    def is_window_allready_build(cls) -> bool:
        return cls.get_results_window() is not None

    @classmethod
    def get_results_window(cls) -> ui.PropertyImportResultWindow:
        return cls.get_properties().result_window

    @classmethod
    def remove_results_window(cls):
        cls.get_properties().result_window = None

    @classmethod
    def create_import_window(cls) -> ui.PropertyImportResultWindow:
        prop = cls.get_properties()
        widget = ui.PropertyImportResultWindow()
        prop.result_window = widget
        prop.ifc_combobox = widget.ui.combo_box_ifc_type
        prop.som_combobox = widget.ui.combo_box_identifier
        prop.all_checkbox = widget.ui.check_box_values

        return prop.result_window

    @classmethod
    def update_results_window(cls):
        trigger.update_ifc_type_combobox()
        trigger.update_object_count()
        trigger.update_property_set_table()
        trigger.update_all_checkbox()

    @classmethod
    def get_pset_table(cls) -> ui.PropertySetTable:
        return cls.get_results_window().ui.table_widget_property_set

    @classmethod
    def get_selected_property_set(cls) -> str | None:
        items = cls.get_pset_table().selectedItems()
        if not items:
            return None
        return items[0].text()

    @classmethod
    def get_property_table(cls) -> ui.PropertyTable:
        return cls.get_results_window().ui.table_widget_property

    @classmethod
    def disable_table(cls, table_widget: QTableWidget):
        table_widget.setRowCount(0)
        table_widget.setDisabled(True)

    @classmethod
    def get_selected_property(cls) -> str | None:
        items = cls.get_property_table().selectedItems()
        if not items:
            return None
        return items[0].text()

    @classmethod
    def get_value_table(cls) -> ui.ValueTable:
        return cls.get_results_window().ui.table_widget_value

    @classmethod
    def get_value_from_table_row(
        cls, table_widget: QTableWidget, row: int, data_types: list
    ):
        column_count = table_widget.columnCount()
        items = list()
        for col, data_type in zip(range(column_count), data_types):
            if data_type == Qt.CheckState:
                items.append(table_widget.cellWidget(row, col))
            else:
                items.append(table_widget.item(row, col))

        values = list()

        for item, data_type in zip(items, data_types):
            if isinstance(item, QTableWidgetItem):
                values.append(data_type(item.text()))
            else:
                values.append(Qt.CheckState)
        return tuple(values)

    @classmethod
    def get_existing_values_in_table(cls, table_widget: QTableWidget, datatypes: list):
        existing_values = set()
        for row in range(table_widget.rowCount()):
            check_item = (
                table_widget.cellWidget(row, 0)
                if datatypes[0] == Qt.CheckState
                else table_widget.item(row, 0)
            )
            if check_item is None:
                continue
            existing_values.add(
                cls.get_value_from_table_row(table_widget, row, datatypes)
            )
        return existing_values

    @classmethod
    def lock_updating(cls, reason):
        cls.get_properties().is_updating_locked = True
        cls.get_properties().update_lock_reason = reason

    @classmethod
    def unlock_updating(cls):
        cls.get_properties().is_updating_locked = False
        cls.get_properties().update_lock_reason = ""

    @classmethod
    def is_updating_locked(cls):
        return cls.get_properties().is_updating_locked

    @classmethod
    def get_update_lock_reason(cls):
        return cls.get_properties().update_lock_reason

    @classmethod
    def update_table_widget(
        cls,
        allowed_values: set[tuple],
        table_widget: QTableWidget,
        datatypes: list,
    ):
        if not allowed_values:
            return
        existing_values = cls.get_existing_values_in_table(table_widget, datatypes)
        add_items = allowed_values.difference(existing_values)
        delete_items = existing_values.difference(allowed_values)
        if not add_items and not delete_items:
            return

        cls.lock_updating(f"Update TableWidget {table_widget}")

        table_widget.setSortingEnabled(False)

        old_row_count = table_widget.rowCount()
        table_widget.setRowCount(old_row_count + len(add_items))

        for row, values in enumerate(add_items, start=old_row_count):
            for col, value in enumerate(values):
                if datatypes[col] == Qt.CheckState:
                    item = ui.ValueCheckBox(table_widget)
                    table_widget.setCellWidget(row, col, item)
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item = QTableWidgetItem()
                    item.setData(Qt.ItemDataRole.EditRole, value)
                    table_widget.setItem(row, col, item)

        for row in reversed(range(table_widget.rowCount())):
            check_item = (
                table_widget.cellWidget(row, 0)
                if datatypes[0] == Qt.CheckState
                else table_widget.item(row, 0)
            )

            if check_item is None:
                table_widget.removeRow(row)
                continue
            tup = cls.get_value_from_table_row(table_widget, row, datatypes)
            if tup in delete_items:
                table_widget.removeRow(row)
        table_widget.resizeColumnsToContents()
        table_widget.setSortingEnabled(True)
        cls.unlock_updating()

    @classmethod
    def update_valuetable_checkstate(cls, checkstate_dict: dict[str, bool]):
        cls.lock_updating(f"Update Valuetable Checkstate")

        table_widget = cls.get_value_table()
        for row in range(table_widget.rowCount()):
            check_item: QCheckBox = table_widget.cellWidget(row, 0)
            value_item = table_widget.item(row, 1)
            if None in (check_item, value_item):
                continue
            value_text = value_item.text()
            cs = checkstate_dict[value_text]
            if check_item.checkState() != cs:
                check_item.setCheckState(cs)

        cls.unlock_updating()

    @classmethod
    def find_checkbox_row_in_table(
        cls, table_widget: QTableWidget, checkbox: ui.ValueCheckBox
    ) -> int:
        for row in range(table_widget.rowCount()):
            if table_widget.cellWidget(row, 0) == checkbox:
                return row
        return -1

    @classmethod
    def get_input_variables(cls):
        all_keyword = cls.get_all_keyword()
        ifc_type = cls.get_ifctype_combo_box().currentText()
        som_object = cls.get_somtype_combo_box().currentData(Qt.ItemDataRole.UserRole)
        if som_object is not None:
            som_object = (
                som_object.ident_value if som_object != all_keyword else all_keyword
            )
        property_set = cls.get_selected_property_set()
        som_property = cls.get_selected_property()

        values = [ifc_type, som_object, property_set, som_property]
        outputs = list()
        for value in values:
            if value is None:
                outputs.append(None)
            elif value == all_keyword:
                outputs.append("IS NOT ''")
            else:
                outputs.append(f"=='{value}'")
        return tuple(outputs)

    @classmethod
    def set_object_count_label_text(cls, text: str):
        label = cls.get_results_window().ui.label_object_count
        label.setText(label.tr(text))

    @classmethod
    def calculate_all_checkbox_state(cls) -> Qt.CheckState | None:
        table = cls.get_value_table()
        if table.cellWidget(0, 0) is None:
            return None
        checkstates = {
            table.cellWidget(row, 0).checkState() for row in range(table.rowCount())
        }
        if len(checkstates) == 1:
            if None in checkstates:
                return None
            return list(checkstates)[0]
        return Qt.CheckState.PartiallyChecked

    @classmethod
    def set_all_checkbox_state(cls, state: Qt.CheckState):
        cls.lock_updating(f"Update All Checkbox")
        cls.get_properties().all_checkbox.setCheckState(state)
        cls.unlock_updating()

    @classmethod
    def get_all_checkbox(cls):
        return cls.get_properties().all_checkbox

    @classmethod
    def build_property_dict(
        cls, objects: list[SOMcreator.SOMClass]
    ) -> dict[str, dict[str, dict[str, SOMcreator.SOMProperty]]]:
        result_dict = dict()
        for obj in objects:
            object_dict = dict()
            for pset in obj.get_property_sets(filter=True):
                object_dict[pset.name] = {
                    p.name: p for p in pset.get_properties(filter=True)
                }
            result_dict[obj.ident_value] = object_dict
        return result_dict

    @classmethod
    def get_property_item_text_color(cls, row: int):
        palette = QPalette()
        if not tool.PropertyImportSQL.get_properties().color_values:
            return palette.base(), palette.text()

        table_widget = cls.get_property_table()
        count_item = table_widget.item(row, 1)
        distinct_count_item = table_widget.item(row, 2)
        count = int(count_item.text())
        distinct_count = int(distinct_count_item.text())
        if distinct_count == 1:
            if count > 1:
                return Qt.GlobalColor.red, palette.text()
        elif distinct_count == count:
            return Qt.GlobalColor.blue, palette.text()
        return palette.base(), palette.text()

    @classmethod
    def update_property_table_styling(cls):
        table_widget = cls.get_property_table()
        column_count = table_widget.columnCount()
        for row in range(table_widget.rowCount()):
            brush_col, text_col = cls.get_property_item_text_color(row)
            for column in range(column_count):
                brush = QBrush(brush_col)
                table_widget.item(row, column).setBackground(brush)


class PropertyImport(som_gui.core.tool.PropertyImport):
    @classmethod
    def get_properties(cls) -> PropertyImportProperties:
        return som_gui.PropertyImportProperties

    @classmethod
    def set_action(cls, name, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name) -> QAction:
        return cls.get_properties().actions[name]

    @classmethod
    def create_ifc_import_window(cls, ifc_importer: IfcImportWidget) -> IfcImportWidget:
        prop = cls.get_properties()
        prop.ifc_import_window = ifc_importer
        prop.run_button = ifc_importer.ui.button_run
        prop.abort_button = ifc_importer.ui.button_close
        ifc_importer.setWindowIcon(som_gui.get_icon())
        trigger.connect_import_buttons(prop.run_button, prop.abort_button)
        return prop.ifc_import_window

    @classmethod
    def get_ifc_import_window(cls) -> IfcImportWidget:
        return cls.get_properties().ifc_import_window

    @classmethod
    def set_main_pset(cls, main_pset_name: str) -> None:
        cls.get_properties().main_pset = main_pset_name

    @classmethod
    def get_main_pset(cls) -> str:
        return cls.get_properties().main_pset

    @classmethod
    def set_main_property(cls, main_property_name: str) -> None:
        cls.get_properties().main_property = main_property_name

    @classmethod
    def get_main_property(cls) -> str:
        return cls.get_properties().main_property

    @classmethod
    def is_aborted(cls) -> bool:
        return cls.get_properties().import_is_aborted

    @classmethod
    def reset_abort(cls) -> None:
        cls.get_properties().import_is_aborted = False

    @classmethod
    def create_import_runner(
        cls, ifc_import_path: str, progress_bar: Progressbar
    ) -> IfcImportRunner:
        runner = tool.IfcImporter.create_runner(progress_bar, ifc_import_path)
        cls.get_properties().ifc_import_runners.append(runner)
        return runner

    @classmethod
    def connect_ifc_import_runner(cls, runner) -> None:
        trigger.connect_ifc_import_runner(runner)

    @classmethod
    def destroy_import_runner(cls, runner) -> None:
        cls.get_properties().ifc_import_runners.remove(runner)

    @classmethod
    def create_property_import_runner(
        cls, runner: IfcImportRunner
    ) -> PropertyImportRunner:
        runner = PropertyImportRunner(runner, runner.progress_bar)
        return runner

    @classmethod
    def connect_property_import_runner(cls, runner: PropertyImportRunner) -> None:
        trigger.connect_property_import_runner(runner)

    @classmethod
    def get_threadpool(cls) -> QThreadPool:
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
            tp.setMaxThreadCount(1)
        return cls.get_properties().thread_pool

    @classmethod
    def import_is_running(cls):
        return cls.get_threadpool().activeThreadCount() > 0

    @classmethod
    def last_import_finished(cls):
        trigger.last_import_finished()

    @classmethod
    def set_progress(cls, runner: PropertyImportRunner, value: int):
        runner.signaller.progress.emit(value)

    @classmethod
    def set_status(cls, runner: PropertyImportRunner, status: str):
        runner.signaller.status.emit(status)


class PropertyImportSQL(som_gui.core.tool.PropertyImportSQL):
    @classmethod
    def get_properties(cls) -> PropertyImportSQLProperties:
        return som_gui.PropertyImportSQLProperties

    @classmethod
    def create_settings_window(
        cls,
    ):
        cls.get_properties().settings_dialog = ui.SettingsDialog()
        return cls.get_properties().settings_dialog

    @classmethod
    def get_settings_dialog_checkbox_list(
        cls, dialog: ui.SettingsDialog
    ) -> list[tuple[QCheckBox, str]]:
        widget = dialog.widget
        checkbox_list = [
            (widget.check_box_regex, "show_regex_values"),
            (widget.check_box_existing_properties, "show_existing_values"),
            (widget.check_box_color, "color_values"),
            (widget.check_box_range, "show_range_values"),
            (widget.check_box_boolean_values, "show_boolean_values"),
            (widget.check_box_object_filter, "activate_object_filter"),
        ]
        return checkbox_list

    @classmethod
    def update_settins_dialog_checkstates(cls, dialog: ui.SettingsDialog):
        checkbox_list = cls.get_settings_dialog_checkbox_list(dialog)
        prop = cls.get_properties()
        for checkbox, property_name in checkbox_list:
            checkbox.setChecked(getattr(prop, property_name))

    @classmethod
    def settings_dialog_accepted(cls, dialog: ui.SettingsDialog):
        prop = cls.get_properties()
        for widget, property_name in cls.get_settings_dialog_checkbox_list(dialog):
            setattr(prop, property_name, widget.isChecked())

    @classmethod
    def get_cursor(cls):
        return cls.get_properties().connection.cursor()

    @classmethod
    def set_current_object_filter(
        cls, usecases: list[SOMcreator.UseCase], phases: list[SOMcreator.Phase]
    ):
        cls.get_properties().active_usecases = usecases
        cls.get_properties().active_phases = phases

    @classmethod
    def get_current_object_filter(
        cls,
    ) -> tuple[list[SOMcreator.UseCase], list[SOMcreator.Phase]]:
        return cls.get_properties().active_usecases, cls.get_properties().active_phases

    @classmethod
    def set_database_path(cls, path: str) -> None:
        cls.get_properties().database_path = path

    @classmethod
    def get_database_path(cls) -> str:
        return cls.get_properties().database_path

    @classmethod
    def connect_to_data_base(cls, path):
        conn = sqlite3.connect(path)
        cls.get_properties().connection = conn

    @classmethod
    def disconnect_from_database(cls):
        cls.get_properties().connection.commit()
        cls.get_properties().connection.close()
        cls.get_properties().connection = None

    @classmethod
    def commit_sql(cls):
        con = cls.get_properties().connection
        if con is None:
            return
        con.commit()

    @classmethod
    def create_table_exection_query(
        cls, table_name: str, row_names: list[str], row_datatypes: list[str]
    ):
        rows = ",".join([f"{n} {d}" for n, d in zip(row_names, row_datatypes)])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({rows})"
        logging.debug(query)
        return query

    @classmethod
    def create_tables(cls):
        cursor = cls.get_cursor()

        # entities
        query = cls.create_table_exection_query(
            ENTITY_TABLE_NAME, ENTITY_TABLE_HEADER, ENTITY_TABLE_DATATYPES
        )
        cursor.execute(query)
        cls.commit_sql()

        # imported_properties

        query = cls.create_table_exection_query(
            PROPERTY_TABLE_NAME, PROPERTY_TABLE_HEADER, PROPERTY_TABLE_DATATYPES
        )
        cursor.execute(query)
        cls.commit_sql()

        query = cls.create_table_exection_query(
            SOM_TABLE_NAME, SOM_TABLE_HEADER, SOM_TABLE_DATATYPES
        )
        cursor.execute(query)
        cls.commit_sql()

        query = cls.create_table_exection_query(
            FILTER_TABLE_NAME, FILTER_TABLE_HEADER, FILTER_TABLE_DATATYPES
        )
        cursor.execute(query)
        cls.commit_sql()

        query = cls.create_table_exection_query(
            PROPERTY_FILTER_TABLE_NAME,
            PROPERTY_FILTER_TABLE_HEADER,
            PROPERTY_FILTER_TABLE_DATATYPES,
        )
        cursor.execute(query)
        cls.commit_sql()

    @classmethod
    def fill_filter_table(cls, project: SOMcreator.SOMProject):
        def add_table_entry(entity: SOMcreator.UseCase | SOMcreator.Phase):
            cursor = cls.get_cursor()
            headers = ",".join(FILTER_TABLE_HEADER)
            values = (entity.name, entity.description, entity.filter_type)
            query = f"INSERT INTO {FILTER_TABLE_NAME} ({headers})  VALUES (?,?,?)"
            cursor.execute(query, values)
            cls.commit_sql()

        for usecase in project.get_usecases():
            add_table_entry(usecase)
        for phase in project.get_phases():
            add_table_entry(phase)

    @classmethod
    def fill_property_filter_table(cls, values: list[tuple[str, str, str, str]]):
        headers = ",".join(PROPERTY_FILTER_TABLE_HEADER)
        query = (
            f"INSERT INTO {PROPERTY_FILTER_TABLE_NAME} ({headers})  VALUES (?,?,?,?)"
        )
        cursor = cls.get_cursor()
        cursor.executemany(query, values)
        cls.commit_sql()

    @classmethod
    def fill_som_properties(
        cls, values: list[tuple[str, str, str, str, str, str, str]]
    ):
        headers = ",".join(SOM_TABLE_HEADER)
        query = f"INSERT INTO {SOM_TABLE_NAME} ({headers})  VALUES (?,?,?,?,?,?,?)"
        cursor = cls.get_cursor()
        cursor.executemany(query, values)
        cls.commit_sql()

    @classmethod
    def add_properties_to_filter_table(
        cls, project: SOMcreator.SOMProject, som_property: SOMcreator.SOMProperty
    ):
        use_case_list = project.get_usecases()
        phase_list = project.get_phases()
        table = []
        for use_case in use_case_list:
            for phase in phase_list:
                state = som_property.get_filter_state(phase, use_case)
                state = 1 if state is None else int(state)
                table.append(
                    (
                        str(som_property.uuid),
                        str(use_case.name),
                        str(phase.name),
                        str(state),
                    )
                )
        return table

    @classmethod
    def init_database(cls, db_path: str):
        cls.set_database_path(db_path)
        logging.info(f"Database: {db_path}")
        cls.connect_to_data_base(db_path)
        cls.create_tables()
        cls.disconnect_from_database()

    @classmethod
    def get_property_data(cls, som_property: SOMcreator.SOMProperty):
        identifier = som_property.property_set.som_class.ident_value
        propertyset = som_property.property_set.name
        prop_name = som_property.name
        valuetype = som_property.value_type
        datatype = som_property.data_type
        return identifier, propertyset, prop_name, valuetype, datatype

    @classmethod
    def add_property_without_value(cls, som_property: SOMcreator.SOMProperty):
        identifier, propertyset, prop_name, valuetype, datatype = cls.get_property_data(
            som_property
        )
        return (
            som_property.uuid,
            propertyset,
            prop_name,
            None,
            valuetype,
            datatype,
            identifier,
        )

    @classmethod
    def add_property_with_value(cls, som_property: SOMcreator.SOMProperty):
        identifier, propertyset, prop_name, valuetype, datatype = cls.get_property_data(
            som_property
        )
        table = [
            (
                som_property.uuid,
                propertyset,
                prop_name,
                value,
                valuetype,
                datatype,
                identifier,
            )
            for value in som_property.allowed_values
        ]
        return table

    @classmethod
    def add_entity(
        cls,
        entity: ifcopenshell.entity_instance,
        main_pset: str,
        main_property: str,
        file_name,
    ):
        cursor = cls.get_cursor()
        identifier = ifc_element_util.get_pset(entity, main_pset, main_property) or ""
        entity_guid = entity.GlobalId
        entity_guid_zw = tool.Util.transform_guid(entity_guid, True)

        values = (
            entity_guid_zw,
            entity_guid,
            entity.Name,
            entity.is_a(),
            file_name,
            identifier,
        )
        headers = ",".join(ENTITY_TABLE_HEADER)
        text = f'INSERT INTO {ENTITY_TABLE_NAME} ({headers}) VALUES ({",".join("?" for _ in ENTITY_TABLE_HEADER)})'
        try:
            cursor.execute(text, values)
        except sqlite3.IntegrityError:
            logging.info(f"GUID '{entity_guid}' exists for multiple Entities! ")
        cls.commit_sql()
        return identifier

    @classmethod
    def import_entity_properties(
        cls,
        entity: ifcopenshell.entity_instance,
        ifc_file: ifcopenshell.file,
        identifier,
        existing_object_dict,
    ):
        # build query
        cursor = cls.get_cursor()
        headers = ",".join(PROPERTY_TABLE_HEADER)
        value_requests = ",".join("?" for _ in PROPERTY_TABLE_HEADER)
        query = (
            f"INSERT INTO {PROPERTY_TABLE_NAME} ({headers}) VALUES ({value_requests})"
        )
        # iterate over all properties of entity
        pset_dict = ifc_element_util.get_psets(entity, verbose=True)
        entity_guid = entity.GlobalId
        entity_guid_zw = tool.Util.transform_guid(entity_guid, True)
        existing_pset_dict = existing_object_dict.get(identifier)
        for pset_name, property_dict in pset_dict.items():
            existing_property_dict = (
                existing_pset_dict.get(pset_name) if existing_pset_dict else None
            )
            for property_name, value_dict in property_dict.items():

                if not isinstance(value_dict, dict):
                    continue
                value = value_dict.get("value")

                value_id = value_dict.get("id")
                data_type = cls.get_datatype_from_value(ifc_file.by_id(value_id))
                if data_type is None:
                    continue

                if existing_property_dict is None:
                    cs = 0
                elif existing_property_dict.get(property_name) is None:
                    cs = 0
                else:
                    cs = (
                        1
                        if value in existing_property_dict[property_name].allowed_values
                        else 0
                    )

                values = (
                    entity_guid_zw,
                    entity_guid,
                    pset_name,
                    property_name,
                    value,
                    data_type,
                    cs,
                    cs,
                )
                cursor.execute(query, values)
        cls.commit_sql()

    @classmethod
    def get_datatype_from_value(cls, value: ifcopenshell.entity_instance):
        if value.is_a() == "IfcPropertySingleValue":
            if value.NominalValue is None:
                logging.info(f"{value} has undefined Value")
                return None
            return value.NominalValue.is_a()
        logging.info(f"Datatype getter for {value.is_a()} is not defined")
        return None
        # ToDo: add different Value Types

    @classmethod
    def create_settings_filter(cls):
        query = ""
        prop = cls.get_properties()
        if not prop.show_existing_values:
            query += f"AND p.{IS_DEFINED} == 0 \n"
        if not prop.show_boolean_values:
            query += f"AND p.{DATATYPE} is not 'IfcBoolean' \n"
        return query

    @classmethod
    def create_som_filter_table(cls) -> str:

        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {FILTERED_SOM_PROPERTIES_TABLE_NAME};")
        prop = cls.get_properties()

        # JOIN on af.PROPERTY_GUID = sp.GUID
        query = f"""
            CREATE TABLE {FILTERED_SOM_PROPERTIES_TABLE_NAME} AS
            SELECT sp.* from {SOM_TABLE_NAME} as sp
            JOIN {PROPERTY_FILTER_TABLE_NAME} af ON af.{GUID} = sp.{GUID}"""

        filters = list()
        if cls.get_properties().activate_object_filter:
            usecases, phases = cls.get_current_object_filter()
            phase_names = ",".join(f"'{p.name}'" for p in phases)
            usecase_names = ",".join(
                f"'{u.name}'" for u in usecases
            )  # cant't use tuple because it adds comma at the end
            usecase_query = f"af.{USE_CASE}  IN ({usecase_names})"
            phase_query = f"af.{PHASE} IN ({phase_names})"  # af.phase in
            value_query = f" af.{VALUE} = 1"
            filters.append(f"{usecase_query} AND {phase_query}  AND {value_query}")

        if not prop.show_regex_values:
            filters.append(
                f"sp.{VALUE_TYPE} is not '{SOMcreator.value_constants.FORMAT}'"
            )
        if not prop.show_range_values:
            filters.append(
                f"sp.{VALUE_TYPE} is not '{SOMcreator.value_constants.RANGE}'"
            )
        if filters:
            filter_query = "\nAND ".join(filters)
            query += f"\nWHERE {filter_query}"
        query += ";"
        logging.debug(query)
        cursor.execute(query)
        cls.disconnect_from_database()
        return query

    @classmethod
    def get_property_query(cls) -> str:
        identifier_match = f"sp.{IDENTIFIER} = e.{IDENTIFIER}"
        property_set_match = f"p.{PROPERTY_SET} = sp.{PROPERTY_SET}"
        property_match = f"p.{NAME} = sp.{NAME}"
        query = f"""
                FROM {PROPERTY_TABLE_NAME} p
                JOIN {ENTITY_TABLE_NAME} e ON e.{GUID} = p.{GUID}
                JOIN {FILTERED_SOM_PROPERTIES_TABLE_NAME} sp 
                ON {identifier_match} AND {property_set_match} AND {property_match}
                """
        return query

    @classmethod
    def get_wanted_ifc_types(cls):
        logging.debug("request IfcTypes")
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        query = f"""
                SELECT DISTINCT e.{IFCTYPE}
                FROM {ENTITY_TABLE_NAME} e
                WHERE {IDENTIFIER} IS NOT '';
                """
        cursor.execute(query)
        ifc_type_list = cursor.fetchall()
        ifc_type_list = [item[0] for item in ifc_type_list]
        cls.disconnect_from_database()
        return ifc_type_list

    @classmethod
    def get_identifier_types(cls, ifc_type: str, all_keyword: str) -> list[str]:
        logging.debug("Request Identifier")
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()

        ifc_type_filter = (
            "" if ifc_type == all_keyword else f"AND {IFCTYPE} IS '{ifc_type}'"
        )
        query = f"""
                    SELECT DISTINCT e.{IDENTIFIER}
                    FROM {ENTITY_TABLE_NAME} e
                    WHERE e.{IDENTIFIER} IS NOT '' {ifc_type_filter};
                """
        cursor.execute(query)
        identifier_list = cursor.fetchall()
        identifier_list = [item[0] for item in identifier_list]

        cls.disconnect_from_database()
        logging.debug("Request Identifier Done")
        return identifier_list

    @classmethod
    def get_property_sets(
        cls, ifc_type: str, identifier: str | SOMcreator.SOMClass
    ) -> list[tuple[str, int]]:
        logging.debug("Request PropertySets")
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        property_query = cls.get_property_query()
        filter_query = cls.create_settings_filter()
        query = f"""
            SELECT DISTINCT p.{PROPERTY_SET}, COUNT(DISTINCT p.{GUID})
            {property_query}
            WHERE e.{IDENTIFIER} {identifier}
            AND e.{IFCTYPE} {ifc_type}
            AND p.{VALUE} iS NOT NULL
        
            {filter_query}
            GROUP BY p.{PROPERTY_SET};
            """
        logging.debug(f"get property_sets: \n{query}")
        cursor.execute(query)
        pset_list = cursor.fetchall()
        cls.disconnect_from_database()
        logging.debug("Request PropertySets Done")

        return pset_list

    @classmethod
    def get_property_list(
        cls, ifc_type: str, identifier: str | SOMcreator.SOMClass, property_set: str
    ) -> list[tuple[str, int, int]]:
        logging.debug("Request Properties")

        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        property_query = cls.get_property_query()
        filter_query = cls.create_settings_filter()
        query = f"""
            SELECT  DISTINCT p.{NAME}, COUNT(DISTINCT e.{GUID}),COUNT(DISTINCT p.{VALUE})
            {property_query}
            WHERE e.{IDENTIFIER} {identifier}
            AND e.{IFCTYPE} {ifc_type}
            AND p.{PROPERTY_SET} {property_set}
            AND p.{VALUE} iS NOT NULL
            {filter_query}
            GROUP BY p.{NAME} ;
            """
        logging.debug(f"get Properties: \n{query}")
        cursor.execute(query)
        property_list = cursor.fetchall()
        cls.disconnect_from_database()
        logging.debug("Request Done")

        return property_list

    @classmethod
    def get_values(cls, ifc_type, identifier, property_set, property_query: str):
        logging.debug("Request Values")

        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        filter_query = cls.create_settings_filter()
        property_query = cls.get_property_query()
        query = f"""
                SELECT  DISTINCT p.{VALUE}, COUNT(DISTINCT e.{GUID}), p.{CHECKED}, COUNT (DISTINCT p.{CHECKED})
                {property_query}
                WHERE e.{IDENTIFIER} {identifier}
                AND e.{IFCTYPE} {ifc_type}
                AND p.{PROPERTY_SET} {property_set}
                AND p.{NAME} {property_query}
                AND p.{VALUE} IS NOT NULL
                {filter_query}
                GROUP BY p.{VALUE} ;
                """

        logging.debug(f"get Values: \n{query}")
        cursor.execute(query)
        logging.debug("Request Done!")

        value_list = cursor.fetchall()
        cls.disconnect_from_database()

        result_list = list()
        checkstate_dict = dict()
        for value, value_count, check_state, check_count in value_list:
            cs = (
                Qt.CheckState.PartiallyChecked
                if check_count > 1
                else Qt.CheckState.Checked if check_state else Qt.CheckState.Unchecked
            )
            result_list.append((Qt.CheckState, value, value_count))
            checkstate_dict[value] = cs

        return result_list, checkstate_dict

    @classmethod
    def change_checkstate_of_values(
        cls, ifc_type, identifier, property_set, property_query, value_text, checkstate
    ):
        logging.debug("Request Checkstate")

        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()

        query = f"""
                UPDATE {PROPERTY_TABLE_NAME}
                SET {CHECKED} = {checkstate}
                WHERE {GUID} IN (
                    SELECT p.{GUID}
                    from {PROPERTY_TABLE_NAME} p
                    JOIN {ENTITY_TABLE_NAME}  e on p.{GUID} = p.{GUID}
                    WHERE e.{IDENTIFIER} {identifier}
                    AND e.{IFCTYPE} {ifc_type}
                    )        
                AND {PROPERTY_SET} {property_set}
                AND {NAME}  {property_query}
                AND {VALUE} {value_text}
            """
        cursor.execute(query)
        logging.debug("Request Done")

        cls.disconnect_from_database()

    @classmethod
    def count_objects(cls, ifc_type, identifier) -> int:
        logging.debug("Request ObjectCount")

        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        query = f"""
            SELECT count(distinct(e.guid))
            FROM {ENTITY_TABLE_NAME} e
            JOIN {PROPERTY_TABLE_NAME} p ON p.{GUID} = e.{GUID}
            WHERE e.{IDENTIFIER} {identifier}
            AND e.{IFCTYPE} {ifc_type}
            
            """
        cursor.execute(query)
        value_list = cursor.fetchall()
        cls.disconnect_from_database()
        logging.debug("Request Done")

        return value_list[0][0]

    @classmethod
    def get_new_property_values(cls):
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        query = f"""
            
            SELECT DISTINCT sp.{IDENTIFIER},sp.{PROPERTY_SET},sp.{NAME}, p.{VALUE}
            from {SOM_TABLE_NAME} sp
            JOIN {ENTITY_TABLE_NAME} e ON sp.{IDENTIFIER} = e.{IDENTIFIER}
            JOIN {PROPERTY_TABLE_NAME} p ON e.{GUID} = p.{GUID}
            WHERE p.{CHECKED} = 1
            AND p.{NAME} = sp.{NAME}
            AND p.{PROPERTY_SET} = sp.{PROPERTY_SET}
            """

        cursor.execute(query)
        value_list = cursor.fetchall()
        cls.disconnect_from_database()
        return value_list

    @classmethod
    def get_removed_property_values(cls):
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        query = f"""
        
            SELECT DISTINCT sp.{IDENTIFIER},sp.{PROPERTY_SET},sp.{NAME}, p.{VALUE}
            from {SOM_TABLE_NAME} sp
            JOIN {ENTITY_TABLE_NAME} e ON sp.{IDENTIFIER} = e.{IDENTIFIER}
            JOIN {PROPERTY_TABLE_NAME} p ON e.{GUID} = p.{GUID}
            WHERE p.{CHECKED} = 0
            AND p.{IS_DEFINED} = 1
            AND p.{NAME} = sp.{NAME}
            AND p.{PROPERTY_SET} = sp.{PROPERTY_SET}
            
            """

        cursor.execute(query)
        value_list = cursor.fetchall()
        cls.disconnect_from_database()
        return value_list

    @classmethod
    def create_export_query(
        cls,
    ) -> str:
        """
        Create Query to List all Entities with all Properties as Columns
        :return:
        """
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        query = f"SELECT DISTINCT {PROPERTY_SET}, {NAME} FROM {PROPERTY_TABLE_NAME}"
        cursor.execute(query)
        columns = cursor.fetchall()
        cls.disconnect_from_database()
        dyn_column_query = [
            f"MAX(CASE WHEN p.{PROPERTY_SET} = '{p}' AND p.{NAME} = '{n}' THEN p.{VALUE} END) AS '{p}:{n}'"
            for [p, n] in columns
        ]
        query = f"""
        SELECT
            e.{GUID},
            e.{IFCTYPE},
            e.{IDENTIFIER},
            e.{NAME},
            e.{FILE},
            {",".join(dyn_column_query)}
        FROM
            {ENTITY_TABLE_NAME} e
        LEFT JOIN
            {PROPERTY_TABLE_NAME} p
        ON
            e.{GUID} = p.{GUID}
        GROUP BY
            e.{GUID}
        ORDER BY
            e.{NAME};
        """
        return query

    @classmethod
    def sql_to_excel(cls, query, export_path: str):
        # Create a Pandas Excel writer
        cls.connect_to_data_base(cls.get_database_path())
        connection = cls.get_properties().connection
        with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
            # Read the table into a DataFrame
            df = pd.read_sql_query(query, connection)
            # Write the DataFrame to an Excel sheet
            df.to_excel(writer, sheet_name="EXPORT", index=False)
        cls.disconnect_from_database()
