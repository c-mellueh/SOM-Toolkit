from __future__ import annotations  # make own class referencable

import logging
from typing import TYPE_CHECKING

import SOMcreator.constants
import ifcopenshell
from PySide6.QtCore import QThreadPool,Qt
from PySide6.QtWidgets import QWidget, QTableWidgetItem,QTableWidget,QDialog
from PySide6.QtGui import QBrush
from SOMcreator import classes
from ifcopenshell.util.element import get_pset

from ..settings import EXISTING_ATTRIBUTE_IMPORT,RANGE_ATTRIBUTE_IMPORT,REGEX_ATTRIBUTE_IMPORT,COLOR_ATTTRIBUTE_IMPORT
from .. import settings
from . import ifc_mod_window
from ..icons import get_icon,get_settings_icon
from ..ifc_modification.modelcheck import get_identifier

if TYPE_CHECKING:
    from som_gui.main_window import MainWindow

from ..qt_designs import ui_model_control,ui_model_control_settings
STANDARD_CHECK_STATE = False


class ModelControlWindow(QWidget):

    def __init__(self, main_window: MainWindow):
        def create_connections():
            self.widget.button_ifc.clicked.connect(self.ifc_clicked)
            self.widget.line_edit_ifc.returnPressed.connect(lambda: self.import_ifc(self.widget.line_edit_ifc.text()))
            self.widget.button_last.clicked.connect(self.last_object_clicked)
            self.widget.button_next.clicked.connect(self.next_object_clicked)
            self.widget.table_widget_property_set.itemClicked.connect(lambda item:item.activate(self.widget.table_widget_attribute))
            self.widget.table_widget_attribute.itemClicked.connect(lambda item: item.activate(self.widget.table_widget_value))
            self.widget.table_widget_attribute.itemDoubleClicked.connect(self.attribute_double_clicked)
            self.widget.table_widget_value.itemClicked.connect(self.value_item_changed)
            self.widget.check_box_values.clicked.connect(self.toggle_value_checkbox)
            self.widget.button_run.clicked.connect(self.button_run_clicked)
            self.widget.button_settings.clicked.connect(self.settings_clicked)
            self.widget.button_settings.setIcon(get_settings_icon())
            self.widget.button_abort.clicked.connect(self.abort_clicked)
        self.main_window = main_window
        super(ModelControlWindow, self).__init__()
        self.widget = ui_model_control.Ui_Form()
        self.widget.setupUi(self)
        self.show()
        self.setWindowTitle("Modellinformationen Einlesen")
        self.setWindowIcon(get_icon())
        self.thread_pool = QThreadPool()
        self.task_status = 0    #0= not started, 1 = running 2= finished
        self.runner: None | ModelControlRunner = None
        self.widget.label_status.hide()
        self.objects:set[ObjectCollection] = set()
        create_connections()
        ifc_mod_window.set_main_attribute(self.main_window.project, self.widget.line_edit_ident_pset,
                                          self.widget.line_edit_ident_attribute)
        ifc_mod_window.auto_set_ifc_path(self.widget.line_edit_ifc)
        self.widget.progress_bar.hide()
        self._current_index = 0
        self.object_list:list[ObjectCollection] = list()
        self.data_dict = dict()
        self.count_dict = dict()


        self.header_dict={self.widget.table_widget_property_set:["PropertySet","Anzahl"],
                          self.widget.table_widget_attribute:["Attribut","Anzahl","Eindeutig"],
                          self.widget.table_widget_value:["Wert","Anzahl"]}

        self.show_items(False)

    def settings_clicked(self):
        settings_dict = {
            RANGE_ATTRIBUTE_IMPORT:settings.get_setting_attribute_import_range(),
            EXISTING_ATTRIBUTE_IMPORT:settings.get_setting_attribute_import_existing(),
            REGEX_ATTRIBUTE_IMPORT:settings.get_setting_attribute_import_regex(),
            COLOR_ATTTRIBUTE_IMPORT:settings.get_setting_attribute_color()
        }
        self.settings_popup =SettingsDialog(settings_dict)
        val = self.settings_popup.exec()
        if not val:
            return

        for key,value in val.items():
            settings.set_setting(settings.ATTRIBUTE_IMPORT_SECTION, key, value)


    def attribute_double_clicked(self,item:AttributeItem):
        attribute = item.attribute
        property_set = attribute.property_set
        obj = property_set.object
        self.main_window.active_object = obj
        self.main_window.open_pset_window(property_set,self. main_window.active_object, None)
        self.main_window.pset_window.table_clicked(None,attribute)

    @property
    def current_index(self) -> int:
        return self._current_index

    @current_index.setter
    def current_index(self,value) -> None:
        self._current_index = value
        if value == self.max_objects-1:
            self.widget.button_next.setEnabled(False)
            self.widget.button_next.setText("-")
        else:
            self.widget.button_next.setEnabled(True)
            next_index = self._current_index+1
            next_object_name = self.object_list[next_index].object.name
            self.widget.button_next.setText(f"{next_object_name} ({next_index+1}/{self.max_objects})")

        if value == 0:
            self.widget.button_last.setEnabled(False)
            self.widget.button_last.setText("-")
        else:
            last_index = self._current_index - 1
            last_object_name = self.object_list[last_index].object.name
            self.widget.button_last.setEnabled(True)
            self.widget.button_last.setText(f"{last_object_name} ({last_index+1}/{self.max_objects})")

    def button_run_clicked(self):
        if self.task_status == 0:
            path = self.widget.line_edit_ifc.text()
            self.import_ifc(path)
            return
        if self.task_status == 1:
            return

        for obj,property_set_dict in self.data_dict.items():
            for property_set, attribute_dict in property_set_dict.items():
                for attribute,value_dict in attribute_dict.items():
                    attribute:classes.Attribute
                    values = attribute.value
                    for value,[accept_bool,count] in value_dict.items():
                        if value not in values and accept_bool:
                            values.append(value)
                            logging.info(f"Wert {value} wurde fuer {obj.name} -> {property_set.name}:{attribute.name} ergaenzt")
                    attribute.value = values

        self.reset()
        self.hide()

    def reset(self):
        self.show_items(False)
        self.widget.button_run.setText("IFC Einlesen")
        self.task_status = 0

    def toggle_value_checkbox(self):
        check_box = self.widget.check_box_values
        check_box.setTristate(False)
        for row in range(self.widget.table_widget_value.rowCount()):
            item  = self.widget.table_widget_value.item(row,0)
            item.setCheckState(check_box.checkState())
            self.value_item_changed(item,update_value_checkbox=False)

    def update_value_checkbox(self):
        accept_bool = list()
        for index in range(self.widget.table_widget_value.rowCount()):
            item = self.widget.table_widget_value.item(index,0)
            if item is None:
                continue
            if item.checkState() == Qt.CheckState.Checked:
                accept_bool.append(True)
            else:
                accept_bool.append(False)

        if all(accept_bool):
            check_state = Qt.CheckState.Checked
        elif any(accept_bool):
            check_state= Qt.CheckState.PartiallyChecked
        else:
            check_state = Qt.CheckState.Unchecked

        self.widget.check_box_values.setCheckState(check_state)

    @property
    def max_objects(self) -> int:
        return len(self.object_list)

    def value_item_changed(self,item:ValueItem,update_value_checkbox = True):
        if not isinstance(item,ValueItem):
            return
        attribute = item.parent_item.attribute
        property_set = attribute.property_set
        obj = property_set.object
        if item.checkState() == Qt.CheckState.Checked:
            self.data_dict[obj][property_set][attribute][item.value][0] = True
        else:
            self.data_dict[obj][property_set][attribute][item.value][0] = False
        if update_value_checkbox:
            self.update_value_checkbox()

    def next_object_clicked(self):
        self.display_object_by_index(self.current_index+1)

    def last_object_clicked(self):
        self.display_object_by_index(self.current_index - 1)

    def show_items(self, show_bool: bool) -> None:
        """func_name either 'hide or 'show'"""
        if show_bool:
            func_name = "show"
        else:
            func_name = "hide"

        getattr(self.widget.splitter_tables, func_name)()
        getattr(self.widget.button_next, func_name)()
        getattr(self.widget.button_last, func_name)()
        getattr(self.widget.label_object_name,func_name)()
        getattr(self.widget.label_status, func_name)()
        geometry = self.geometry()
        if show_bool:
            geometry.setHeight(450)
        else:
            geometry.setHeight(100)
            self.resize(geometry.width(), 100)
        self.setGeometry(geometry)

    def ifc_clicked(self):
        path = ifc_mod_window.ifc_file_dialog(self, self.widget.line_edit_ifc)
        if path is None:
            return
        self.import_ifc(path)

    def import_ifc(self, ifc_path: list[str]|str):

        if isinstance(ifc_path,str):
            ifc_path = ifc_path.split(";")

        proj = self.main_window.project
        pset = self.widget.line_edit_ident_pset.text()
        attribute = self.widget.line_edit_ident_attribute.text()

        self.runner = ModelControlRunner(ifc_path, proj, pset, attribute, "ModelControl")
        self.connect_runner(self.runner)
        self.thread_pool.start(self.runner)

    def on_started(self):
        self.task_status = 1
        self.widget.button_run.setEnabled(False)
        self.show_items(False)
        self.widget.progress_bar.show()

    def on_finished(self,value):
        self.task_status = 2
        self.show_items(True)
        self.widget.button_run.setEnabled(True)
        self.widget.button_run.setText("Werte übernehmen")
        self.widget.progress_bar.hide()
        self.widget.label_status.hide()

        if value == ifc_mod_window.ABORT:
            self.abort_clicked()
            return

        self.data_dict = self.runner.data_dict
        self.count_dict = self.runner.count_dict

        objects = [ObjectCollection(obj,self,pset_dict,self.count_dict) for obj,pset_dict in self.data_dict.items()]
        self.object_list = sorted(list(objects),key = lambda obj:obj.name)
        self.display_object_by_index(0)


    def display_object_by_index(self,index:int):
        self.current_index= index
        obj = self.object_list[index]
        self.widget.label_object_name.setText(obj.name)
        self.reset_table(self.widget.table_widget_property_set,)
        self.reset_table(self.widget.table_widget_attribute)
        self.reset_table(self.widget.table_widget_value)
        obj.activate(self.widget.table_widget_property_set)

    def reset_table(self,table:QTableWidget):
        table.clear()
        table.setRowCount(0)
        headers = self.header_dict[table]
        table.setHorizontalHeaderLabels(headers)
        table.setColumnWidth(0,200)

        if table == self.widget.table_widget_attribute:
            self.widget.label_attributes.setText("Attribute")

        if table == self.widget.table_widget_value:
            self.widget.label_value.setText("Werte")

    def update_status(self, value):
        self.widget.label_status.show()
        self.widget.label_status.setText(value)
        logging.info(value)
        pass

    def connect_runner(self, runner: ModelControlRunner):
        runner.signaller.started.connect(self.on_started)
        runner.signaller.finished.connect(self.on_finished)
        runner.signaller.progress.connect(self.widget.progress_bar.setValue)
        runner.signaller.status.connect(self.update_status)


    def abort_clicked(self):

        if self.task_status == 1:
            self.runner.abort()
            self.reset()
        else:
            self.reset()
            self.hide()


class ModelControlRunner(ifc_mod_window.IfcRunner):
    def __init__(self, ifc_paths: list[str] | str, project: classes.Project, main_pset: str, main_attribute: str,
                 function_name: str):

        self.data_dict = dict()
        self.count_dict = dict()

        super(ModelControlRunner, self).__init__(ifc_paths, project, main_pset, main_attribute,
                                                 function_name)

    def run_file_function(self, file_path):
        def is_real_layer(entity:ifcopenshell.entity_instance) -> bool:
            """filter that checks if layer is just grouping layer"""
            def get_parent_groups(internal_entity: ifcopenshell.entity_instance):
                parents = set()
                for rel in getattr(internal_entity, "HasAssignments", []):
                    if rel.is_a("IfcRelAssignsToGroup"):
                        parents.add(rel[6])
                return parents

            def get_layers(internal_entity: ifcopenshell.entity_instance) -> set[int]:
                parent_groups = get_parent_groups(internal_entity)
                layers = set()

                if not parent_groups:
                    layers.add(0)
                    return layers

                for parent in parent_groups:
                    for layer in get_layers(parent):
                        layers.add(layer + 1)

                return layers


            layers = get_layers(entity)
            values = [layer%2==0 for layer in layers]
            if all(values):
                return False
            if any(values):
                logging.warning(f"Gruppenlayer von {entity} kontrollieren!")
            else:
                return True

        def create_data_dict(elements):

            def check_entity(d_dict, entity: ifcopenshell.entity_instance):
                if self.is_aborted:
                    return
                ident = get_identifier(entity, self.main_pset, self.main_attribute)
                obj = bk_dict.get(ident)
                if obj is None:
                    return
                if obj not in d_dict:
                    d_dict[obj] = {}
                if obj not in count_dict:
                    count_dict[obj] = 0
                count_dict[obj]+=1
                for property_set in obj.property_sets:
                    check_property_set(d_dict[obj], property_set, entity)

            def check_property_set(sub_dict, property_set: classes.PropertySet, entity: ifcopenshell.entity_instance):
                pset_name = property_set.name
                ifc_pset_dict = get_pset(entity, pset_name)

                if ifc_pset_dict is None:
                    return

                if property_set not in sub_dict:
                    sub_dict[property_set] = dict()

                if property_set not in count_dict:
                    count_dict[property_set] = 0
                count_dict[property_set] += 1

                for attribute in property_set.attributes:
                    check_attribute(sub_dict[property_set], attribute, ifc_pset_dict)

            def check_attribute(sub_dict, attribute, ifc_pset_dict):
                attribute_name = attribute.name
                value = ifc_pset_dict.get(attribute_name)
                if value is None:
                    return

                check_state = STANDARD_CHECK_STATE
                if value in attribute.value:
                    if add_existing:
                        check_state = True
                    else:
                        return


                if attribute.value_type == SOMcreator.constants.RANGE and not add_range:
                    return

                if attribute.value_type == SOMcreator.constants.FORMAT and not add_regex:
                    return

                if attribute not in sub_dict:
                    sub_dict[attribute] = dict()
                if attribute not in count_dict:
                    count_dict[attribute] = 0
                count_dict[attribute] += 1


                if value not in sub_dict[attribute]:
                    sub_dict[attribute][value] = [check_state,1]
                else:
                    sub_dict[attribute][value][1]+=1

            add_existing = settings.get_setting_attribute_import_existing()
            add_range = settings.get_setting_attribute_import_range()
            add_regex = settings.get_setting_attribute_import_regex()
            dd = dict()
            count_dict = dict()
            element_count = len(elements)

            for index, element in enumerate(elements, start=1):
                if self.is_aborted:
                    return None,None
                if index % 10 == 0:
                    self.signaller.status.emit(f"Check {index}/{element_count}")
                    progress = index / element_count * 100
                    self.signaller.progress.emit(progress)
                check_entity(dd, element)

            return dd,count_dict

        ifc = super(ModelControlRunner, self).run_file_function(file_path)
        entities = ifc.by_type("IfcElement")
        groups = ifc.by_type("IfcGroup")
        groups = list(filter(is_real_layer,groups))
        bk_dict: dict[str, classes.Object] = {obj.ident_value: obj for obj in self.project.objects}
        data_dict,count_dict = create_data_dict(entities + groups)
        if self.is_aborted:
            return
        self.data_dict.update(data_dict)
        self.count_dict.update(count_dict)


class ObjectCollection(object):
    def __init__(self, obj: classes.Object,window:ModelControlWindow,property_set_dict:dict,count_dict:dict):
        self.object = obj
        self.count = count_dict[self.object]
        self.property_set_dict = property_set_dict
        self.count_dict = count_dict
        self.window = window
        super(ObjectCollection, self).__init__()

    @property
    def name(self):
        return f"{self.object.name}   ({self.object.ident_value})   [{self.count}]"

    def activate(self,property_set_table_widget:QTableWidget):
        self.window.reset_table(property_set_table_widget)
        self.window.reset_table(self.window.widget.table_widget_attribute)
        self.window.reset_table(self.window.widget.table_widget_value)
        property_set_table_widget.setRowCount(len(self.property_set_dict))
        for index,(property_set,attribute_dict) in enumerate(self.property_set_dict.items()):
            property_set_table_widget.setItem(index, 0,PropertySetItem(self,property_set,attribute_dict,property_set.name))
            property_set_table_widget.setItem(index, 1,PropertySetItem(self,property_set,attribute_dict,self.count))


class PropertySetItem(QTableWidgetItem):
    def __init__(self,parent_item:ObjectCollection, property_set: classes.PropertySet,attribute_dict,text):
        super(PropertySetItem, self).__init__()
        self.property_set = property_set
        self.parent_item = parent_item
        self.count = self.parent_item.count_dict[self.property_set]
        self.attribute_dict:dict[classes.Attribute,dict] = attribute_dict
        self.setText(str(text))
        self.window:ModelControlWindow = self.parent_item.window

    @property
    def name(self):
        return f"{self.property_set.name}"

    def activate(self,attribute_table_widget:QTableWidget):
        self.window.reset_table(attribute_table_widget)
        self.window.reset_table(self.window.widget.table_widget_value)
        self.window.widget.label_attributes.setText(f"Attribute [{self.property_set.name}]")


        color_cells = settings.get_setting_attribute_color()
        attribute_table_widget.setRowCount(len(self.attribute_dict))
        only_single_attribute_color = QBrush("#f5a9b8")
        all_different_color = QBrush("#5bcffa")

        for row,(attribute,value_dict) in enumerate(sorted(self.attribute_dict.items(),key=lambda x:x[0].name)):
            count = self.parent_item.count_dict[attribute]
            distinct_count = len(value_dict)
            items = list()
            items.append(AttributeItem(self,attribute,value_dict,attribute.name))
            items.append(AttributeItem(self,attribute,value_dict,str(count)))
            items.append(AttributeItem(self,attribute,value_dict,str(distinct_count)))
            for index,item in enumerate(items):
                attribute_table_widget.setItem(row,index,item)

            if count == 1:
                continue
            if distinct_count == 1 and color_cells:
                for item in items:
                    item.setBackground(only_single_attribute_color)

            if distinct_count == count and color_cells:
                for item in items:
                    item.setBackground(all_different_color)


class AttributeItem(QTableWidgetItem):
    def __init__(self,parent_item:PropertySetItem, attribute: classes.Attribute,value_dict,text):
        super(AttributeItem, self).__init__()
        self.attribute = attribute
        self.parent_item = parent_item
        self.value_dict = value_dict
        self.setText(str(text))
        self.window = self.parent_item.window

    def activate(self, value_table_widget: QTableWidget):
        self.window.reset_table(value_table_widget)
        self.window.widget.label_value.setText(f"Werte [{self.attribute.name}]")
        value_table_widget.setRowCount(len(self.value_dict))

        for index,(value,[accept_bool,count]) in enumerate(self.value_dict.items()):
            value_table_widget.setItem(index, 0 ,ValueItem(self,value,accept_bool))
            value_table_widget.setItem(index, 1, QTableWidgetItem(str(count)))

        self.window.update_value_checkbox()


class ValueItem(QTableWidgetItem):
    def __init__(self,parent_item:AttributeItem, value,accept_bool,):
        super(ValueItem, self).__init__()
        self.value = value
        self.setText(f"{value}" )
        self.parent_item = parent_item
        self.window = self.parent_item.window

        if accept_bool:
            self.setCheckState(Qt.CheckState.Checked)
        else:
            self.setCheckState(Qt.CheckState.Unchecked)


class SettingsDialog(QDialog):

    EXISTING = EXISTING_ATTRIBUTE_IMPORT
    REGEX = REGEX_ATTRIBUTE_IMPORT
    RANGE = RANGE_ATTRIBUTE_IMPORT
    COLOR = COLOR_ATTTRIBUTE_IMPORT

    def __init__(self,settings_dict:dict[str,bool]):
        super(SettingsDialog, self).__init__()
        self.widget = ui_model_control_settings.Ui_Dialog()
        self.widget.setupUi(self)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Einstellungen")
        self.check_box_dict = {
            self.EXISTING : self.widget.check_box_existing_attributes,
            self.REGEX: self.widget.check_box_regex,
            self.RANGE: self.widget.check_box_range,
            self.COLOR: self.widget.check_box_color
        }

        for key,check_box in self.check_box_dict.items():
            if settings_dict[key]:
                check_box.setCheckState(Qt.CheckState.Checked)
            else:
                check_box.setCheckState(Qt.CheckState.Unchecked)



    def exec(self) -> dict[str,bool]|int:
        val = super(SettingsDialog, self).exec()
        if not val:
            return val
        settings_dict = dict()
        for key,check_box in self.check_box_dict.items():
            if check_box.checkState() == Qt.CheckState.Checked:
                settings_dict[key] = True
            else:
                settings_dict[key] = False
        return settings_dict


