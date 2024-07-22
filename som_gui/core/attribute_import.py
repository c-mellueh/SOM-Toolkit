from __future__ import annotations
from typing import Type, TYPE_CHECKING
import os
import logging
import ifcopenshell
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.tool.ifc_importer import IfcImportRunner
    from som_gui.module.attribute_import.ui import ValueCheckBox
import time

DB_PATH = ""  # "C:/Users/CHRIST~1/AppData/Local/Temp/tmpxqjw4ehg.db"  # "C:/Users/CHRIST~1/AppData/Local/Temp/tmpqpvbsv88.db"


def open_import_window(attribute_import: Type[tool.AttributeImport],
                       attribute_import_results: Type[tool.AttributeImportResults],
                       attribute_import_sql: Type[tool.AttributeImportSQL], ifc_importer: Type[tool.IfcImporter]):
    # DEBUG
    if DB_PATH:
        open_results_window(attribute_import_results)
        attribute_import_sql.set_database_path(DB_PATH)
        return

    if attribute_import_results.is_window_allready_build():
        attribute_import_results.get_results_window().show()
        return

    window = attribute_import.create_ifc_import_window()
    ifc_import_widget = ifc_importer.create_importer()
    attribute_import.add_ifc_importer_to_window(ifc_import_widget)
    attribute_import.connect_import_buttons()
    window.show()


def ifc_import_run_clicked(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter],
                           attribute_import_sql: Type[tool.AttributeImportSQL], project: Type[tool.Project],
                           util: Type[tool.Util]):
    ifc_import_widget = attribute_import.get_ifc_import_widget()
    ifc_paths = ifc_importer.get_ifc_paths(ifc_import_widget)
    main_pset_name = ifc_importer.get_main_pset(ifc_import_widget)
    main_attribute_name = ifc_importer.get_main_attribute(ifc_import_widget)

    if not ifc_importer.check_inputs(ifc_paths, main_pset_name, main_attribute_name):
        return

    attribute_import.reset_abort()

    ifc_importer.set_run_button_enabled(ifc_import_widget, False)
    ifc_importer.set_close_button_text(ifc_import_widget, "Abbrechen")
    attribute_import.set_main_pset(main_pset_name)
    attribute_import.set_main_attribute(main_attribute_name)
    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)
    ifc_importer.set_progressbar_visible(ifc_import_widget, True)
    ifc_importer.set_progress(ifc_import_widget, 0)
    init_database(attribute_import, attribute_import_sql, project, util)
    for path in ifc_paths:
        ifc_importer.set_status(ifc_import_widget, f"Import '{os.path.basename(path)}'")
        runner = attribute_import.create_import_runner(path)
        attribute_import.connect_ifc_import_runner(runner)
        pool.start(runner)


def init_database(attribute_import: Type[tool.AttributeImport], attribute_import_sql: Type[tool.AttributeImportSQL],
                  project: Type[tool.Project], util: Type[tool.Util]):
    proj = project.get()
    db_path = util.create_tempfile(".db")
    attribute_import_sql.init_database(db_path)
    all_attributes = list(proj.get_all_attributes())
    attribute_count = len(all_attributes)
    attribute_import_sql.connect_to_data_base(db_path)
    status_text = "Attribute aus SOM importieren:"

    for index, attribute in enumerate(all_attributes):
        if index % 100 == 0:
            attribute_import.set_progress(int(index / attribute_count * 100))
            attribute_import.set_status(f"{status_text} {index}/{attribute_count}")

        if not attribute.property_set.object:
            continue

        if not attribute.value:
            attribute_import_sql.add_attribute_without_value(attribute)
        else:
            attribute_import_sql.add_attribute_with_value(attribute)

    attribute_import_sql.disconnect_from_database()
    attribute_import.set_progress(100)
    attribute_import.set_status(f"{status_text} {attribute_count}/{attribute_count}")


def abort_clicked():
    pass


def ifc_import_started(runner, attribute_import: Type[tool.AttributeImport],
                       ifc_importer: Type[tool.IfcImporter]):
    widget = attribute_import.get_ifc_import_widget()
    ifc_importer.set_progressbar_visible(widget, True)
    ifc_importer.set_status(widget, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(widget, 0)


def ifc_import_finished(runner: IfcImportRunner, attribute_import: Type[tool.AttributeImport],
                        ifc_importer: Type[tool.IfcImporter]):
    """
    creates and runs Modelcheck Runnable
    """

    attribute_import.destroy_import_runner(runner)
    ifc_import_widget = attribute_import.get_ifc_import_widget()
    ifc_importer.set_status(ifc_import_widget, f"Import Abgeschlossen")
    attribute_import_runner = attribute_import.create_attribute_import_runner(runner)
    attribute_import.connect_attribute_import_runner(attribute_import_runner)
    attribute_import.set_current_runner(attribute_import_runner)
    attribute_import.get_attribute_import_threadpool().start(attribute_import_runner)


def start_attribute_import(file: ifcopenshell.file, path, attribute_import: Type[tool.AttributeImport],
                           attribute_import_sql: Type[tool.AttributeImportSQL]):
    attribute_import.set_ifc_path(path)
    pset_name, attribute_name = attribute_import.get_main_pset(), attribute_import.get_main_attribute()
    attribute_import_sql.connect_to_data_base(attribute_import_sql.get_database_path())
    entity_list = list(file.by_type("IfcObject"))
    entity_count = len(entity_list)
    status_text = "Entität aus Datei importieren:"
    for index, entity in enumerate(entity_list):
        if index % 100 == 0:
            attribute_import.set_progress(int(index / entity_count * 100))
            attribute_import.set_status(f"{status_text} {index}/{entity_count}")
        attribute_import_sql.add_entity(entity, pset_name, attribute_name, os.path.basename(path))
        attribute_import_sql.import_entity_attributes(entity, file)
    attribute_import_sql.disconnect_from_database()


def attribute_import_finished(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    ifc_import_widget = attribute_import.get_ifc_import_widget()

    if attribute_import.is_aborted():
        ifc_importer.set_progressbar_visible(ifc_import_widget, False)
        ifc_importer.set_close_button_text(ifc_import_widget, "Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        return

    time.sleep(0.2)
    if not attribute_import.attribute_import_is_running():
        ifc_importer.set_close_button_text(ifc_import_widget, f"Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        attribute_import.last_import_finished()
    else:
        logging.info(f"Prüfung von Datei abgeschlossen, nächste Datei ist dran.")


def last_import_finished(attribute_import: Type[tool.AttributeImport],
                         attribute_import_results: Type[tool.AttributeImportResults]):
    attribute_import.get_ifc_import_window().close()
    open_results_window(attribute_import_results)


def open_results_window(attribute_import_results: Type[tool.AttributeImportResults]):
    attribute_import_widget = attribute_import_results.create_attribute_import_window()
    attribute_import_results.connect_update_trigger(attribute_import_widget)
    attribute_import_widget.show()


def update_results_window(attriubte_import_results: Type[tool.AttributeImportResults],
                          attribute_import_sql: Type[tool.AttributeImportSQL]):
    widget = attriubte_import_results.get_results_window().widget
    widget.combo_box_name.repaint()
    widget.combo_box_group.repaint()
    update_property_set_table(attriubte_import_results, attribute_import_sql)
    widget.label_object_count.repaint()
    update_object_count(attriubte_import_results, attribute_import_sql)
    update_all_checkbox(attriubte_import_results)

def update_ifctype_combobox(attribute_import_results: Type[tool.AttributeImportResults],
                            attribute_import_sql: Type[tool.AttributeImportSQL], project: Type[tool.Project]):
    if attribute_import_results.is_updating_locked():
        logging.debug(f"abort Ifc combobox update because lock: {attribute_import_results.get_update_lock_reason()}")
        return
    combobox = attribute_import_results.get_ifctype_combo_box()
    wanted_ifc_types = set(attribute_import_sql.get_wanted_ifc_types())
    wanted_ifc_types.add(attribute_import_results.get_all_keyword())
    attribute_import_results.update_combobox(combobox, wanted_ifc_types)
    update_identifier_combobox(attribute_import_results, attribute_import_sql, project)


def update_identifier_combobox(attribute_import_results: Type[tool.AttributeImportResults],
                               attribute_import_sql: Type[tool.AttributeImportSQL], project: Type[tool.Project]):
    if attribute_import_results.is_updating_locked():
        logging.debug(
            f"abort Identifiercombobox update because lock: {attribute_import_results.get_update_lock_reason()}")
        return
    combobox = attribute_import_results.get_somtype_combo_box()
    ifc_type = attribute_import_results.get_ifctype_combo_box().currentText()
    object_list = list(project.get().get_all_objects())

    wanted_som_types = set(
        attribute_import_sql.get_identifier_types(ifc_type, attribute_import_results.get_all_keyword()))
    attribute_import_results.update_som_combobox(combobox, wanted_som_types, object_list)


def update_object_count(attribute_import_results: Type[tool.AttributeImportResults],
                        attribute_import_sql: Type[tool.AttributeImportSQL]):
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()
    if None in (ifc_type, identifier):
        return
    object_count = attribute_import_sql.count_objects(ifc_type, identifier)
    attribute_import_results.set_object_count_label_text(f"Anzahl: {object_count}")


def update_property_set_table(attribute_import_results: Type[tool.AttributeImportResults],
                              attribute_import_sql: Type[tool.AttributeImportSQL]):
    if attribute_import_results.is_updating_locked():
        return
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()
    if ifc_type is None or identifier is None:
        return
    property_set_list = attribute_import_sql.get_property_sets(ifc_type, identifier)
    table_widget = attribute_import_results.get_pset_table()
    attribute_import_results.update_table_widget(set(property_set_list), table_widget, [str, int])
    update_attribute_table(attribute_import_results, attribute_import_sql)


def update_attribute_table(attribute_import_results: Type[tool.AttributeImportResults],
                           attribute_import_sql: Type[tool.AttributeImportSQL]):
    if attribute_import_results.is_updating_locked():
        return
    table_widget = attribute_import_results.get_attribute_table()
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()

    if None in [ifc_type, identifier, property_set]:
        attribute_import_results.disable_table(table_widget)
        return
    else:
        table_widget.setDisabled(False)

    attribute_list = attribute_import_sql.get_attributes(ifc_type, identifier, property_set)
    attribute_import_results.update_table_widget(set(attribute_list), table_widget, [str, int, int])
    update_value_table(attribute_import_results, attribute_import_sql)


def update_value_table(attribute_import_results: Type[tool.AttributeImportResults],
                       attribute_import_sql: Type[tool.AttributeImportSQL]):
    if attribute_import_results.is_updating_locked():
        return
    table_widget = attribute_import_results.get_value_table()
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()

    if None in [ifc_type, identifier, property_set, attribute]:
        attribute_import_results.disable_table(table_widget)
        attribute_import_results.get_all_checkbox().setDisabled(True)
        return
    else:
        attribute_import_results.get_all_checkbox().setDisabled(False)
        table_widget.setDisabled(False)

    value_list, checkstate_dict = attribute_import_sql.get_values(ifc_type, identifier, property_set, attribute)
    if not value_list:
        return
    attribute_import_results.update_table_widget(set(value_list), table_widget, [Qt.CheckState, str, int])
    attribute_import_results.update_valuetable_checkstate(checkstate_dict)


def value_checkstate_changed(checkbox: ValueCheckBox, attribute_import_results: Type[tool.AttributeImportResults],
                             attribute_import_sql: Type[tool.AttributeImportSQL]):
    if attribute_import_results.is_updating_locked():
        return
    value_table = attribute_import_results.get_value_table()
    row = attribute_import_results.find_checkbox_row_in_table(value_table, checkbox)

    if value_table.item(row, 1) is None:
        return
    value_text = value_table.item(row, 1).text()
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()

    checkstate = attribute_import_results.checkstate_to_int(checkbox.checkState())
    logging.info(f"value_checkstate_changed {row} {checkbox.checkState()} new: {checkstate}")
    logging.info(f"checkstate: {checkbox.checkState()} {checkbox} {checkbox.isTristate()}")
    if None in [ifc_type, identifier, property_set, attribute]:
        return

    sql_value_text = f"== '{value_text}'"

    attribute_import_sql.change_checkstate_of_values(ifc_type, identifier, property_set, attribute, sql_value_text,
                                                     checkstate)

    update_all_checkbox(attribute_import_results)


def update_all_checkbox(attribute_import_results: Type[tool.AttributeImportResults]):
    checkstate = attribute_import_results.calculate_all_checkbox_state()
    if checkstate == attribute_import_results.get_all_checkbox().checkState():
        return
    if checkstate is None:
        return
    attribute_import_results.set_all_checkbox_state(checkstate)


def all_checkbox_checkstate_changed(attribute_import_results: Type[tool.AttributeImportResults],
                                    attribute_import_sql: Type[tool.AttributeImportSQL]):
    if attribute_import_results.is_updating_locked():
        logging.debug(f"abort all_checkbox_change because {attribute_import_results.get_update_lock_reason()}")
        return

    checkbox = attribute_import_results.get_all_checkbox()
    checkstate = attribute_import_results.checkstate_to_int(checkbox.checkState())
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()
    value_text = "IS NOT NULL"
    attribute_import_sql.change_checkstate_of_values(ifc_type, identifier, property_set, attribute, value_text,
                                                     checkstate)

    update_value_table(attribute_import_results, attribute_import_sql)


def results_abort_clicked(attribute_import_results: Type[tool.AttributeImportResults]):
    window = attribute_import_results.get_results_window()
    window.close()


def results_accept_clicked(attribute_import_results: Type[tool.AttributeImportResults],
                           attribute_import_sql: Type[tool.AttributeImportSQL], project: Type[tool.Project]):
    proj = project.get()
    new_attribute_values = attribute_import_sql.get_new_attribute_values()
    attribute_dict = attribute_import_results.build_attribute_dict(list(proj.get_all_objects()))

    for identifier, property_set_name, attribute_name, value in new_attribute_values:
        attribute = attribute_dict[identifier][property_set_name][attribute_name]
        attribute.value.append(value)

    window = attribute_import_results.get_results_window()
    window.close()
