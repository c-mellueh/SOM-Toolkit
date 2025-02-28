from __future__ import annotations

from typing import Callable, Iterator, TYPE_CHECKING

from PySide6.QtCore import QObject, QRunnable, Signal

from som_gui import tool
from som_gui.tool.ifc_importer import IfcImportRunner

if TYPE_CHECKING:
    from som_gui.module.modelcheck.prop import ModelcheckProperties
    from som_gui.module.util.ui import Progressbar
import som_gui.core.tool
import SOMcreator
import datetime
import logging
import re
import sqlite3
from ifcopenshell import entity_instance
import ifcopenshell
from som_gui.module.modelcheck.constants import *
from ifcopenshell.util import element as ifc_el
from SOMcreator import value_constants
from som_gui.resources.data import constants
from som_gui.module.modelcheck import trigger
from PySide6.QtCore import QCoreApplication

rev_datatype_dict = {
    str: "IfcText/IfcLabel",
    bool: "IfcBoolean",
    int: "IfcInteger",
    float: "IfcReal",
}


class ModelcheckRunner(QRunnable):
    def __init__(
        self, ifc_file: ifcopenshell.file, path, progressbar: Progressbar = None
    ):
        super().__init__()
        self.file = ifc_file
        self.path = path
        self.signaller = Signaller()
        self.progress_bar: Progressbar | None = progressbar

    def run(self):
        trigger.start_modelcheck(self)
        self.signaller.finished.emit()


class Signaller(QObject):
    finished = Signal()
    status = Signal(str)
    progress = Signal(int)


class Modelcheck(som_gui.core.tool.Modelcheck):
    @classmethod
    def get_file_check_plugins(cls) -> list[Callable]:
        return cls.get_properties().file_check_plugins

    @classmethod
    def get_entity_check_plugins(cls) -> list[Callable]:
        return cls.get_properties().entity_check_plugins

    @classmethod
    def add_file_check_plugin(cls, file_check_func):
        cls.get_properties().file_check_plugins.append(file_check_func)

    @classmethod
    def add_entity_check_plugin(cls, entity_check_func):
        cls.get_properties().entity_check_plugins.append(entity_check_func)

    @classmethod
    def reset_guids(cls):
        cls.get_properties().guids = dict()

    @classmethod
    def increment_checked_items(cls, runner: ModelcheckRunner):
        checked_count = cls.get_object_checked_count()
        object_count = tool.Modelcheck.get_object_count()
        old_progress_value = int(checked_count / object_count * 100)
        new_progress_value = int((checked_count + 1) / object_count * 100)
        cls.set_object_checked_count(checked_count + 1)
        if new_progress_value > old_progress_value:
            cls.set_progress(runner, new_progress_value)

    @classmethod
    def set_status(cls, runner: ModelcheckRunner, text: str):
        runner.signaller.status.emit(text)

    @classmethod
    def set_progress(cls, runner: ModelcheckRunner, value: int):
        runner.signaller.progress.emit(value)

    @classmethod
    def get_element_count(cls) -> int:
        return len(cls.get_properties().group_parent_dict.keys())

    @classmethod
    def entity_should_be_tested(cls, entity: ifcopenshell.entity_instance) -> bool:
        obj = cls.get_object_representation(entity)
        if obj is None:
            return False
        return obj in cls.get_data_dict()

    @classmethod
    def get_object_representation(
        cls, entity: ifcopenshell.entity_instance
    ) -> SOMcreator.SOMClass | None:
        identifier = cls.get_ident_value(entity)
        return cls.get_ident_dict().get(identifier)

    @classmethod
    def build_ident_dict(cls, objects: set[SOMcreator.SOMClass]):
        cls.get_properties().ident_dict = {o.ident_value: o for o in objects}

    @classmethod
    def build_data_dict(
        cls,
        check_state_dict: dict[
            SOMcreator.SOMClass | SOMcreator.PropertySet | SOMcreator.SOMProperty, bool
        ],
    ):
        def iter_objects(objects: Iterator[SOMcreator.SOMClass]):
            for obj in objects:
                if not check_state_dict.get(obj):
                    continue
                for property_set in obj.get_property_sets(filter=False):
                    if not check_state_dict.get(property_set):
                        continue
                    attribute_list = list()
                    for attribute in property_set.get_attributes(filter=False):
                        if not check_state_dict.get(attribute):
                            continue
                        attribute_list.append(attribute)

                    if not attribute_list:
                        continue
                    if obj not in output_data_dict:
                        output_data_dict[obj] = {property_set: attribute_list}
                    else:
                        output_data_dict[obj][property_set] = attribute_list
                iter_objects(obj.get_children(filter=True))

        output_data_dict = dict()
        iter_objects(tool.Project.get_root_objects())
        cls.set_data_dict(output_data_dict)
        return output_data_dict

    @classmethod
    def create_modelcheck_runner(cls, runner: IfcImportRunner) -> ModelcheckRunner:
        return ModelcheckRunner(runner.ifc, runner.path, runner.progress_bar)

    #######################################################################################
    ###############################Modelchecks#############################################
    #######################################################################################

    @classmethod
    def check_values(cls, value, attribute: SOMcreator.SOMProperty):
        check_dict = {
            value_constants.LIST: cls.check_list,
            value_constants.RANGE: cls.check_range,
            value_constants.FORMAT: cls.check_format,
            constants.GER_LIST: cls.check_list,
            constants.GER_VALUE: cls.check_values,
            constants.GER_FORMAT: cls.check_format,
            constants.GER_RANGE: cls.check_range,
        }
        func = check_dict[attribute.value_type]
        func(value, attribute)
        cls.check_datatype(value, attribute)

    @classmethod
    def check_datatype(cls, value, attribute):
        guid = cls.get_active_guid()
        data_type = value_constants.DATATYPE_DICT[attribute.data_type]
        element_type = cls.get_active_element_type()
        if not isinstance(value, data_type):
            cls.datatype_issue(
                guid, attribute, element_type, rev_datatype_dict[type(value)], value
            )

    @classmethod
    def check_format(cls, value, attribute):
        element_type = cls.get_active_element_type()
        guid = cls.get_active_guid()
        is_ok = False
        for form in attribute.value:
            if re.match(form, value) is not None:
                is_ok = True
        if not is_ok:
            cls.format_issue(guid, attribute, value)

    @classmethod
    def check_list(cls, value, attribute):
        if not attribute.value:
            return
        element_type = cls.get_active_element_type()
        guid = cls.get_active_guid()
        if str(value) not in [str(v) for v in attribute.value]:
            cls.list_issue(guid, attribute, element_type, value)

    @classmethod
    def check_range(cls, value, attribute):
        is_ok = False
        element_type = cls.get_active_element_type()
        guid = cls.get_active_guid()
        for possible_range in attribute:
            if min(possible_range) <= value <= max(possible_range):
                is_ok = True
        if not is_ok:
            cls.range_issue(guid, attribute, element_type, value)

    @classmethod
    def check_for_attributes(cls, element, obj: SOMcreator.SOMClass):

        element_type = cls.get_active_element_type()
        guid = cls.get_active_guid()
        data_dict = cls.get_data_dict()
        pset_dict = ifc_el.get_psets(element)

        for property_set in data_dict[obj]:
            pset_name = property_set.name
            if pset_name not in pset_dict:
                cls.property_set_issue(element.GlobalId, pset_name, element_type)
                continue

            for attribute in data_dict[obj][property_set]:
                attribute_name = attribute.name
                if attribute.name not in pset_dict[pset_name]:
                    cls.attribute_issue(
                        element.GlobalId, pset_name, attribute_name, element_type
                    )
                    continue

                value = pset_dict[pset_name][attribute_name]
                if value is None or value == "":
                    cls.empty_value_issue(guid, pset_name, attribute.name, element_type)
                else:
                    cls.check_values(value, attribute)

    ###################################################################################
    ################################ISSUES#############################################
    ###################################################################################

    @classmethod
    def datatype_issue(cls, guid, attribute, element_type, datatype: str, value):

        description = QCoreApplication.translate(
            "Modelcheck", "{} has the wrong Datatype ({} not allowed)"
        )  # {} besitzt den falschen Datentype ({} nicht erlaubt)
        description = description.format(element_type, datatype)
        issue_nr = DATATYPE_ISSUE
        cls.add_issues(guid, description, issue_nr, attribute, value=value)

    @classmethod
    def format_issue(cls, guid, attribute: SOMcreator.SOMProperty, value):
        element_type = cls.get_active_element_type()
        description = QCoreApplication.translate(
            "Modelcheck", '"{}" does not match format Requirement: "{}"'
        )  # f"{element_type} besitzt nicht das richtige Format für {attribute.property_set.name}:{attribute.name}"
        description = description.format(value, "||".join(attribute.value))
        issue_nr = ATTRIBUTE_VALUE_ISSUES
        cls.add_issues(guid, description, issue_nr, attribute, value=value)

    @classmethod
    def list_issue(cls, guid, attribute, element_type, value):
        description = QCoreApplication.translate(
            "Modelcheck", 'Value "{}" is not allowed'
        ).format(
            value
        )  # {element_type} besitzt nicht das richtige Format für {attribute.property_set.name}:{attribute.name}"

        issue_nr = ATTRIBUTE_VALUE_ISSUES
        cls.add_issues(guid, description, issue_nr, attribute, value=value)

    @classmethod
    def range_issue(cls, guid, attribute, element_type, value):
        description = QCoreApplication.translate(
            "Modelcheck", 'Value "{}" is not in allowed range(s)'
        )
        description = description.format(value)
        issue_nr = ATTRIBUTE_VALUE_ISSUES
        cls.add_issues(guid, description, issue_nr, attribute, value=value)

    @classmethod
    def property_set_issue(cls, guid, pset_name, element_type):
        description = QCoreApplication.translate(
            "Modelcheck", '{} does not contain the Propertyset "{}"'
        )
        description = description.format(element_type, pset_name)
        issue_nr = PROPERTY_SET_ISSUE
        cls.add_issues(guid, description, issue_nr, None, pset_name=pset_name)

    @classmethod
    def empty_value_issue(cls, guid, pset_name, attribute_name, element_type):
        description = QCoreApplication.translate(
            "Modelcheck", "{} has an empty Attribute"
        )
        description = description.format(element_type)
        issue_nr = ATTRIBUTE_EXIST_ISSUE
        cls.add_issues(
            guid,
            description,
            issue_nr,
            None,
            pset_name=pset_name,
            attribute_name=attribute_name,
        )

    @classmethod
    def attribute_issue(cls, guid, pset_name, attribute_name, element_type):
        description = QCoreApplication.translate(
            "Modelcheck", '{} is missing the Attribute "{}:{}"'
        )
        description = description.format(element_type, pset_name, attribute_name)
        issue_nr = ATTRIBUTE_EXIST_ISSUE
        cls.add_issues(
            guid,
            description,
            issue_nr,
            None,
            pset_name=pset_name,
            attribute_name=attribute_name,
        )

    @classmethod
    def ident_issue(cls, guid, pset_name, attribute_name):
        element_type = cls.get_active_element_type()
        description = QCoreApplication.translate(
            "Modelcheck", "{} is missing the identifier-Attribute"
        )
        description = description.format(element_type)
        issue_nr = IDENT_ATTRIBUTE_ISSUE
        cls.add_issues(
            guid,
            description,
            issue_nr,
            None,
            pset_name=pset_name,
            attribute_name=attribute_name,
        )

    @classmethod
    def ident_pset_issue(cls, guid, pset_name):
        element_type = cls.get_active_element_type()
        description = QCoreApplication.translate(
            "Modelcheck", "{} is missing die identifier PropertySet"
        )
        description = description.format(element_type)
        issue_nr = IDENT_PROPERTY_SET_ISSUE
        cls.add_issues(guid, description, issue_nr, None, pset_name=pset_name)

    @classmethod
    def ident_unknown(cls, guid, pset_name, attribute_name, value):
        element_type = cls.get_active_element_type()
        description = QCoreApplication.translate(
            "Modelcheck", """{} Value of Identifier ("{}") does not exist in SOM"""
        )
        description = description.format(element_type, value)
        issue_nr = IDENT_ATTRIBUTE_UNKNOWN
        cls.add_issues(
            guid,
            description,
            issue_nr,
            None,
            pset_name=pset_name,
            attribute_name=attribute_name,
            value=value,
        )

    @classmethod
    def guid_issue(cls, guid, file1, file2):
        description = QCoreApplication.translate(
            "Modelcheck", 'GUID exists in File "{}" and"{}"'
        )
        description = description.format(file1, file2)
        issue_nr = GUID_ISSUE
        cls.add_issues(guid, description, issue_nr, None)

    ################
    ###### SQL #####
    ################

    @classmethod
    def init_sql_database(cls, db_path: str) -> str:
        cls.set_database_path(db_path)
        logging.info(f"Database: {db_path}")

        cls.connect_to_data_base(db_path)
        cls.create_tables()
        cls.disconnect_from_data_base()

        return db_path

    @classmethod
    def remove_existing_issues(cls, creation_date):
        cursor = cls.get_cursor()
        project_name = tool.Project.get().name
        file_name = cls.get_ifc_name()

        query = f"""
        DELETE FROM issues
        WHERE short_description in (
        SELECT short_description from issues
        INNER JOIN entities  on issues.GUID = entities.GUID
        where issues.creation_date = '{creation_date}'
        AND entities.Project = '{project_name}'
        AND entities.datei = '{file_name}')
        """
        cursor.execute(query)
        cls.commit_sql()

    @classmethod
    def create_tables(cls):
        cursor = cls.get_cursor()
        # entities
        header_command = ",".join(
            [f"[{h}] {d}" for h, d in zip(ENTITY_TABLE_HEADER, ENTITY_TABLE_DATATYPES)]
        )
        logging.debug(header_command)
        cursor.execute(f""" CREATE TABLE IF NOT EXISTS entities ({header_command})""")
        cls.commit_sql()

        # issues
        header_command = ",".join(
            [f"[{h}] {d}" for h, d in zip(ISSUE_TABLE_HEADER, ISSUE_TABLE_DATATYPES)]
        )
        logging.debug(header_command)
        cursor.execute(
            f"""
                  CREATE TABLE IF NOT EXISTS issues ({header_command})"""
        )
        cls.commit_sql()

    @classmethod
    def add_issues(
        cls,
        guid,
        description,
        issue_type,
        attribute: SOMcreator.SOMProperty,
        pset_name="",
        attribute_name="",
        value="",
    ):
        cursor = cls.get_cursor()
        guid_zw = tool.Util.transform_guid(guid, True)
        date = datetime.date.today()
        if attribute is not None:
            pset_name = attribute.property_set.name
            attribute_name = attribute.name

        issue_headers = str()
        request = f"""INSERT INTO issues {f'({",".join(ISSUE_TABLE_HEADER)})'} VALUES (?,?,?,?,?,?,?,?)"""
        values = (
            guid_zw,
            guid,
            date,
            description,
            issue_type,
            pset_name,
            attribute_name,
            value,
        )
        cursor.execute(request, values)
        cls.commit_sql()

    @classmethod
    def db_create_entity(cls, element: entity_instance, identifier):
        cursor = cls.get_cursor()
        file_name = cls.get_ifc_name()
        project = tool.Project.get().name
        guid_zwc = tool.Util.transform_guid(element.GlobalId, True)
        guid = tool.Util.transform_guid(element.GlobalId, False)
        name = element.Name
        ifc_type = element.is_a()
        center = [0, 0, 0]
        guids = cls.get_guids()
        if guid in guids:
            if file_name != guids[guid]:
                cls.guid_issue(guid, file_name, guids[guid])
            return
        else:
            guids[guid] = file_name
        try:
            values = (
                guid_zwc,
                guid,
                name,
                project,
                ifc_type,
                center[0],
                center[1],
                center[2],
                file_name,
                identifier,
            )
            query = f""" INSERT INTO entities ({",".join(ENTITY_TABLE_HEADER)}) VALUES (?,?,?,?,?,?,?,?,?,?)"""
            cursor.execute(query, values)
            cls.commit_sql()
        except sqlite3.IntegrityError:
            logging.warning("Integrity Error -> Element allready exists")
            pass

    ## Getter and Setter
    @classmethod
    def get_ident_value(
        cls, entity: entity_instance, main_pset_name=None, main_attribute_name=None
    ):
        pset_name = (
            cls.get_main_pset_name() if main_pset_name is None else main_pset_name
        )
        attribute_name = (
            cls.get_main_attribute_name()
            if main_attribute_name is None
            else main_attribute_name
        )
        return ifc_el.get_pset(entity, pset_name, attribute_name)

    @classmethod
    def get_attribute_value(
        cls, entity: entity_instance, pset_name: str, attribute_name: str
    ):
        psets = ifc_el.get_psets(entity)
        pset = psets.get(pset_name)
        if not pset:
            return None
        return pset.get(attribute_name)

    @classmethod
    def is_pset_existing(cls, entity: entity_instance, pset_name: str):
        psets = ifc_el.get_psets(entity)
        return psets.get(pset_name) is not None

    @classmethod
    def is_attribute_existing(
        cls, entity: entity_instance, pset_name: str, attribute_name: str
    ) -> bool:
        psets = ifc_el.get_psets(entity)
        pset = psets.get(pset_name)
        if not pset:
            return False
        return attribute_name in pset

    @classmethod
    def get_active_guid(cls) -> str:
        return cls.get_active_element().GlobalId

    @classmethod
    def get_active_element(cls):
        return cls.get_properties().active_element

    @classmethod
    def set_active_element(cls, element: entity_instance):
        cls.get_properties().active_element = element

    @classmethod
    def get_active_element_type(cls):
        return cls.get_properties().active_element_type

    @classmethod
    def set_active_element_type(cls, value):
        cls.get_properties().active_element_type = value

    @classmethod
    def get_data_dict(cls):
        return cls.get_properties().data_dict

    @classmethod
    def set_data_dict(cls, value):
        cls.get_properties().data_dict = value

    @classmethod
    def get_ident_dict(cls) -> dict:
        return cls.get_properties().ident_dict

    @classmethod
    def get_ifc_name(cls):
        return cls.get_properties().ifc_name

    @classmethod
    def set_ifc_name(cls, value):
        cls.get_properties().ifc_name = value

    @classmethod
    def get_main_attribute_name(cls):
        return cls.get_properties().main_attribute_name

    @classmethod
    def get_main_pset_name(cls):
        return cls.get_properties().main_pset_name

    @classmethod
    def set_main_attribute_name(cls, value: str):
        cls.get_properties().main_attribute_name = value

    @classmethod
    def set_main_pset_name(cls, value: str):
        cls.get_properties().main_pset_name = value

    @classmethod
    def get_guids(cls):
        return cls.get_properties().guids

    @classmethod
    def get_properties(cls) -> ModelcheckProperties:
        return som_gui.ModelcheckProperties

    @classmethod
    def get_database_path(cls) -> str:
        return cls.get_properties().database_path

    @classmethod
    def set_database_path(cls, path: str):
        cls.get_properties().database_path = path

    @classmethod
    def get_object_checked_count(cls) -> int:
        return cls.get_properties().object_checked_count

    @classmethod
    def set_object_checked_count(cls, value: int):
        cls.get_properties().object_checked_count = value

    @classmethod
    def get_object_count(cls) -> int:
        return cls.get_properties().object_count

    @classmethod
    def set_object_count(cls, value: int):
        cls.get_properties().object_count = value

    @classmethod
    def is_aborted(cls):
        return cls.get_properties().abort_modelcheck

    @classmethod
    def abort(cls):
        cls.get_properties().abort_modelcheck = True

    @classmethod
    def reset_abort(cls):
        cls.get_properties().abort_modelcheck = False

    @classmethod
    def connect_to_data_base(cls, path):
        conn = sqlite3.connect(path)
        cls.get_properties().connection = conn

    @classmethod
    def disconnect_from_data_base(cls):
        cls.get_properties().connection.commit()
        cls.get_properties().connection.close()
        cls.get_properties().connection = None

    @classmethod
    def get_cursor(cls):
        return cls.get_properties().connection.cursor()

    @classmethod
    def commit_sql(cls):
        con = cls.get_properties().connection
        if con is None:
            return
        con.commit()
