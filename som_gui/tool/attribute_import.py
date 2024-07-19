from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

import som_gui.core.tool
import som_gui
from som_gui.module.attribute_import import ui, trigger
from som_gui import tool
from PySide6.QtWidgets import QComboBox, QTableWidgetItem, QTableWidget, QCheckBox
from PySide6.QtCore import QRunnable, QObject, Signal, QThreadPool, Qt
import ifcopenshell
from ifcopenshell.util import element as ifc_element_util
import logging

if TYPE_CHECKING:
    from som_gui.module.attribute_import.prop import AttributeImportProperties, AttributeImportSQLProperties
    from som_gui.module.ifc_importer.ui import IfcImportWidget
    from som_gui.tool.ifc_importer import IfcImportRunner
import sqlite3


class AttributeImportRunner(QRunnable):
    def __init__(self, runner: IfcImportRunner):
        super().__init__()
        self.file = runner.ifc
        self.path = runner.path
        self.signaller = Signaller()

    def run(self):
        trigger.start_attribute_import(self.file, self.path)
        self.signaller.finished.emit()


class Signaller(QObject):
    finished = Signal()
    status = Signal(str)
    progress = Signal(int)


class AttributeImportResults(som_gui.core.tool.AttributeImport):

    @classmethod
    def get_properties(cls) -> AttributeImportProperties:
        return som_gui.AttributeImportProperties

    @classmethod
    def checkstate_to_int(cls, checkstate: Qt.CheckState) -> int:
        return 1 if checkstate in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked) else 0

    @classmethod
    def get_ifctype_combo_box(cls) -> QComboBox:
        return cls.get_properties().ifc_combobox

    @classmethod
    def get_somtype_combo_box(cls) -> QComboBox:
        return cls.get_properties().som_combobox

    @classmethod
    def connect_update_trigger(cls, attribute_widget: ui.AttributeImportResultWindow):
        widget = attribute_widget.widget
        update_trigger = trigger.update_attribute_import_window
        widget.combo_box_name.currentIndexChanged.connect(update_trigger)
        widget.combo_box_group.currentIndexChanged.connect(update_trigger)
        widget.table_widget_property_set.itemSelectionChanged.connect(trigger.pset_table_selection_changed)
        widget.table_widget_attribute.itemSelectionChanged.connect(trigger.attribute_table_selection_changed)
        widget.table_widget_value.itemSelectionChanged.connect(trigger.value_table_selection_changed)
        cls.get_properties().all_checkbox.checkStateChanged.connect(trigger.all_checkbox_checkstate_changed)
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
            combobox.model().sort(0)
        cls.unlock_updating()

    @classmethod
    def update_som_combobox(cls, combobox: QComboBox, allowed_values: set[str], object_list: list[SOMcreator.Object]):
        cls.lock_updating("SOM ComboBox")
        all_keyword = cls.get_all_keyword()
        object_dict = {obj.ident_value: obj for obj in object_list}
        allowed_objects = set(object_dict.get(v) for v in allowed_values)
        existing_objects = {combobox.itemData(index, Qt.ItemDataRole.UserRole) for index in range(combobox.count()) if
                            combobox.itemText(index) != all_keyword}

        add_items = allowed_objects.difference(existing_objects)
        delete_items = existing_objects.difference(allowed_objects)

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
            combobox.model().sort(0)
        cls.unlock_updating()

    @classmethod
    def get_all_keyword(cls) -> str:
        return cls.get_properties().all_keyword

    @classmethod
    def is_window_allready_build(cls) -> bool:
        return cls.get_results_window() is not None

    @classmethod
    def get_results_window(cls) -> ui.AttributeImportResultWindow:
        return cls.get_properties().attribute_import_window

    @classmethod
    def create_attribute_import_window(cls) -> ui.AttributeImportResultWindow:
        prop = cls.get_properties()
        widget = ui.AttributeImportResultWindow()
        prop.attribute_import_window = widget
        prop.ifc_combobox = widget.widget.combo_box_group
        prop.som_combobox = widget.widget.combo_box_name
        prop.all_checkbox = widget.widget.check_box_values

        return prop.attribute_import_window

    @classmethod
    def get_pset_table(cls) -> ui.PropertySetTable:
        return cls.get_results_window().widget.table_widget_property_set

    @classmethod
    def get_selected_property_set(cls) -> str | None:
        items = cls.get_pset_table().selectedItems()
        if not items:
            return None
        return items[0].text()

    @classmethod
    def get_attribute_table(cls) -> ui.AttributeTable:
        return cls.get_results_window().widget.table_widget_attribute

    @classmethod
    def disable_table(cls, table_widget: QTableWidget):
        table_widget.setRowCount(0)
        table_widget.setDisabled(True)

    @classmethod
    def get_selected_attribute(cls) -> str | None:
        items = cls.get_attribute_table().selectedItems()
        if not items:
            return None
        return items[0].text()

    @classmethod
    def get_value_table(cls) -> ui.ValueTable:
        return cls.get_results_window().widget.table_widget_value

    @classmethod
    def get_value_from_table_row(cls, table_widget: QTableWidget, row: int, data_types: list):
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
            check_item = table_widget.cellWidget(row, 0) if datatypes[0] == Qt.CheckState else table_widget.item(row, 0)
            if check_item is None:
                continue
            existing_values.add(cls.get_value_from_table_row(table_widget, row, datatypes))
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
    def update_table_widget(cls, allowed_values: set[tuple], table_widget: QTableWidget, datatypes: list, ):
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
            check_item = table_widget.cellWidget(row, 0) if datatypes[0] == Qt.CheckState else table_widget.item(row, 0)

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
    def get_value_checkstate_dict(cls, value_list: list[tuple[str, int, int, int]]):
        value_dict = dict()
        for value, value_count, check, check_count in value_list:
            if check_count > 1:
                cs = Qt.CheckState.PartiallyChecked
            else:
                cs = Qt.CheckState.Checked if check == 1 else Qt.CheckState.Unchecked
            value_dict[value] = cs
        return value_dict

    @classmethod
    def find_checkbox_row_in_table(cls, table_widget: QTableWidget, checkbox: ui.ValueCheckBox):
        for row in range(table_widget.rowCount()):
            if table_widget.cellWidget(row, 0) == checkbox:
                return row

    @classmethod
    def get_input_variables(cls):
        all_keyword = cls.get_all_keyword()
        ifc_type = cls.get_ifctype_combo_box().currentText()
        som_object = cls.get_somtype_combo_box().currentData(Qt.ItemDataRole.UserRole)
        if som_object is not None:
            som_object = som_object.ident_value if som_object != all_keyword else all_keyword
        property_set = cls.get_selected_property_set()
        attribute = cls.get_selected_attribute()

        values = [ifc_type, som_object, property_set, attribute]
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
        label = cls.get_results_window().widget.label_object_count
        label.setText(label.tr(text))

    @classmethod
    def calculate_all_checkbox_state(cls) -> Qt.CheckState | None:
        table = cls.get_value_table()
        if table.cellWidget(0, 0) is None:
            return None
        checkstates = {table.cellWidget(row, 0).checkState() for row in range(table.rowCount())}
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

class AttributeImport(som_gui.core.tool.AttributeImport):
    @classmethod
    def get_properties(cls) -> AttributeImportProperties:
        return som_gui.AttributeImportProperties

    @classmethod
    def set_ifc_path(cls, path):
        cls.get_properties().ifc_path = path

    @classmethod
    def connect_import_buttons(cls):
        trigger.connect_import_buttons(cls.get_properties().run_button, cls.get_properties().abort_button)

    @classmethod
    def create_ifc_import_window(cls) -> ui.AttributeImportWindow:
        prop = cls.get_properties()
        prop.ifc_import_window = ui.AttributeImportWindow()
        return prop.ifc_import_window

    @classmethod
    def get_ifc_import_window(cls):
        return cls.get_properties().ifc_import_window

    @classmethod
    def get_ifc_import_widget(cls):
        return cls.get_properties().ifc_importer

    @classmethod
    def add_ifc_importer_to_window(cls, ifc_importer: IfcImportWidget):
        cls.get_properties().ifc_importer = ifc_importer
        cls.get_properties().ifc_button = ifc_importer.widget.button_ifc
        cls.get_properties().run_button = ifc_importer.widget.button_run
        cls.get_properties().abort_button = ifc_importer.widget.button_close
        cls.get_properties().status_label = ifc_importer.widget.label_status
        cls.get_properties().progress_bar = ifc_importer.widget.progress_bar
        cls.get_ifc_import_window().layout().addWidget(ifc_importer)

    @classmethod
    def set_main_pset(cls, main_pset_name: str) -> None:
        cls.get_properties().main_pset = main_pset_name

    @classmethod
    def get_main_pset(cls) -> str:
        return cls.get_properties().main_pset

    @classmethod
    def set_main_attribute(cls, main_attribute_name: str) -> None:
        cls.get_properties().main_attribute = main_attribute_name

    @classmethod
    def get_main_attribute(cls) -> str:
        return cls.get_properties().main_attribute

    @classmethod
    def is_aborted(cls) -> bool:
        return cls.get_properties().import_is_aborted

    @classmethod
    def reset_abort(cls) -> None:
        cls.get_properties().import_is_aborted = False

    @classmethod
    def create_import_runner(cls, ifc_import_path: str) -> QRunnable:
        status_label = cls.get_ifc_import_widget().widget.label_status
        runner = tool.IfcImporter.create_runner(status_label, ifc_import_path)
        cls.get_properties().ifc_import_runners.append(runner)
        return runner

    @classmethod
    def connect_ifc_import_runner(cls, runner) -> None:
        trigger.connect_ifc_import_runner(runner)

    @classmethod
    def destroy_import_runner(cls, runner) -> None:
        cls.get_properties().ifc_import_runners.remove(runner)

    @classmethod
    def create_attribute_import_runner(cls, runner: IfcImportRunner) -> AttributeImportRunner:
        return AttributeImportRunner(runner)

    @classmethod
    def connect_attribute_import_runner(cls, runner: AttributeImportRunner) -> None:
        trigger.connect_attribute_import_runner(runner)

    @classmethod
    def set_current_runner(cls, runner: AttributeImportRunner) -> None:
        cls.get_properties().runner = runner

    @classmethod
    def get_attribute_import_threadpool(cls):
        if cls.get_properties().thread_pool is None:
            tp = QThreadPool()
            cls.get_properties().thread_pool = tp
            tp.setMaxThreadCount(1)
        return cls.get_properties().thread_pool

    @classmethod
    def attribute_import_is_running(cls):
        return cls.get_attribute_import_threadpool().activeThreadCount() > 0

    @classmethod
    def last_import_finished(cls):
        trigger.last_import_finished()

    @classmethod
    def set_progress(cls, value: int):
        cls.get_properties().progress_bar.setValue(value)

    @classmethod
    def set_status(cls, text: str):
        cls.get_properties().status_label.setText(text)


class AttributeImportSQL(som_gui.core.tool.AttributeImportSQL):
    @classmethod
    def get_properties(cls) -> AttributeImportSQLProperties:
        return som_gui.AttributeImportSQLProperties

    @classmethod
    def get_cursor(cls):
        return cls.get_properties().connection.cursor()

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
    def create_tables(cls):
        cursor = cls.get_cursor()
        # entities
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS entities
                  ([GUID_ZWC] CHAR(64) PRIMARY KEY,[GUID] CHAR(64),[Name] CHAR(64), [ifc_type] TEXT,[datei] TEXT,[bauteilKlassifikation] TEXT)
                  ''')
        cls.commit_sql()

        # imported_attributes
        cursor.execute('''
                  CREATE TABLE IF NOT EXISTS attributes
                  ([GUID_ZWC] CHAR(64),[GUID] CHAR(64), [PropertySet] TEXT, [Attribut] TEXT, [Value] Text, [DataType] Text,[Checked] INTEGER)
                  ''')
        cls.commit_sql()

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS som_attributes
          ([bauteilKlassifikation] TEXT, [PropertySet] TEXT, [Attribut] TEXT, [Value] Text,[ValueType] Text,[DataType] Text)
          ''')
        cls.commit_sql()

    @classmethod
    def init_database(cls, db_path: str):
        cls.set_database_path(db_path)
        logging.info(f"Database: {db_path}")

        cls.connect_to_data_base(db_path)
        cls.create_tables()
        cls.disconnect_from_database()

    @classmethod
    def get_attribute_data(cls, attribute: SOMcreator.Attribute):
        bauteilklassifikation = attribute.property_set.object.ident_value
        propertyset = attribute.property_set.name
        attribute_name = attribute.name
        valuetype = attribute.value_type
        datatype = attribute.data_type
        return bauteilklassifikation, propertyset, attribute_name, valuetype, datatype

    @classmethod
    def add_attribute_without_value(cls, attribute: SOMcreator.Attribute):
        cursor = cls.get_cursor()
        bauteilklassifikation, propertyset, attribute_name, valuetype, datatype = cls.get_attribute_data(attribute)
        text = f'''
                      INSERT INTO som_attributes (bauteilKlassifikation,PropertySet,Attribut,Value,ValueType,DataType)
                            VALUES
                            ('{bauteilklassifikation}','{propertyset}','{attribute_name}','','{valuetype}','{datatype}')
                      '''
        cursor.execute(text)
        cls.commit_sql()

    @classmethod
    def add_attribute_with_value(cls, attribute: SOMcreator.Attribute):
        cursor = cls.get_cursor()
        bauteilklassifikation, propertyset, attribute_name, valuetype, datatype = cls.get_attribute_data(attribute)
        for value in attribute.value:
            text = f'''
                          INSERT INTO som_attributes (bauteilKlassifikation,PropertySet,Attribut,Value,ValueType,DataType)
                                VALUES
                                ('{bauteilklassifikation}','{propertyset}','{attribute_name}','{value}','{valuetype}','{datatype}')
                                  '''
            cursor.execute(text)
            cls.commit_sql()

    @classmethod
    def add_entity(cls, entity: ifcopenshell.entity_instance, main_pset: str, main_attribute: str, file_name):
        cursor = cls.get_cursor()
        identifier = ifc_element_util.get_pset(entity, main_pset, main_attribute) or ""
        entity_guid = entity.GlobalId
        entity_guid_zw = tool.Util.transform_guid(entity_guid, True)

        text = f'''
          INSERT INTO entities (GUID_ZWC,GUID,Name,ifc_type,datei,bauteilKlassifikation)
                VALUES
                ('{entity_guid_zw}','{entity_guid}','{entity.Name}','{entity.is_a()}','{file_name}','{identifier}')
                  '''

        try:
            cursor.execute(text)
        except sqlite3.IntegrityError:
            logging.warning(f"GUID '{entity_guid}' exists for multiple Entities! ")
        cls.commit_sql()

    @classmethod
    def import_entity_attributes(cls, entity: ifcopenshell.entity_instance, ifc_file: ifcopenshell.file):

        cursor = cls.get_cursor()
        pset_dict = ifc_element_util.get_psets(entity, verbose=True)
        entity_guid = entity.GlobalId
        entity_guid_zw = tool.Util.transform_guid(entity_guid, True)

        for property_set_name, attribute_dict in pset_dict.items():
            for attribute_name, value_dict in attribute_dict.items():
                if not isinstance(value_dict, dict):
                    continue
                value = value_dict.get("value") or ""
                value_id = value_dict.get("id")
                data_type = cls.get_datatype_from_value(ifc_file.by_id(value_id))
                if data_type is None:
                    continue

                text = f'''
                 INSERT INTO attributes (GUID_ZWC,GUID,PropertySet,Attribut,Value,DataType,Checked)
                VALUES
                ('{entity_guid_zw}','{entity_guid}','{property_set_name}','{attribute_name}','{value}','{data_type}',{0})
                '''
                cursor.execute(text)
        cls.commit_sql()

    @classmethod
    def get_datatype_from_value(cls, value: ifcopenshell.entity_instance):
        if value.is_a() == "IfcPropertySingleValue":
            return value.NominalValue.is_a()
        logging.info(f"Datatype getter for {value.is_a()} is not defined")
        return None
        # ToDo: add different Value Types

    @classmethod
    def get_wanted_ifc_types(cls):
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        cursor.execute('''
            SELECT DISTINCT ifc_type
            FROM entities
            WHERE bauteilKlassifikation IS NOT '';
        ''')
        ifc_type_list = cursor.fetchall()
        ifc_type_list = [item[0] for item in ifc_type_list]
        cls.disconnect_from_database()
        return ifc_type_list

    @classmethod
    def get_identifier_types(cls, ifc_type: str, all_keyword: str) -> list[str]:
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()

        ifc_type_filter = "" if ifc_type == all_keyword else f"AND ifc_type IS '{ifc_type}'"
        sql_query = f'''
                SELECT DISTINCT bauteilKlassifikation
                FROM entities
                WHERE bauteilKlassifikation IS NOT '' {ifc_type_filter};
            '''
        cursor.execute(sql_query)
        identifier_list = cursor.fetchall()
        identifier_list = [item[0] for item in identifier_list]

        cls.disconnect_from_database()
        return identifier_list

    @classmethod
    def get_property_sets(cls, ifc_type: str, identifier: str | SOMcreator.Object) -> list[
        tuple[str, int]]:
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()

        sql_query = f'''
        SELECT DISTINCT attributes.propertyset, COUNT(DISTINCT attributes.GUID)
        FROM attributes
        JOIN entities ON attributes.guid = entities.guid
        WHERE entities.bauteilKlassifikation {identifier}
        AND entities.ifc_type {ifc_type}
        GROUP BY attributes.propertyset;
        '''
        cursor.execute(sql_query)
        pset_list = cursor.fetchall()
        cls.disconnect_from_database()
        return pset_list

    @classmethod
    def get_attributes(cls, ifc_type: str, identifier: str | SOMcreator.Object, property_set: str) -> \
            list[tuple[str, int, int]]:
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()

        sql_query = f"""
        SELECT  DISTINCT attributes.Attribut, COUNT(attributes.Value),COUNT(DISTINCT attributes.Value)
        FROM attributes
        JOIN entities ON attributes.guid = entities.guid
        WHERE entities.bauteilKlassifikation {identifier}
        AND entities.ifc_type {ifc_type}
        AND attributes.PropertySet {property_set}
        GROUP BY attributes.Attribut ;
        """
        cursor.execute(sql_query)
        attribute_list = cursor.fetchall()
        cls.disconnect_from_database()
        return attribute_list

    @classmethod
    def get_values(cls, ifc_type, identifier, property_set, attribute):
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()

        sql_query = f"""
            SELECT  DISTINCT attributes.Value, COUNT(attributes.Value), attributes.Checked, COUNT (DISTINCT attributes.Checked)
            FROM attributes
            JOIN entities ON attributes.guid = entities.guid
            WHERE entities.bauteilKlassifikation {identifier}
            AND entities.ifc_type {ifc_type}
            AND attributes.PropertySet {property_set}
            AND attributes.Attribut {attribute}
            GROUP BY attributes.Value ;
                """

        cursor.execute(sql_query)
        value_list = cursor.fetchall()
        cls.disconnect_from_database()

        result_list = list()
        checkstate_dict = dict()
        for value, value_count, check_state, check_count in value_list:
            cs = Qt.CheckState.PartiallyChecked if check_count > 1 else Qt.CheckState.Checked if check_state else Qt.CheckState.Unchecked
            result_list.append((Qt.CheckState, value, value_count))
            checkstate_dict[value] = cs
        return result_list, checkstate_dict

    @classmethod
    def change_checkstate_of_values(cls, ifc_type, identifier, property_set, attribute, value_text, checkstate):
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()

        sql_query = f"""
        UPDATE attributes
        SET checked = {checkstate}
        WHERE guid IN (
            SELECT attributes.GUID
            from attributes
            JOIN entities on attributes.GUID = entities.GUID
            WHERE entities.bauteilKlassifikation {identifier}
            AND entities.ifc_type {ifc_type}
            
            )        
        AND PropertySet {property_set}
        AND Attribut  {attribute}
        AND Value {value_text}
        """
        cursor.execute(sql_query)
        cls.disconnect_from_database()

    @classmethod
    def count_objects(cls, ifc_type, identifier) -> int:
        cls.connect_to_data_base(cls.get_database_path())
        cursor = cls.get_cursor()
        sql_query = f"""
        SELECT count(distinct(entities.guid))
        FROM entities
        JOIN attributes ON entities.guid = attributes.guid
        WHERE entities.bauteilKlassifikation {identifier}
        AND entities.ifc_type {ifc_type}
        
        """

        cursor.execute(sql_query)
        value_list = cursor.fetchall()
        cls.disconnect_from_database()
        return value_list[0][0]
