from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

import som_gui.core.tool
import som_gui
from som_gui.module.attribute_import import ui, trigger
from som_gui import tool
from PySide6.QtWidgets import QComboBox, QPushButton
from PySide6.QtCore import QRunnable, QObject, Signal, QThreadPool
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


class AttributeImport(som_gui.core.tool.AttributeImport):
    @classmethod
    def get_properties(cls) -> AttributeImportProperties:
        return som_gui.AttributeImportProperties

    @classmethod
    def connect_import_buttons(cls):
        trigger.connect_import_buttons(cls.get_properties().run_button, cls.get_properties().abort_button)

    @classmethod
    def get_ifctype_combo_box(cls) -> QComboBox:
        return cls.get_properties().ifc_combobox

    @classmethod
    def get_somtype_combo_box(cls) -> QComboBox:
        return cls.get_properties().som_combobox

    @classmethod
    def update_combobox(cls, combobox: QComboBox, allowed_values: set[str]):
        existing_ifc_types = set(tool.Util.get_combobox_values(combobox))
        add_items = allowed_values.difference(existing_ifc_types)
        delete_items = existing_ifc_types.difference(allowed_values)
        combobox.addItems(list(add_items))
        for item in delete_items:
            combobox.removeItem(combobox.findText(item))
        if add_items or delete_items:
            combobox.model().sort(0)

    @classmethod
    def get_all_keyword(cls) -> str:
        return cls.get_properties().all_keyword

    @classmethod
    def format_somtypes(cls, som_types: set[str], object_list: list[SOMcreator.Object]):
        object_dict = {obj.ident_value: obj.name for obj in object_list}
        return {f"{object_dict.get(som_type)} ({som_type})" for som_type in som_types}

    @classmethod
    def set_ifc_path(cls, path):
        cls.get_properties().ifc_path = path

    @classmethod
    def add_attribute_import_widget_to_window(cls, attribute_import_widget):
        cls.get_window().layout().addWidget(attribute_import_widget)
        attribute_import_widget.hide()

    @classmethod
    def add_ifc_importer_to_window(cls, ifc_importer: IfcImportWidget):
        cls.get_properties().ifc_importer = ifc_importer
        cls.get_properties().ifc_button = ifc_importer.widget.button_ifc
        cls.get_properties().run_button = ifc_importer.widget.button_run
        cls.get_properties().abort_button = ifc_importer.widget.button_close
        cls.get_properties().status_label = ifc_importer.widget.label_status
        cls.get_properties().progress_bar = ifc_importer.widget.progress_bar
        cls.get_window().layout().addWidget(ifc_importer)

    @classmethod
    def is_window_allready_build(cls) -> bool:
        return cls.get_attribute_widget() is not None

    @classmethod
    def get_attribute_widget(cls) -> ui.AttributeImportWidget:
        return cls.get_properties().attribute_import_widget

    @classmethod
    def get_window(cls):
        return cls.get_properties().active_window

    @classmethod
    def create_window(cls) -> ui.AttributeImportWindow:
        prop = cls.get_properties()
        prop.active_window = ui.AttributeImportWindow()
        return prop.active_window

    @classmethod
    def create_import_widget(cls) -> ui.AttributeImportWidget:
        prop = cls.get_properties()
        widget = ui.AttributeImportWidget()
        prop.attribute_import_widget = widget
        prop.ifc_combobox = widget.widget.combo_box_group
        prop.som_combobox = widget.widget.combo_box_name

        return prop.attribute_import_widget

    @classmethod
    def get_ifc_import_widget(cls):
        return cls.get_properties().ifc_importer

    @classmethod
    def connect_buttons(cls, button_list: list[QPushButton]):
        trigger.connect_import_buttons(*button_list)

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
    def set_current_runner(cls, runner) -> AttributeImportRunner:
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
                  ([GUID_ZWC] CHAR(64),[GUID] CHAR(64), [PropertySet] TEXT, [Attribut] TEXT, [Value] Text, [DataType] Text)
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
                 INSERT INTO attributes (GUID_ZWC,GUID,PropertySet,Attribut,Value,DataType)
                VALUES
                ('{entity_guid_zw}','{entity_guid}','{property_set_name}','{attribute_name}','{value}','{data_type}')
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
        if ifc_type == all_keyword:
            cursor.execute('''
                SELECT DISTINCT bauteilKlassifikation
                FROM entities
                WHERE bauteilKlassifikation IS NOT '';
            ''')
            identifier_list = cursor.fetchall()
            identifier_list = [item[0] for item in identifier_list]

        else:
            cursor.execute(f'''
            SELECT DISTINCT bauteilKlassifikation
            FROM entities
            WHERE bauteilKlassifikation IS NOT "" AND ifc_type IS "{ifc_type}";
            ''')
            identifier_list = cursor.fetchall()
            identifier_list = [item[0] for item in identifier_list]

        cls.disconnect_from_database()
        return identifier_list
