from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Type

import ifcopenshell
from PySide6.QtCore import QCoreApplication, Qt

import SOMcreator.constants.value_constants as value_constants
from som_gui.module.attribute_import.constants import EXPORT_PATH,FILETYPE
if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.tool.ifc_importer import IfcImportRunner
    from som_gui.module.attribute_import.ui import ValueCheckBox
    from som_gui.tool.attribute_import import AttributeImportRunner

import time


# DB_PATH = ""

def create_main_menu_actions(attribute_import: Type[tool.AttributeImport], main_window: Type[tool.MainWindow]):
    from som_gui.module.attribute_import import trigger
    open_window_action = main_window.add_action("menuModels", "IV", trigger.open_import_window)
    attribute_import.set_action("open_window", open_window_action)


def retranslate_ui(attribute_import: Type[tool.AttributeImport],
                   attribute_import_results: Type[tool.AttributeImportResults], util: Type[tool.Util]):
    open_window_action = attribute_import.get_action("open_window")
    open_window_action.setText(QCoreApplication.translate("AttributeImport", "Import Values"))

    ifc_window = attribute_import.get_ifc_import_window()
    if ifc_window:
        title = QCoreApplication.translate("AttributeImport", "Import Values")
        ifc_window.ui.retranslateUi(ifc_window)
        ifc_window.setWindowTitle(util.get_window_title(title))
        ifc_window.ui.file_selector_widget.name = QCoreApplication.translate("AttributeImport", "IFC Path")

    result_window = attribute_import_results.get_results_window()
    if result_window:
        result_window.ui.retranslateUi(result_window)
        title = QCoreApplication.translate("AttributeImport", "Import Values")
        result_window.setWindowTitle(util.get_window_title(title))


def open_import_window(attribute_import: Type[tool.AttributeImport],
                       attribute_import_results: Type[tool.AttributeImportResults],
                       ifc_importer: Type[tool.IfcImporter], project: Type[tool.Project],
                       attribute_import_sql: Type[tool.AttributeImportSQL]):
    proj = project.get()
    usecases = [proj.get_usecase_by_index(i) for i in proj.active_usecases]
    phases = [proj.get_phase_by_index(i) for i in proj.active_phases]
    attribute_import_sql.set_current_object_filter(usecases, phases)
    if attribute_import_results.is_window_allready_build():
        attribute_import_sql.create_som_filter_table()
        attribute_import_results.get_results_window().show()
        return

    window = attribute_import.create_ifc_import_window(ifc_importer.create_importer())
    from som_gui.module.attribute_import import trigger
    trigger.retranslate_ui()
    window.show()


def ifc_import_run_clicked(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter],
                           attribute_import_sql: Type[tool.AttributeImportSQL], project: Type[tool.Project],
                           util: Type[tool.Util]):
    ifc_import_widget = attribute_import.get_ifc_import_window()
    ifc_paths = ifc_importer.get_ifc_paths(ifc_import_widget)
    main_pset_name = ifc_importer.get_main_pset(ifc_import_widget)
    main_attribute_name = ifc_importer.get_main_attribute(ifc_import_widget)

    if not ifc_importer.check_inputs(ifc_paths, main_pset_name, main_attribute_name):
        return

    ifc_importer.clear_progress_bars(ifc_import_widget)
    attribute_import.reset_abort()

    ifc_importer.set_run_button_enabled(ifc_import_widget, False)

    button_text = QCoreApplication.translate("AttributeImport", "Abort")
    ifc_importer.set_close_button_text(ifc_import_widget, button_text)
    attribute_import.set_main_pset(main_pset_name)
    attribute_import.set_main_attribute(main_attribute_name)
    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)
    progress_bar = util.create_progressbar()
    ifc_importer.add_progress_bar(ifc_import_widget,progress_bar)

    ifc_importer.set_progressbars_visible(ifc_import_widget, True)
    init_database(progress_bar,attribute_import, attribute_import_sql, project, util)
    for path in ifc_paths:
        progress_bar = util.create_progressbar()
        ifc_importer.add_progress_bar(ifc_import_widget, progress_bar)
        runner = attribute_import.create_import_runner(path,progress_bar)
        attribute_import.connect_ifc_import_runner(runner)
        status = QCoreApplication.translate("AttributeImport", "Import {}").format(os.path.basename(path))
        ifc_importer.set_status(runner, status)
        pool.start(runner)


def init_database(progress_bar,attribute_import: Type[tool.AttributeImport], attribute_import_sql: Type[tool.AttributeImportSQL],
                  project: Type[tool.Project], util: Type[tool.Util]):
    proj = project.get()
    db_path = util.create_tempfile(".db")
    attribute_import_sql.init_database(db_path)
    all_attributes = list(proj.get_attributes(filter=False))

    attribute_count = len(all_attributes)


    status_text = QCoreApplication.translate("AttributeImport", "Import Attributes from SOM")
    attribute_table = list()
    filter_table = []

    for index, attribute in enumerate(all_attributes):
        if index % 100 == 0:
            util.set_progress(progress_bar,int(index / attribute_count * 100))
            util.set_status(progress_bar,f"{status_text} {index}/{attribute_count}")

        if not attribute.property_set.object:
            continue
        filter_table+=attribute_import_sql.add_attribute_to_filter_table(proj, attribute)

        if not attribute.value:
            attribute_table.append(attribute_import_sql.add_attribute_without_value(attribute))
        else:
            attribute_table+=attribute_import_sql.add_attribute_with_value(attribute)

    attribute_import_sql.connect_to_data_base(db_path)
    attribute_import_sql.fill_filter_table(proj)
    attribute_import_sql.fill_attribute_filter_table(filter_table)
    attribute_import_sql.fill_som_attribute(attribute_table)
    attribute_import_sql.disconnect_from_database()

    util.set_progress(progress_bar,100)
    util.set_status(progress_bar,f"{status_text} {attribute_count}/{attribute_count}")


def abort_clicked():
    pass


def ifc_import_started(runner:IfcImportRunner, attribute_import: Type[tool.AttributeImport],
                       ifc_importer: Type[tool.IfcImporter]):
    widget = attribute_import.get_ifc_import_window()
    ifc_importer.set_progressbars_visible(widget, True)
    ifc_importer.set_status(runner, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(runner, 0)


def ifc_import_finished(runner: IfcImportRunner, attribute_import: Type[tool.AttributeImport],
                        ifc_importer: Type[tool.IfcImporter]):
    """
    creates and runs AttributeImport Runnable
    """

    attribute_import.destroy_import_runner(runner)
    ifc_importer.set_status(runner, QCoreApplication.translate("AttributeImport","Import Done!"))
    attribute_import_runner = attribute_import.create_attribute_import_runner(runner)
    attribute_import.connect_attribute_import_runner(attribute_import_runner)
    attribute_import.get_attribute_import_threadpool().start(attribute_import_runner)


def start_attribute_import(runner:AttributeImportRunner, attribute_import: Type[tool.AttributeImport],
                           attribute_import_results: Type[tool.AttributeImportResults],
                           attribute_import_sql: Type[tool.AttributeImportSQL], project: Type[tool.Project]):
    file = runner.file
    path = runner.path


    pset_name, attribute_name = attribute_import.get_main_pset(), attribute_import.get_main_attribute()
    attribute_import_sql.connect_to_data_base(attribute_import_sql.get_database_path())
    entity_list = list(file.by_type("IfcObject"))
    entity_count = len(entity_list)
    status_text =  QCoreApplication.translate("AttributeImport","Import entity from file:")
    attribute_dict = attribute_import_results.build_attribute_dict(list(project.get().get_objects(filter=False)))
    for index, entity in enumerate(entity_list):
        if index % 100 == 0:
            attribute_import.set_status(runner,f"{status_text} {index}/{entity_count}")
            attribute_import.set_progress(runner, int(index / entity_count * 100))

        identifier = attribute_import_sql.add_entity(entity, pset_name, attribute_name, os.path.basename(path))
        attribute_import_sql.import_entity_attributes(entity, file, identifier, attribute_dict)

    status = QCoreApplication.translate("AttributeImport","import of '{}' entities done!").format(runner.path)
    attribute_import.set_status(runner, status)
    attribute_import.set_progress(runner, 100)
    attribute_import_sql.disconnect_from_database()


def attribute_import_finished(attribute_import: Type[tool.AttributeImport], ifc_importer: Type[tool.IfcImporter]):
    ifc_import_widget = attribute_import.get_ifc_import_window()

    if attribute_import.is_aborted():
        ifc_importer.set_progressbars_visible(ifc_import_widget, False)
        ifc_importer.set_close_button_text(ifc_import_widget, "Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        return

    time.sleep(0.2)
    if attribute_import.attribute_import_is_running() or ifc_importer.import_is_running():
        logging.info(f"Prüfung von Datei abgeschlossen, nächste Datei ist dran.")
    else:
        ifc_importer.set_close_button_text(ifc_import_widget, f"Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        attribute_import.last_import_finished()



def last_import_finished(attribute_import: Type[tool.AttributeImport],
                         attribute_import_sql: Type[tool.AttributeImportSQL]):
    attribute_import.get_ifc_import_window().close()
    attribute_import_sql.create_som_filter_table()
    from ..module.attribute_import import trigger
    trigger.open_results_window()


def open_results_window(attribute_import_results: Type[tool.AttributeImportResults]):
    attribute_import_widget = attribute_import_results.create_attribute_import_window()
    attribute_import_results.connect_trigger(attribute_import_widget)
    attribute_import_widget.show()
    attribute_import_results.update_results_window()
    attribute_import_results.get_ifctype_combo_box().setCurrentText(attribute_import_results.get_all_keyword())
    attribute_import_results.get_somtype_combo_box().setCurrentText(attribute_import_results.get_all_keyword())
    from ..module.attribute_import import trigger
    trigger.retranslate_ui()
    attribute_import_results.update_results_window()


def update_results_window(attriubte_import_results: Type[tool.AttributeImportResults]):
    attriubte_import_results.update_results_window()


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
    object_list = list(project.get().get_objects(filter=False))

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
    logging.debug("Update propertyset table")
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()
    if not (ifc_type is None or identifier is None):
        property_set_list = attribute_import_sql.get_property_sets(ifc_type, identifier)
        table_widget = attribute_import_results.get_pset_table()
        attribute_import_results.update_table_widget(set(property_set_list), table_widget, [str, int])
    update_attribute_table(attribute_import_results, attribute_import_sql)


def update_attribute_table(attribute_import_results: Type[tool.AttributeImportResults],
                           attribute_import_sql: Type[tool.AttributeImportSQL]):
    logging.debug("Update Attribute table")

    table_widget = attribute_import_results.get_attribute_table()
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()

    if None in [ifc_type, identifier, property_set]:
        attribute_import_results.disable_table(table_widget)
    else:
        table_widget.setDisabled(False)
        attribute_list = attribute_import_sql.get_attributes(ifc_type, identifier, property_set)
        attribute_import_results.update_table_widget(set(attribute_list), table_widget, [str, int, int])

    attribute_import_results.update_attribute_table_styling()
    update_value_table(attribute_import_results, attribute_import_sql)


def update_value_table(attribute_import_results: Type[tool.AttributeImportResults],
                       attribute_import_sql: Type[tool.AttributeImportSQL]):
    logging.debug("Update Value table")

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
    update_all_checkbox(attribute_import_results)


def value_checkstate_changed(checkbox: ValueCheckBox, attribute_import_results: Type[tool.AttributeImportResults],
                             attribute_import_sql: Type[tool.AttributeImportSQL]):
    logging.debug("Update Value Checkstates")
    if attribute_import_results.is_updating_locked():
        return
    value_table = attribute_import_results.get_value_table()
    row = attribute_import_results.find_checkbox_row_in_table(value_table, checkbox)

    if value_table.item(row, 1) is None:
        return
    sql_value_text = f"== '{value_table.item(row, 1).text()}'"
    ifc_type, identifier, property_set, attribute = attribute_import_results.get_input_variables()

    checkstate = attribute_import_results.checkstate_to_int(checkbox.checkState())
    logging.info(f"value_checkstate_changed {row} {checkbox.checkState()} new: {checkstate}")
    logging.info(f"checkstate: {checkbox.checkState()} {checkbox} {checkbox.isTristate()}")
    if None in [ifc_type, identifier, property_set, attribute]:
        update_all_checkbox(attribute_import_results)
        return

    attribute_import_sql.change_checkstate_of_values(ifc_type, identifier, property_set, attribute, sql_value_text,
                                                     checkstate)
    update_all_checkbox(attribute_import_results)


def update_all_checkbox(attribute_import_results: Type[tool.AttributeImportResults]):
    logging.debug(f"Update All Checkbox")
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


def settings_clicked(attribute_import_results: Type[tool.AttributeImportResults],
                     attriubte_import_sql: Type[tool.AttributeImportSQL], util: Type[tool.Util]):
    settings_dialog = attriubte_import_sql.create_settings_window()
    title = QCoreApplication.translate("AttributeImport", "Settings v")
    settings_dialog.setWindowTitle(util.get_window_title(title))
    attriubte_import_sql.update_settins_dialog_checkstates(settings_dialog)
    if settings_dialog.exec():
        attriubte_import_sql.settings_dialog_accepted(settings_dialog)
        attriubte_import_sql.create_som_filter_table()
        attribute_import_results.update_results_window()


def results_abort_clicked(attribute_import_results: Type[tool.AttributeImportResults]):
    window = attribute_import_results.get_results_window()
    window.close()
    attribute_import_results.remove_results_window()


def results_accept_clicked(attribute_import_results: Type[tool.AttributeImportResults],
                           attribute_import_sql: Type[tool.AttributeImportSQL], project: Type[tool.Project]):
    proj = project.get()
    new_attribute_values = attribute_import_sql.get_new_attribute_values()
    attribute_dict = attribute_import_results.build_attribute_dict(list(proj.get_objects(filter=False)))

    for identifier, property_set_name, attribute_name, value in new_attribute_values:
        attribute = attribute_dict[identifier][property_set_name][attribute_name]
        if attribute.value_type in [value_constants.FORMAT, value_constants.RANGE]:
            continue
        if value not in attribute.value:
            attribute.value.append(value)

    removed_values = attribute_import_sql.get_removed_attribute_values()
    for identifier, property_set_name, attribute_name, value in removed_values:
        attribute = attribute_dict[identifier][property_set_name][attribute_name]
        attribute.value.remove(value)
    window = attribute_import_results.get_results_window()
    window.close()
    attribute_import_results.remove_results_window()

def export_attributes(attribute_import_results:Type[tool.AttributeImportResults] ,attribute_import_sql: Type[tool.AttributeImportSQL],appdata:Type[tool.Appdata],popups:Type[tool.Popups]):
    """
    Create Table of all Entities with all attributes as Header
    :param attribute_import_sql:
    :param appdata:
    :param popups:
    :return:
    """
    old_path = appdata.get_path(EXPORT_PATH)
    title = QCoreApplication.translate("AttributeImport","Export Attribute Data")
    new_path = popups.get_save_path(FILETYPE,old_path,attribute_import_results.get_results_window(),title)
    if not new_path:
        return
    appdata.set_path(EXPORT_PATH, new_path)
    attribute_import_sql.export_data(new_path)
    text = QCoreApplication.translate("AttributeImport","Export Done!")
    popups.create_info_popup(text,text)
