from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Type

import ifcopenshell
from PySide6.QtCore import QCoreApplication, Qt

import SOMcreator.constants.value_constants as value_constants
from som_gui.module.property_import.constants import EXPORT_PATH, FILETYPE

if TYPE_CHECKING:
    from som_gui import tool
    from som_gui.tool.ifc_importer import IfcImportRunner
    from som_gui.module.property_import.ui import ValueCheckBox
    from som_gui.tool.property_import import PropertyImportRunner

import time


# DB_PATH = ""


def create_main_menu_actions(
    property_import: Type[tool.PropertyImport], main_window: Type[tool.MainWindow]
):
    from som_gui.module.property_import import trigger

    open_window_action = main_window.add_action(
        "menuModels", "IV", trigger.open_import_window
    )
    property_import.set_action("open_window", open_window_action)


def retranslate_ui(
    property_import: Type[tool.PropertyImport],
    property_import_results: Type[tool.PropertyImportResults],
    util: Type[tool.Util],
):
    open_window_action = property_import.get_action("open_window")
    open_window_action.setText(
        QCoreApplication.translate("PropertyImport", "Import Properties")
    )

    ifc_window = property_import.get_ifc_import_window()
    if ifc_window:
        title = QCoreApplication.translate("PropertyImport", "Import Properties")
        ifc_window.ui.retranslateUi(ifc_window)
        ifc_window.setWindowTitle(util.get_window_title(title))
        ifc_window.ui.file_selector_widget.name = QCoreApplication.translate(
            "PropertyImport", "IFC Path"
        )

    result_window = property_import_results.get_results_window()
    if result_window:
        result_window.ui.retranslateUi(result_window)
        title = QCoreApplication.translate("PropertyImport", "Import Properties")
        result_window.setWindowTitle(util.get_window_title(title))


def open_import_window(
    property_import: Type[tool.PropertyImport],
    property_import_results: Type[tool.PropertyImportResults],
    ifc_importer: Type[tool.IfcImporter],
    project: Type[tool.Project],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    proj = project.get()
    usecases = [proj.get_usecase_by_index(i) for i in proj.active_usecases]
    phases = [proj.get_phase_by_index(i) for i in proj.active_phases]
    property_import_sql.set_current_class_filter(usecases, phases)
    if property_import_results.is_window_allready_build():
        property_import_sql.create_som_filter_table()
        property_import_results.get_results_window().show()
        return

    window = property_import.create_ifc_import_window(ifc_importer.create_importer())
    from som_gui.module.property_import import trigger

    trigger.retranslate_ui()
    window.show()


def ifc_import_run_clicked(
    property_import: Type[tool.PropertyImport],
    ifc_importer: Type[tool.IfcImporter],
    property_import_sql: Type[tool.PropertyImportSQL],
    project: Type[tool.Project],
    util: Type[tool.Util],
):
    ifc_import_widget = property_import.get_ifc_import_window()
    ifc_paths = ifc_importer.get_ifc_paths(ifc_import_widget)
    main_pset_name = ifc_importer.get_main_pset(ifc_import_widget)
    main_property_name = ifc_importer.get_main_property(ifc_import_widget)

    if not ifc_importer.check_inputs(ifc_paths, main_pset_name, main_property_name):
        return

    ifc_importer.clear_progress_bars(ifc_import_widget)
    property_import.reset_abort()

    ifc_importer.set_run_button_enabled(ifc_import_widget, False)
    button_text = QCoreApplication.translate("PropertyImport", "Abort")
    ifc_importer.set_close_button_text(ifc_import_widget, button_text)
    property_import.set_main_pset(main_pset_name)
    property_import.set_main_property(main_property_name)
    pool = ifc_importer.create_thread_pool()
    pool.setMaxThreadCount(3)
    progress_bar = util.create_progressbar()
    ifc_importer.add_progress_bar(ifc_import_widget, progress_bar)

    ifc_importer.set_progressbars_visible(ifc_import_widget, True)
    init_database(progress_bar, property_import, property_import_sql, project, util)
    for path in ifc_paths:
        progress_bar = util.create_progressbar()
        ifc_importer.add_progress_bar(ifc_import_widget, progress_bar)
        runner = property_import.create_import_runner(path, progress_bar)
        property_import.connect_ifc_import_runner(runner)
        status = QCoreApplication.translate("PropertyImport", "Import {}").format(
            os.path.basename(path)
        )
        ifc_importer.set_status(runner, status)
        pool.start(runner)


def init_database(
    progress_bar,
    property_import: Type[tool.PropertyImport],
    property_import_sql: Type[tool.PropertyImportSQL],
    project: Type[tool.Project],
    util: Type[tool.Util],
):
    proj = project.get()
    db_path = util.create_tempfile(".db")
    property_import_sql.init_database(db_path)
    all_properties = list(proj.get_properties(filter=False))

    property_count = len(all_properties)

    status_text = QCoreApplication.translate(
        "PropertyImport", "Import properties from SOM"
    )
    property_table = list()
    filter_table = []

    for index, som_property in enumerate(all_properties):
        if index % 100 == 0:
            util.set_progress(progress_bar, int(index / property_count * 100))
            util.set_status(progress_bar, f"{status_text} {index}/{property_count}")

        if not som_property.property_set.som_class:
            continue
        filter_table += property_import_sql.add_properties_to_filter_table(
            proj, som_property
        )

        if not som_property.allowed_values:
            property_table.append(
                property_import_sql.add_property_without_value(som_property)
            )
        else:
            property_table += property_import_sql.add_property_with_value(som_property)

    property_import_sql.connect_to_data_base(db_path)
    property_import_sql.fill_filter_table(proj)
    property_import_sql.fill_property_filter_table(filter_table)
    property_import_sql.fill_som_properties(property_table)
    property_import_sql.disconnect_from_database()

    util.set_progress(progress_bar, 100)
    util.set_status(progress_bar, f"{status_text} {property_count}/{property_count}")


def abort_clicked():
    pass


def ifc_import_started(
    runner: IfcImportRunner,
    property_import: Type[tool.PropertyImport],
    ifc_importer: Type[tool.IfcImporter],
):
    widget = property_import.get_ifc_import_window()
    ifc_importer.set_progressbars_visible(widget, True)
    ifc_importer.set_status(runner, f"Import '{os.path.basename(runner.path)}'")
    ifc_importer.set_progress(runner, 0)


def ifc_import_finished(
    runner: IfcImportRunner,
    property_import: Type[tool.PropertyImport],
    ifc_importer: Type[tool.IfcImporter],
):
    """
    creates and runs PropertyImport Runnable
    """

    property_import.destroy_import_runner(runner)
    ifc_importer.set_status(
        runner, QCoreApplication.translate("PropertyImport", "Import Done!")
    )
    property_import_runner = property_import.create_property_import_runner(runner)
    property_import.connect_property_import_runner(property_import_runner)
    property_import.get_threadpool().start(property_import_runner)


def start_property_import(
    runner: PropertyImportRunner,
    property_import: Type[tool.PropertyImport],
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
    project: Type[tool.Project],
):
    file = runner.file
    path = runner.path

    pset_name, property_name = (
        property_import.get_main_pset(),
        property_import.get_main_property(),
    )
    property_import_sql.connect_to_data_base(property_import_sql.get_database_path())
    entity_list = list(file.by_type("IfcObject"))
    entity_count = len(entity_list)
    status_text = QCoreApplication.translate(
        "PropertyImport", "Import entity from file:"
    )
    property_dict = property_import_results.build_property_dict(
        list(project.get().get_classes(filter=False))
    )
    for index, entity in enumerate(entity_list):
        if index % 100 == 0:
            property_import.set_status(runner, f"{status_text} {index}/{entity_count}")
            property_import.set_progress(runner, int(index / entity_count * 100))

        identifier = property_import_sql.add_entity(
            entity, pset_name, property_name, os.path.basename(path)
        )
        property_import_sql.import_entity_properties(
            entity, file, identifier, property_dict
        )

    status = QCoreApplication.translate(
        "PropertyImport", "import of '{}' entities done!"
    ).format(runner.path)
    property_import.set_status(runner, status)
    property_import.set_progress(runner, 100)
    property_import_sql.disconnect_from_database()


def property_import_finished(
    property_import: Type[tool.PropertyImport], ifc_importer: Type[tool.IfcImporter]
):
    ifc_import_widget = property_import.get_ifc_import_window()

    if property_import.is_aborted():
        ifc_importer.set_progressbars_visible(ifc_import_widget, False)
        ifc_importer.set_close_button_text(ifc_import_widget, "Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        return

    time.sleep(0.2)
    if property_import.import_is_running() or ifc_importer.import_is_running():
        logging.info(f"Prüfung von Datei abgeschlossen, nächste Datei ist dran.")
    else:
        ifc_importer.set_close_button_text(ifc_import_widget, f"Close")
        ifc_importer.set_run_button_enabled(ifc_import_widget, True)
        property_import.last_import_finished()


def last_import_finished(
    property_import: Type[tool.PropertyImport],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    property_import.get_ifc_import_window().close()
    property_import_sql.create_som_filter_table()
    from ..module.property_import import trigger

    trigger.open_results_window()


def open_results_window(property_import_results: Type[tool.PropertyImportResults]):
    property_import_widget = property_import_results.create_import_window()
    property_import_results.connect_trigger(property_import_widget)
    property_import_widget.show()
    property_import_results.update_results_window()
    property_import_results.get_ifctype_combo_box().setCurrentText(
        property_import_results.get_all_keyword()
    )
    property_import_results.get_somtype_combo_box().setCurrentText(
        property_import_results.get_all_keyword()
    )
    from ..module.property_import import trigger

    trigger.retranslate_ui()
    property_import_results.update_results_window()


def update_results_window(attriubte_import_results: Type[tool.PropertyImportResults]):
    attriubte_import_results.update_results_window()


def update_ifctype_combobox(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
    project: Type[tool.Project],
):
    if property_import_results.is_updating_locked():
        logging.debug(
            f"abort Ifc combobox update because lock: {property_import_results.get_update_lock_reason()}"
        )
        return
    combobox = property_import_results.get_ifctype_combo_box()
    wanted_ifc_types = set(property_import_sql.get_wanted_ifc_types())
    wanted_ifc_types.add(property_import_results.get_all_keyword())
    property_import_results.update_combobox(combobox, wanted_ifc_types)
    update_identifier_combobox(property_import_results, property_import_sql, project)


def update_identifier_combobox(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
    project: Type[tool.Project],
):
    if property_import_results.is_updating_locked():
        logging.debug(
            f"abort Identifiercombobox update because lock: {property_import_results.get_update_lock_reason()}"
        )
        return
    combobox = property_import_results.get_somtype_combo_box()
    ifc_type = property_import_results.get_ifctype_combo_box().currentText()
    class_list = list(project.get().get_classes(filter=False))

    wanted_som_types = set(
        property_import_sql.get_identifier_types(
            ifc_type, property_import_results.get_all_keyword()
        )
    )
    property_import_results.update_som_combobox(combobox, wanted_som_types, class_list)


def update_class_count(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    ifc_type, identifier, property_set, som_property = (
        property_import_results.get_input_variables()
    )
    if None in (ifc_type, identifier):
        return
    class_count = property_import_sql.count_classes(ifc_type, identifier)
    text = QCoreApplication.translate("PropertyImport", "Count: {}").format(class_count)
    property_import_results.set_class_count_label_text(text)


def update_property_set_table(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    logging.debug("Update propertyset table")
    ifc_type, identifier, property_set, som_property = (
        property_import_results.get_input_variables()
    )
    if not (ifc_type is None or identifier is None):
        property_set_list = property_import_sql.get_property_sets(ifc_type, identifier)
        table_widget = property_import_results.get_pset_table()
        property_import_results.update_table_widget(
            set(property_set_list), table_widget, [str, int]
        )
    update_property_table(property_import_results, property_import_sql)


def update_property_table(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    logging.debug("Update Property table")

    table_widget = property_import_results.get_property_table()
    ifc_type, identifier, property_set, som_property = (
        property_import_results.get_input_variables()
    )

    if None in [ifc_type, identifier, property_set]:
        property_import_results.disable_table(table_widget)
    else:
        table_widget.setDisabled(False)
        property_list = property_import_sql.get_properties(
            ifc_type, identifier, property_set
        )
        property_import_results.update_table_widget(
            set(property_list), table_widget, [str, int, int]
        )

    property_import_results.update_property_table_styling()
    update_value_table(property_import_results, property_import_sql)


def update_value_table(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    logging.debug("Update Value table")

    table_widget = property_import_results.get_value_table()
    ifc_type, identifier, property_set, som_property = (
        property_import_results.get_input_variables()
    )

    if None in [ifc_type, identifier, property_set, som_property]:
        property_import_results.disable_table(table_widget)
        property_import_results.get_all_checkbox().setDisabled(True)
        return
    else:
        property_import_results.get_all_checkbox().setDisabled(False)
        table_widget.setDisabled(False)

    value_list, checkstate_dict = property_import_sql.get_values(
        ifc_type, identifier, property_set, som_property
    )
    if not value_list:
        return
    property_import_results.update_table_widget(
        set(value_list), table_widget, [Qt.CheckState, str, int]
    )
    property_import_results.update_valuetable_checkstate(checkstate_dict)
    update_all_checkbox(property_import_results)


def value_checkstate_changed(
    checkbox: ValueCheckBox,
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    logging.debug("Update Value Checkstates")
    if property_import_results.is_updating_locked():
        return
    value_table = property_import_results.get_value_table()
    row = property_import_results.find_checkbox_row_in_table(value_table, checkbox)

    if value_table.item(row, 1) is None:
        return
    item = value_table.item(row, 1)
    if not item:
        return
    sql_value_text = f"== '{item.text()}'"
    ifc_type, identifier, property_set, som_property = (
        property_import_results.get_input_variables()
    )

    checkstate = property_import_results.checkstate_to_int(checkbox.checkState())
    logging.info(
        f"value_checkstate_changed {row} {checkbox.checkState()} new: {checkstate}"
    )
    logging.info(
        f"checkstate: {checkbox.checkState()} {checkbox} {checkbox.isTristate()}"
    )
    if None in [ifc_type, identifier, property_set, som_property]:
        update_all_checkbox(property_import_results)
        return

    property_import_sql.change_checkstate_of_values(
        ifc_type, identifier, property_set, som_property, sql_value_text, checkstate
    )
    update_all_checkbox(property_import_results)


def update_all_checkbox(property_import_results: Type[tool.PropertyImportResults]):
    logging.debug(f"Update All Checkbox")
    checkstate = property_import_results.calculate_all_checkbox_state()
    if checkstate == property_import_results.get_all_checkbox().checkState():
        return
    if checkstate is None:
        return
    property_import_results.set_all_checkbox_state(checkstate)


def all_checkbox_checkstate_changed(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
):
    if property_import_results.is_updating_locked():
        logging.debug(
            f"abort all_checkbox_change because {property_import_results.get_update_lock_reason()}"
        )
        return

    checkbox = property_import_results.get_all_checkbox()
    checkstate = property_import_results.checkstate_to_int(checkbox.checkState())
    ifc_type, identifier, property_set, som_property = (
        property_import_results.get_input_variables()
    )
    value_text = "IS NOT NULL"
    property_import_sql.change_checkstate_of_values(
        ifc_type, identifier, property_set, som_property, value_text, checkstate
    )

    update_value_table(property_import_results, property_import_sql)


def settings_clicked(
    property_import_results: Type[tool.PropertyImportResults],
    attriubte_import_sql: Type[tool.PropertyImportSQL],
    util: Type[tool.Util],
):
    settings_dialog = attriubte_import_sql.create_settings_window()
    title = QCoreApplication.translate("PropertyImport", "Settings v")
    settings_dialog.setWindowTitle(util.get_window_title(title))
    attriubte_import_sql.update_settins_dialog_checkstates(settings_dialog)
    if settings_dialog.exec():
        attriubte_import_sql.settings_dialog_accepted(settings_dialog)
        attriubte_import_sql.create_som_filter_table()
        property_import_results.update_results_window()


def results_abort_clicked(property_import_results: Type[tool.PropertyImportResults]):
    window = property_import_results.get_results_window()
    window.close()
    property_import_results.remove_results_window()


def import_values_to_som(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
    project: Type[tool.Project],
):
    logging.debug("Start Import")
    proj = project.get()
    new_property_values = property_import_sql.get_new_property_values()
    property_dict = property_import_results.build_property_dict(
        list(proj.get_classes(filter=False))
    )

    for identifier, property_set_name, property_name, value in new_property_values:
        som_property = property_dict[identifier][property_set_name][property_name]
        if som_property.value_type in [value_constants.FORMAT, value_constants.RANGE]:
            continue
        if value not in som_property.allowed_values:
            som_property.allowed_values.append(value)

    removed_values = property_import_sql.get_removed_property_values()
    for identifier, property_set_name, property_name, value in removed_values:
        som_property = property_dict[identifier][property_set_name][property_name]
        som_property.allowed_values.remove(value)
    window = property_import_results.get_results_window()
    window.close()
    property_import_results.remove_results_window()


def export_properties(
    property_import_results: Type[tool.PropertyImportResults],
    property_import_sql: Type[tool.PropertyImportSQL],
    appdata: Type[tool.Appdata],
    popups: Type[tool.Popups],
):
    """
    Create Table of all Entities with all properties as Header
    :param property_import_sql:
    :param appdata:
    :param popups:
    :return:
    """
    old_path = appdata.get_path(EXPORT_PATH)
    title = QCoreApplication.translate("PropertyImport", "Export Property Data")
    new_path = popups.get_save_path(
        FILETYPE, property_import_results.get_results_window(), old_path, title
    )
    if not new_path:
        return
    appdata.set_path(EXPORT_PATH, new_path)
    query = property_import_sql.create_export_query()
    property_import_sql.sql_to_excel(query, new_path)
    text = QCoreApplication.translate("PropertyImport", "Export Done!")
    popups.create_info_popup(text, text)
