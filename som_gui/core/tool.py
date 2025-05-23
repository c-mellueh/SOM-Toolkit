class Appdata:
    def _get_config(
        self,
    ):
        pass

    def _write_config(self, config_parser):
        pass

    def get_bool_setting(self, section, option, default):
        pass

    def get_float_setting(self, section, option, default):
        pass

    def get_ini_path(
        self,
    ):
        pass

    def get_int_setting(self, section, option, default):
        pass

    def get_list_setting(self, section, option, default):
        pass

    def get_path(self, value):
        pass

    def get_string_setting(self, section, option, default):
        pass

    def set_path(self, path, value):
        pass

    def set_setting(self, section, option, value):
        pass


class Bsdd:
    def add_classes_to_dictionary(self, project):
        pass

    def add_widget_to_toolbox(self, name, widget):
        pass

    def clear_toolbox(
        self,
    ):
        pass

    def create_dictionary_widget(
        self,
    ):
        pass

    def create_window(
        self,
    ):
        pass

    def export_to_json(self, path):
        pass

    def get_action(self, name):
        pass

    def get_dict_presets(
        self,
    ):
        pass

    def get_dictionary(
        self,
    ):
        pass

    def get_dictionary_widget(
        self,
    ):
        pass

    def get_export_path(
        self,
    ):
        pass

    def get_linked_property_name(self, item):
        pass

    def get_open_window_trigger(
        self,
    ):
        pass

    def get_path_line_edit(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_tab_list(
        self,
    ):
        pass

    def get_toolbox(
        self,
    ):
        pass

    def get_window(
        self,
    ):
        pass

    def is_update_blocked(
        self,
    ):
        pass

    def reset_classes(
        self,
    ):
        pass

    def reset_dictionary(
        self,
    ):
        pass

    def reset_properties(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_linked_property_name(self, item, value):
        pass

    def set_tabs(self, tab_list):
        pass

    def transform_project_to_dict(self, proj):
        pass

    def trigger_retranslation(
        self,
    ):
        pass


class Class:
    def add_class_creation_check(self, key, check_function):
        pass

    def check_class_creation_input(self, data_dict):
        pass

    def connect_signals(
        self,
    ):
        pass

    def create_class(self, data_dict, property_set, identifier_property):
        pass

    def delete_class(self, som_class, recursive):
        pass

    def find_property(self, som_class, pset_name, property_name):
        pass

    def get_existing_ident_values(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def group_classes(self, parent, children):
        pass

    def handle_property_issue(self, result):
        pass

    def inherit_property_set_to_all_children(self, som_class, property_set):
        pass

    def is_identifier_allowed(self, identifier, ignore, is_group):
        pass

    def modify_class(self, som_class, data_dict):
        pass

    def set_ident_value(self, som_class, value):
        pass


class ClassInfo:
    def add_classes_infos_add_function(self, key, getter_function):
        pass

    def add_plugin_entry(
        self,
        key,
        layout_name,
        widget_creator,
        index,
        init_value_getter,
        widget_value_getter,
        widget_value_setter,
        test_function,
        value_setter,
    ):
        pass

    def add_plugin_infos_to_class(self, som_class, data_dict):
        pass

    def are_plugin_requirements_met(self, som_class, data_dict):
        pass

    def connect_dialog(self, dialog, predefined_psets):
        pass

    def create_dialog(self, title):
        pass

    def create_ifc_completer(
        self,
    ):
        pass

    def generate_datadict(
        self,
    ):
        pass

    def get_active_class(
        self,
    ):
        pass

    def get_class_infos(
        self,
    ):
        pass

    def get_dialog(
        self,
    ):
        pass

    def get_ifc_mappings(
        self,
    ):
        pass

    def get_mode(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_ui(
        self,
    ):
        pass

    def is_ident_property_valid(self, data_dict):
        pass

    def is_ident_pset_valid(self, data_dict):
        pass

    def is_identifier_unique(self, data_dict):
        pass

    def oi_change_visibility_identifiers(self, hide):
        pass

    def oi_fill_properties(self, mode):
        pass

    def oi_set_ident_value_color(self, color):
        pass

    def oi_set_values(self, data_dict):
        pass

    def remove_plugin_entry(self, key):
        pass

    def reset(
        self,
    ):
        pass

    def set_active_class(self, value):
        pass

    def trigger_class_info_widget(self, mode, som_class):
        pass

    def update_dialog(self, dialog):
        pass

    def update_property_combobox(self, predefined_psets):
        pass


class ClassTree:
    def add_column_to_tree(
        self, tree, name_getter, logical_index, getter_func, setter_func, role
    ):
        pass

    def add_context_menu_entry(
        self, tree, name_getter, function, on_selection, single, multi
    ):
        pass

    def add_tree(self, tree):
        pass

    def clear_context_menu_list(self, tree):
        pass

    def collapse_selection(self, tree):
        pass

    def connect_tree(self, tree):
        pass

    def connect_trigger(
        self,
    ):
        pass

    def create_completer(self, texts, widget):
        pass

    def create_context_menu(self, tree):
        pass

    def delete_selection(self, tree):
        pass

    def expand_selection(self, tree):
        pass

    def expand_to_class(self, tree, som_class):
        pass

    def get_class_from_index(self, index):
        pass

    def get_classes_from_mimedata(self, mime_data):
        pass

    def get_column_list(self, tree):
        pass

    def get_header_names(self, tree):
        pass

    def get_index_from_pos(self, tree, pos):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_selected(self, tree):
        pass

    def get_selected_classes(self, tree):
        pass

    def get_trees(
        self,
    ):
        pass

    def group_classes(self, parent, children):
        pass

    def handle_class_move(self, tree, dropped_on_index):
        pass

    def insert_row_by_class(self, tree, som_class):
        pass

    def is_drop_indication_pos_on_item(self, tree):
        pass

    def remove_column_from_tree(self, tree, column_name):
        pass

    def remove_row_by_class(self, tree, som_class):
        pass

    def remove_tree(self, tree):
        pass

    def reset_tree(self, tree):
        pass

    def resize_tree(self, tree):
        pass

    def set_column_list(self, tree, value):
        pass

    def write_classes_to_mimedata(self, classes, mime_data):
        pass


class CompareProjectSelector:
    def accept_clicked(
        self,
    ):
        pass

    def connect_project_select_dialog(self, dialog):
        pass

    def create_project_select_dialog(
        self,
    ):
        pass

    def fill_project_select_dialog(self, project, open_path):
        pass

    def get_input_layout(
        self,
    ):
        pass

    def get_project_label(
        self,
    ):
        pass

    def get_project_layouts(
        self,
    ):
        pass

    def get_project_select_dialog(
        self,
    ):
        pass

    def get_project_select_path(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def is_current_project_input(
        self,
    ):
        pass

    def set_project_select_path(self, project_path):
        pass

    def toggle_current_project_as_input(
        self,
    ):
        pass


class CompareWindow:
    def add_tab(self, name_getter, widget, init_func, _tool, export_func):
        pass

    def connect_triggers(
        self,
    ):
        pass

    def create_window(
        self,
    ):
        pass

    def get_action(self, name):
        pass

    def get_export_functions(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_tabwidget(
        self,
    ):
        pass

    def get_window(
        self,
    ):
        pass

    def init_tabs(self, project0, project1):
        pass

    def reset(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_projects(self, project1, project2):
        pass


class Console:
    def close_console(
        self,
    ):
        pass

    def create_console(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass


class Exports:
    def create_mapping_script(self, project, name, path):
        pass

    def create_settings_widget(self, names):
        pass

    def export_allplan(self, project, path, name):
        pass

    def export_bookmarks(self, project, path):
        pass

    def export_card_1(self, project, parent_window, path):
        pass

    def export_excel(self, project, path):
        pass

    def export_vestra(self, project, parent_window, path):
        pass

    def get_action(self, name):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_settings_widget(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass


class FilterCompare:
    def add_phase_index_tuple(self, value):
        pass

    def add_use_case_index_tuple(self, value):
        pass

    def append_collumns(self, class_tree, pset_tree_widget):
        pass

    def are_all_filters_identical(self, filter_list):
        pass

    def are_classes_identical(self, class_0, class_1):
        pass

    def are_properties_identical(self, property_0, property_1):
        pass

    def are_psets_identical(self, pset0, pset1):
        pass

    def create_combobox_widget(self, checkstate0, checkstate1):
        pass

    def create_tree_selection_trigger(self, widget):
        pass

    def create_widget(
        self,
    ):
        pass

    def export_class_filter_differences(self, file, property_compare):
        pass

    def export_property_filter_differnces(self, file, property_list):
        pass

    def export_pset_filter_differences(self, file, pset_list, property_compare):
        pass

    def export_write_statechange(self, file, type_name, filter_list, indent):
        pass

    def fill_tree_with_checkstates(self, item):
        pass

    def find_matching_phases(self, proj0, proj1):
        pass

    def find_matching_usecases(self, proj0, proj1):
        pass

    def get_class_tree(
        self,
    ):
        pass

    def get_existing_header_texts(self, tree_widget):
        pass

    def get_filter_list(self, entity0, entity1):
        pass

    def get_match_list(
        self,
    ):
        pass

    def get_phase_list(
        self,
    ):
        pass

    def get_project(self, index):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_usecase_list(
        self,
    ):
        pass

    def get_widget(
        self,
    ):
        pass

    def make_header_wordwrap(self, tree):
        pass

    def reset(
        self,
    ):
        pass

    def set_phase_list(self, phase_list):
        pass

    def set_projects(self, project1, project2):
        pass

    def set_tree_item_column_color(self, item, column, color):
        pass

    def set_usecase_list(self, usecase_list):
        pass

    def style_class_tree(self, item):
        pass


class IfcSchema:
    pass


class IfcImporter:
    def add_progress_bar(self, widget, progress_bar):
        pass

    def check_inputs(self, ifc_paths, main_pset, main_property):
        pass

    def clear_progress_bars(self, widget):
        pass

    def create_importer(
        self,
    ):
        pass

    def create_runner(self, progress_bar, path):
        pass

    def create_thread_pool(
        self,
    ):
        pass

    def get_ifc_paths(self, widget):
        pass

    def get_main_property(self, widget):
        pass

    def get_main_pset(self, widget):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_threadpool(
        self,
    ):
        pass

    def import_is_running(
        self,
    ):
        pass

    def set_close_button_text(self, widget, text):
        pass

    def set_progress(self, runner, value):
        pass

    def set_progressbars_visible(self, widget, visible):
        pass

    def set_run_button_enabled(self, widget, enabled):
        pass

    def set_status(self, runner, status):
        pass


class Language:
    def get_language(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_system_language(
        self,
    ):
        pass

    def get_widget(
        self,
    ):
        pass

    def load_main_translations(self, app, lang_code):
        pass

    def load_plugin_translations(self, plugin_names, app, lang_code):
        pass

    def retranslate_main_ui(
        self,
    ):
        pass

    def retranslate_plugins(self, plugin_names):
        pass

    def set_language(self, code):
        pass

    def set_widget(self, widget):
        pass


class Logging:
    def create_console_handler(
        self,
    ):
        pass

    def create_error_popup(
        self,
    ):
        pass

    def create_file_handler(self, path):
        pass

    def create_popup_handler(self, main_window):
        pass

    def get_custom_formatter(
        self,
    ):
        pass

    def get_log_level(
        self,
    ):
        pass

    def get_logger(
        self,
    ):
        pass

    def get_logging_directory(
        self,
    ):
        pass

    def get_logging_filename(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_settings_widget(
        self,
    ):
        pass

    def get_signaller(
        self,
    ):
        pass

    def set_log_level(self, log_level):
        pass

    def set_logging_directory(self, path, check_if_identical):
        pass

    def set_settings_widget(self, widget):
        pass

    def show_exception_popup(self, exctype, value, tb):
        pass

    def show_popup(self, record, message):
        pass


class MainWindow:
    def add_action(self, parent_name, name, function):
        pass

    def add_submenu(self, parent_name, name):
        pass

    def connect_class_tree(
        self,
    ):
        pass

    def connect_signals(
        self,
    ):
        pass

    def create(self, application):
        pass

    def get(
        self,
    ):
        pass

    def get_action(self, name):
        pass

    def get_active_class(
        self,
    ):
        pass

    def get_active_property_set(
        self,
    ):
        pass

    def get_app(
        self,
    ):
        pass

    def get_class_name_label(
        self,
    ):
        pass

    def get_class_tree(
        self,
    ):
        pass

    def get_menu_bar(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_set_table_widget(
        self,
    ):
        pass

    def get_property_table(
        self,
    ):
        pass

    def get_pset_name_label(
        self,
    ):
        pass

    def get_statusbar(
        self,
    ):
        pass

    def get_ui(
        self,
    ):
        pass

    def hide_console(
        self,
    ):
        pass

    def is_console_visible(
        self,
    ):
        pass

    def remove_action(self, parent_name, action):
        pass

    def remove_submenu(self, parent_name, sub_menu):
        pass

    def request_new_property(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_active_class(self, som_class):
        pass

    def set_status_bar_text(self, text):
        pass

    def set_window_title(self, title):
        pass

    def show_console(
        self,
    ):
        pass

    def toggle_console(
        self,
    ):
        pass


class Mapping:
    def add_class_to_ifc_export_data(self, som_class):
        pass

    def connect_window_triggers(self, window):
        pass

    def create_child(self, entity):
        pass

    def create_export_dict(self, root_classes):
        pass

    def create_window(
        self,
    ):
        pass

    def disable_all_child_entities(self, item, disabled):
        pass

    def fill_class_tree(self, root_classes):
        pass

    def get_action(self, name):
        pass

    def get_checkstate(self, entity):
        pass

    def get_class_tree(
        self,
    ):
        pass

    def get_entity_from_item(self, item):
        pass

    def get_ifc_export_dict(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_pset_tree(
        self,
    ):
        pass

    def get_selected_class(
        self,
    ):
        pass

    def get_window(
        self,
    ):
        pass

    def reset_export_dict(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_checkstate(self, entity, checkstate):
        pass

    def update_tree(self, entities, parent_item, tree):
        pass


class Modelcheck:
    def abort(
        self,
    ):
        pass

    def add_entity_check_plugin(self, entity_check_func):
        pass

    def add_file_check_plugin(self, file_check_func):
        pass

    def add_issues(
        self,
        guid,
        description,
        issue_type,
        som_property,
        pset_name,
        property_name,
        value,
    ):
        pass

    def build_data_dict(self, check_state_dict):
        pass

    def build_ident_dict(self, classes):
        pass

    def check_datatype(self, value, som_property):
        pass

    def check_for_properties(self, element, som_class):
        pass

    def check_format(self, value, som_property):
        pass

    def check_list(self, value, som_property):
        pass

    def check_range(self, value, som_property):
        pass

    def check_values(self, value, som_property):
        pass

    def commit_sql(
        self,
    ):
        pass

    def connect_to_data_base(self, path):
        pass

    def create_modelcheck_runner(self, runner):
        pass

    def create_tables(
        self,
    ):
        pass

    def datatype_issue(self, guid, som_property, element_type, datatype, value):
        pass

    def db_create_entity(self, element, identifier):
        pass

    def disconnect_from_data_base(
        self,
    ):
        pass

    def empty_value_issue(self, guid, pset_name, property_name, element_type):
        pass

    def entity_should_be_tested(self, entity):
        pass

    def format_issue(self, guid, som_property, value):
        pass

    def get_active_element(
        self,
    ):
        pass

    def get_active_element_type(
        self,
    ):
        pass

    def get_active_guid(
        self,
    ):
        pass

    def get_class_checked_count(
        self,
    ):
        pass

    def get_class_count(
        self,
    ):
        pass

    def get_class_representation(self, entity):
        pass

    def get_cursor(
        self,
    ):
        pass

    def get_data_dict(
        self,
    ):
        pass

    def get_database_path(
        self,
    ):
        pass

    def get_element_count(
        self,
    ):
        pass

    def get_entity_check_plugins(
        self,
    ):
        pass

    def get_file_check_plugins(
        self,
    ):
        pass

    def get_guids(
        self,
    ):
        pass

    def get_ident_dict(
        self,
    ):
        pass

    def get_ident_value(self, entity, main_pset_name, main_prop_name):
        pass

    def get_ifc_name(
        self,
    ):
        pass

    def get_main_property_name(
        self,
    ):
        pass

    def get_main_pset_name(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_value(self, entity, pset_name, property_name):
        pass

    def guid_issue(self, guid, file1, file2):
        pass

    def ident_issue(self, guid, pset_name, property_name):
        pass

    def ident_pset_issue(self, guid, pset_name):
        pass

    def ident_unknown(self, guid, pset_name, property_name, value):
        pass

    def increment_checked_items(self, runner):
        pass

    def init_sql_database(self, db_path):
        pass

    def is_aborted(
        self,
    ):
        pass

    def is_property_existing(self, entity, pset_name, property_name):
        pass

    def is_pset_existing(self, entity, pset_name):
        pass

    def list_issue(self, guid, som_property, element_type, value):
        pass

    def property_issue(self, guid, pset_name, property_name, element_type):
        pass

    def property_set_issue(self, guid, pset_name, element_type):
        pass

    def range_issue(self, guid, som_property, element_type, value):
        pass

    def remove_existing_issues(self, creation_date):
        pass

    def reset_abort(
        self,
    ):
        pass

    def reset_guids(
        self,
    ):
        pass

    def set_active_element(self, element):
        pass

    def set_active_element_type(self, value):
        pass

    def set_class_checked_count(self, value):
        pass

    def set_class_count(self, value):
        pass

    def set_data_dict(self, value):
        pass

    def set_database_path(self, path):
        pass

    def set_ifc_name(self, value):
        pass

    def set_main_property_name(self, value):
        pass

    def set_main_pset_name(self, value):
        pass

    def set_progress(self, runner, value):
        pass

    def set_status(self, runner, text):
        pass


class ModelcheckExternal:
    def _build_tree(
        self,
    ):
        pass

    def create_menubar(self, window):
        pass

    def create_window(
        self,
    ):
        pass

    def export_bimcollab(
        self,
    ):
        pass

    def export_desite_csv(
        self,
    ):
        pass

    def export_desite_fast(
        self,
    ):
        pass

    def export_desite_js(
        self,
    ):
        pass

    def export_desite_property_table(
        self,
    ):
        pass

    def export_ids(
        self,
    ):
        pass

    def get_action(self, name):
        pass

    def get_data_dict(
        self,
    ):
        pass

    def get_main_property(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_window(
        self,
    ):
        pass

    def is_window_allready_build(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass


class ModelcheckResults:
    def autofit_column_width(self, worksheet):
        pass

    def create_table(self, worksheet, last_cell):
        pass

    def create_workbook(
        self,
    ):
        pass

    def fill_worksheet(self, issues, ws):
        pass

    def get_export_path(
        self,
    ):
        pass

    def get_header(
        self,
    ):
        pass

    def get_max_width(self, worksheet):
        pass

    def get_properties(
        self,
    ):
        pass

    def last_modelcheck_finished(
        self,
    ):
        pass

    def query_issues(self, path):
        pass

    def set_export_path(self, value):
        pass


class ModelcheckWindow:
    def _update_pset_row(self, item, enabled):
        pass

    def add_progress_bar(self, progress_bar):
        pass

    def autofill_export_path(
        self,
    ):
        pass

    def check_export_path(self, export_path):
        pass

    def check_selection(self, widget):
        pass

    def clear_progress_bars(
        self,
    ):
        pass

    def close_window(
        self,
    ):
        pass

    def collapse_selection(self, widget):
        pass

    def connect_buttons(
        self,
    ):
        pass

    def connect_class_tree(self, tree_widget):
        pass

    def connect_ifc_import_runner(self, runner):
        pass

    def connect_modelcheck_runner(self, runner):
        pass

    def connect_pset_tree(self, tree_widget):
        pass

    def create_class_tree_row(self, som_class):
        pass

    def create_context_menu(self, pos, funcion_list, widget):
        pass

    def create_import_runner(self, progress_bar, ifc_import_path):
        pass

    def create_pset_tree_row(self, entity, parent_item):
        pass

    def create_window(
        self,
    ):
        pass

    def destroy_import_runner(self, runner):
        pass

    def expand_selection(self, widget):
        pass

    def fill_class_tree(self, entities, parent_item, model, tree):
        pass

    def fill_pset_tree(self, property_sets, enabled, tree):
        pass

    def get_action(self, name):
        pass

    def get_class_tree(
        self,
    ):
        pass

    def get_item_check_state(self, item):
        pass

    def get_item_checkstate_dict(
        self,
    ):
        pass

    def get_modelcheck_threadpool(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_pset_tree(
        self,
    ):
        pass

    def get_selected_class(
        self,
    ):
        pass

    def get_selected_items(self, widget):
        pass

    def get_window(
        self,
    ):
        pass

    def is_initial_paint(
        self,
    ):
        pass

    def is_window_allready_build(
        self,
    ):
        pass

    def modelcheck_is_running(
        self,
    ):
        pass

    def read_inputs(
        self,
    ):
        pass

    def reset_butons(
        self,
    ):
        pass

    def resize_class_tree(self, tree):
        pass

    def set_action(self, name, action):
        pass

    def set_item_check_state(self, item, cs):
        pass

    def set_progress(self, runner, value):
        pass

    def set_progress_bar_layout_visible(self, state):
        pass

    def set_progressbar_visible(self, runner, state):
        pass

    def set_pset_tree_title(self, text):
        pass

    def set_selected_class(self, som_class):
        pass

    def set_status(self, runner, status):
        pass

    def show_buttons(self, buttons):
        pass

    def show_pset_tree_title(self, show):
        pass

    def uncheck_selection(self, widget):
        pass

    def update_class_tree_row(self, parent_item, row_index):
        pass


class Plugins:
    def activate_plugin(self, plugin_name):
        pass

    def create_settings_entry(self, plugin_name):
        pass

    def deactivate_plugin(self, plugin_name):
        pass

    def get_available_plugins(
        self,
    ):
        pass

    def get_description(self, name):
        pass

    def get_friendly_name(self, name):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_settings_widget(
        self,
    ):
        pass

    def get_submodules(self, plugin_name):
        pass

    def is_plugin_active(self, plugin_name):
        pass

    def on_new_project(self, plugin_name):
        pass

    def set_plugin_active(self, plugin_name, state):
        pass

    def set_settings_widget(self, widget):
        pass


class Popups:
    def _get_path(self, file_format, window, path, save, title):
        pass

    def _request_text_input(self, title, request_text, prefill, parent, completer):
        pass

    def create_file_dne_warning(self, path):
        pass

    def create_folder_dne_warning(self, path):
        pass

    def create_info_popup(self, text, title):
        pass

    def create_warning_popup(self, text, window_title, text_title):
        pass

    def file_in_use_warning(self, title, text, detail):
        pass

    def get_folder(self, window, path):
        pass

    def get_open_path(self, file_format, window, path, title):
        pass

    def get_project_name(
        self,
    ):
        pass

    def get_save_path(self, file_format, window, path, title):
        pass

    def msg_unsaved(
        self,
    ):
        pass

    def req_delete_items(self, string_list, item_type):
        pass

    def req_export_pset_name(self, parent_window):
        pass

    def request_property_name(self, old_name, parent):
        pass

    def request_property_set_merge(self, name, mode):
        pass

    def request_save_before_exit(
        self,
    ):
        pass


class PredefinedPropertySet:
    def add_classes_to_table_widget(self, property_sets, table_widget):
        pass

    def add_property_sets_to_widget(self, property_sets, list_widget):
        pass

    def clear_class_table(
        self,
    ):
        pass

    def close_window(
        self,
    ):
        pass

    def connect_signals(
        self,
    ):
        pass

    def connect_window(self, window):
        pass

    def create_property_set(
        self,
    ):
        pass

    def create_window(
        self,
    ):
        pass

    def delete_selected_classes(
        self,
    ):
        pass

    def delete_selected_property_set(
        self,
    ):
        pass

    def get_action(self, name):
        pass

    def get_active_property_set(
        self,
    ):
        pass

    def get_class_from_item(self, item):
        pass

    def get_class_table_widget(
        self,
    ):
        pass

    def get_existing_psets_in_list_widget(self, pset_list):
        pass

    def get_existing_psets_in_table_widget(self, class_table):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_sets(
        self,
    ):
        pass

    def get_property_table(
        self,
    ):
        pass

    def get_pset_list_widget(
        self,
    ):
        pass

    def get_selected_linked_psets(
        self,
    ):
        pass

    def get_selected_property_set(
        self,
    ):
        pass

    def get_window(
        self,
    ):
        pass

    def is_edit_mode_active(
        self,
    ):
        pass

    def remove_property_sets_from_list_widget(self, property_sets, list_widget):
        pass

    def remove_property_sets_from_table_widget(self, property_sets, table_widget):
        pass

    def remove_selected_links(
        self,
    ):
        pass

    def rename_selected_property_set(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_active_property_set(self, property_set):
        pass

    def set_window(self, window):
        pass

    def update_class_widget(
        self,
    ):
        pass

    def update_pset_widget(
        self,
    ):
        pass


class PredefinedPropertySetCompare:
    def create_pset_list(self, psets0, psets1):
        pass

    def create_tree_selection_trigger(self, widget):
        pass

    def create_widget(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_pset_lists(
        self,
    ):
        pass

    def reset(
        self,
    ):
        pass

    def set_predefined_psets(self, psets0, psets1):
        pass

    def set_pset_lists(self, pset_lists):
        pass


class Project:
    def add_plugin_save_function(self, func):
        pass

    def create_combobox(self, filter_1):
        pass

    def create_mapping_window(self, title, filter_1, filter_2):
        pass

    def create_project(
        self,
    ):
        pass

    def fill_mapping_table(self, table, filter_1, filter_2):
        pass

    def get(
        self,
    ):
        pass

    def get_action(self, name):
        pass

    def get_filter_matrix(
        self,
    ):
        pass

    def get_mapping_from_table(self, table):
        pass

    def get_phase_mapping(self, title, p1, p2):
        pass

    def get_phases(
        self,
    ):
        pass

    def get_plugin_functions(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_root_classes(self, filter_classes, proj):
        pass

    def get_settings_general_widget(
        self,
    ):
        pass

    def get_settings_path_widget(
        self,
    ):
        pass

    def get_use_case_mapping(self, title, p1, p2):
        pass

    def get_use_cases(
        self,
    ):
        pass

    def load_project(self, path):
        pass

    def merge_projects(self, title, project_1, project_2):
        pass

    def remove_plugin_save_function(self, index):
        pass

    def set_action(self, name, action):
        pass

    def set_active_project(self, proj):
        pass

    def set_settings_general_widget(self, widget):
        pass

    def set_settings_path_widget(self, widget):
        pass


class ProjectFilter:
    def get_action(self, name):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_settings_widget(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_settings_widget(self, widget):
        pass


class Property:
    def add_property_data_value(self, name, getter, setter):
        pass

    def connect_signals(
        self,
    ):
        pass

    def create_by_dict(self, property_data):
        pass

    def get_allowed_unit_prefixes(self, appdata):
        pass

    def get_allowed_units(self, appdata):
        pass

    def get_checked_texts_from_list_widget(self, list_widget):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_data(self, som_property):
        pass

    def get_unit_settings_widget(
        self,
    ):
        pass

    def set_data_by_dict(self, som_property, data_dict):
        pass

    def set_unit_settings_widget(self, widget):
        pass


class PropertyCompare:
    def add_class_to_item(self, som_class, item, index):
        pass

    def add_missing_classes_to_tree(self, tree, root_classes):
        pass

    def add_properties_to_pset_tree(self, tree, add_missing):
        pass

    def are_classes_identical(self, class_0, class_1, check_pset):
        pass

    def are_properties_identical(self, property_0, property_1):
        pass

    def are_property_sets_identical(
        self, property_set0, property_set1, check_properties
    ):
        pass

    def children_are_identical(self, entity0, entity1):
        pass

    def clear_table(self, table):
        pass

    def clear_tree(self, tree):
        pass

    def compare_classes(self, class_0, class_1):
        pass

    def compare_properties(self, property_0, property_1):
        pass

    def compare_property_sets(self, pset_0, pset_1):
        pass

    def create_child_matchup(self, entity0, entity1):
        pass

    def create_class_dicts(
        self,
    ):
        pass

    def create_class_lists(
        self,
    ):
        pass

    def create_tree_selection_trigger(self, widget):
        pass

    def create_widget(
        self,
    ):
        pass

    def export_child_check(self, file, type_name, entity0, entity1, indent):
        pass

    def export_class_differences(self, file):
        pass

    def export_existance_check(self, file, type_name, entity0, entity1, indent):
        pass

    def export_name_check(self, file, type_name, entity0, entity1, indent):
        pass

    def export_property_check(self, file, type_name, attrib0, attrib1, indent):
        pass

    def export_property_differences(self, file, property_list):
        pass

    def export_pset_differences(self, file, pset_list, lb):
        pass

    def fill_class_tree(self, tree, add_missing):
        pass

    def fill_class_tree_layer(self, classes, parent_item, add_missing):
        pass

    def fill_pset_tree(self, tree, pset_list, add_missing):
        pass

    def fill_table(self, table, info_list, entities):
        pass

    def fill_value_table(self, table, som_property):
        pass

    def fill_value_table_pset(self, widget):
        pass

    def find_existing_parent_item(self, som_class):
        pass

    def find_matching_class(self, som_class, index):
        pass

    def find_matching_entity(self, search_element, uuid_dict1, name_dict1):
        pass

    def generate_name_dict(self, element_list):
        pass

    def generate_uuid_dict(self, element_list):
        pass

    def get_branch_color(self, index):
        pass

    def get_class_dict(
        self,
    ):
        pass

    def get_class_list(
        self,
    ):
        pass

    def get_class_tree(self, widget):
        pass

    def get_entities_from_item(self, item):
        pass

    def get_header_name_from_project(self, project):
        pass

    def get_ident_dict(self, index):
        pass

    def get_info_table(self, widget):
        pass

    def get_item_from_class(self, som_class):
        pass

    def get_level(self, index):
        pass

    def get_missing_classes(self, index):
        pass

    def get_name_path(self, entity):
        pass

    def get_project(self, index):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_info_list(
        self,
    ):
        pass

    def get_property_list(self, property_set):
        pass

    def get_pset_info_list(
        self,
    ):
        pass

    def get_pset_list(self, som_class):
        pass

    def get_pset_tree(self, widget):
        pass

    def get_selected_entity(self, tree):
        pass

    def get_selected_item(self, tree):
        pass

    def get_uuid_dict(self, index):
        pass

    def get_value_list(self, entity):
        pass

    def get_value_table(self, widget):
        pass

    def get_widget(
        self,
    ):
        pass

    def reset(
        self,
    ):
        pass

    def set_branch_color(self, tree, index, color):
        pass

    def set_class_item_relation(self, som_class, item):
        pass

    def set_header_labels(self, trees, tables, labels):
        pass

    def set_projects(self, project1, project2):
        pass

    def set_property_list(self, property_set, property_list):
        pass

    def set_pset_list(self, som_class, pset_list):
        pass

    def set_tree_row_color(self, item, style_index):
        pass

    def set_value_list(self, entity, value_list):
        pass

    def style_parent_item(self, item, style):
        pass

    def style_table(self, table, shift):
        pass

    def style_tree_item(self, item):
        pass


class PropertyImport:
    def connect_ifc_import_runner(self, runner):
        pass

    def connect_property_import_runner(self, runner):
        pass

    def create_ifc_import_window(self, ifc_importer):
        pass

    def create_import_runner(self, ifc_import_path, progress_bar):
        pass

    def create_property_import_runner(self, runner):
        pass

    def destroy_import_runner(self, runner):
        pass

    def get_action(self, name):
        pass

    def get_ifc_import_window(
        self,
    ):
        pass

    def get_main_property(
        self,
    ):
        pass

    def get_main_pset(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_threadpool(
        self,
    ):
        pass

    def import_is_running(
        self,
    ):
        pass

    def is_aborted(
        self,
    ):
        pass

    def last_import_finished(
        self,
    ):
        pass

    def reset_abort(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_main_property(self, main_property_name):
        pass

    def set_main_pset(self, main_pset_name):
        pass

    def set_progress(self, runner, value):
        pass

    def set_status(self, runner, status):
        pass


class PropertyImportResults:
    def build_property_dict(self, classes):
        pass

    def calculate_all_checkbox_state(
        self,
    ):
        pass

    def checkstate_to_int(self, checkstate):
        pass

    def connect_trigger(self, property_widget):
        pass

    def create_import_window(
        self,
    ):
        pass

    def disable_table(self, table_widget):
        pass

    def find_checkbox_row_in_table(self, table_widget, checkbox):
        pass

    def get_all_checkbox(
        self,
    ):
        pass

    def get_all_keyword(
        self,
    ):
        pass

    def get_existing_values_in_table(self, table_widget, datatypes):
        pass

    def get_ifctype_combo_box(
        self,
    ):
        pass

    def get_input_variables(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_item_text_color(self, row):
        pass

    def get_property_table(
        self,
    ):
        pass

    def get_pset_table(
        self,
    ):
        pass

    def get_results_window(
        self,
    ):
        pass

    def get_selected_property(
        self,
    ):
        pass

    def get_selected_property_set(
        self,
    ):
        pass

    def get_somtype_combo_box(
        self,
    ):
        pass

    def get_update_lock_reason(
        self,
    ):
        pass

    def get_value_from_table_row(self, table_widget, row, data_types):
        pass

    def get_value_table(
        self,
    ):
        pass

    def is_updating_locked(
        self,
    ):
        pass

    def is_window_allready_build(
        self,
    ):
        pass

    def lock_updating(self, reason):
        pass

    def remove_results_window(
        self,
    ):
        pass

    def set_all_checkbox_state(self, state):
        pass

    def set_class_count_label_text(self, text):
        pass

    def unlock_updating(
        self,
    ):
        pass

    def update_combobox(self, combobox, allowed_values):
        pass

    def update_property_table_styling(
        self,
    ):
        pass

    def update_results_window(
        self,
    ):
        pass

    def update_som_combobox(self, combobox, allowed_values, class_list):
        pass

    def update_table_widget(self, allowed_values, table_widget, datatypes):
        pass

    def update_valuetable_checkstate(self, checkstate_dict):
        pass


class PropertyImportSQL:
    def add_entity(self, entity, main_pset, main_property, file_name):
        pass

    def add_properties_to_filter_table(self, project, som_property):
        pass

    def add_property_with_value(self, som_property):
        pass

    def add_property_without_value(self, som_property):
        pass

    def are_entities_with_identifiers_existing(
        self,
    ):
        pass

    def change_checkstate_of_values(
        self, ifc_type, identifier, property_set, property_query, value_text, checkstate
    ):
        pass

    def commit_sql(
        self,
    ):
        pass

    def connect_to_data_base(self, path):
        pass

    def count_classes(self, ifc_type, identifier):
        pass

    def create_export_query(
        self,
    ):
        pass

    def create_settings_filter(
        self,
    ):
        pass

    def create_settings_window(
        self,
    ):
        pass

    def create_som_filter_table(
        self,
    ):
        pass

    def create_table_exection_query(self, table_name, row_names, row_datatypes):
        pass

    def create_tables(
        self,
    ):
        pass

    def disconnect_from_database(
        self,
    ):
        pass

    def fill_filter_table(self, project):
        pass

    def fill_property_filter_table(self, values):
        pass

    def fill_som_properties(self, values):
        pass

    def get_current_class_filter(
        self,
    ):
        pass

    def get_cursor(
        self,
    ):
        pass

    def get_database_path(
        self,
    ):
        pass

    def get_datatype_from_value(self, value):
        pass

    def get_identifier_types(self, ifc_type, all_keyword):
        pass

    def get_new_property_values(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_data(self, som_property):
        pass

    def get_property_list(self, ifc_type, identifier, property_set):
        pass

    def get_property_query(
        self,
    ):
        pass

    def get_property_sets(self, ifc_type, identifier):
        pass

    def get_removed_property_values(
        self,
    ):
        pass

    def get_settings_dialog_checkbox_list(self, dialog):
        pass

    def get_values(self, ifc_type, identifier, property_set, property_query):
        pass

    def get_wanted_ifc_types(
        self,
    ):
        pass

    def import_entity_properties(
        self, entity, ifc_file, identifier, existing_class_dict
    ):
        pass

    def init_database(self, db_path):
        pass

    def set_current_class_filter(self, usecases, phases):
        pass

    def set_database_path(self, path):
        pass

    def settings_dialog_accepted(self, dialog):
        pass

    def sql_to_excel(self, query, export_path):
        pass

    def update_settins_dialog_checkstates(self, dialog):
        pass


class PropertySet:
    def add_property_sets_to_table(self, property_sets, table):
        pass

    def clear_table(
        self,
    ):
        pass

    def create_context_menu(self, global_pos, function_list):
        pass

    def create_property_set(self, name, som_class, parent):
        pass

    def delete_table_pset(
        self,
    ):
        pass

    def get_active_property_set(
        self,
    ):
        pass

    def get_existing_psets_in_table(self, table):
        pass

    def get_inheritable_property_sets(self, som_class):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_by_name(self, property_set, name):
        pass

    def get_property_set_from_item(self, item):
        pass

    def get_property_set_from_row(self, row, table):
        pass

    def get_property_sets(self, active_class):
        pass

    def get_pset_from_index(self, index):
        pass

    def get_pset_from_item(self, item):
        pass

    def get_row_from_pset(self, property_set):
        pass

    def get_selecte_property_set_from_table(
        self,
    ):
        pass

    def get_table(
        self,
    ):
        pass

    def is_pset_existing(self, pset_name, active_class):
        pass

    def pset_table_is_editing(
        self,
    ):
        pass

    def remove_property_by_name(self, property_set, property_name):
        pass

    def remove_property_sets_from_table(self, property_sets, table):
        pass

    def rename_table_pset(
        self,
    ):
        pass


    def select_property_set(self, property_set):
        pass

    def set_active_property_set(self, property_set):
        pass

    def set_enabled(self, enabled):
        pass

    def set_pset_name_by_row(self, pset, row, table):
        pass

    def set_sorting_indicator(self, table_widget, col_index):
        pass

    def trigger_table_repaint(
        self,
    ):
        pass

    def update_completer(self, som_class):
        pass

    def update_property_set_table(self, table):
        pass

    def update_table_row(self, table, row):
        pass


class PropertyTable:
    def add_column_to_table(self, name, get_function):
        pass

    def add_context_menu_builder(self, context_menu_builder):
        pass

    def add_parent_of_selected_properties(self, table):
        pass

    def add_properties_to_table(self, properties, table):
        pass

    def connect_table(self, table):
        pass

    def context_menu_builder_add_connection(self, table):
        pass

    def context_menu_builder_delete(self, table, with_child):
        pass

    def context_menu_builder_remove_connection(self, table):
        pass

    def context_menu_builder_rename(self, table):
        pass

    def delete_selected_properties(self, table, with_child):
        pass

    def edit_selected_property_name(self, table):
        pass

    def format_row(self, row):
        pass

    def format_row_value(self, item, value):
        pass

    def get_column_count(
        self,
    ):
        pass

    def get_context_menu_builders(
        self,
    ):
        pass

    def get_existing_properties(self, table):
        pass

    def get_header_labels(
        self,
    ):
        pass

    def get_item_from_pos(self, table, pos):
        pass

    def get_possible_parent(self, som_property):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_dict_from_mime_data(self, mime_data):
        pass

    def get_property_from_item(self, item):
        pass

    def get_property_set_by_table(self, table):
        pass

    def get_property_set_of_table(self, table):
        pass

    def get_row_index_from_property(self, som_property, table):
        pass

    def get_selected_properties(self, table):
        pass

    def is_drop_allowed(self, event, target_table):
        pass

    def refresh_table(self, table):
        pass

    def remove_parent_of_selected_properties(self, table):
        pass

    def remove_properties_from_table(self, properties, table):
        pass

    def set_property_set_of_table(self, table, property_set):
        pass

    def update_row(self, table, index):
        pass

    def write_property_dicts_to_mime_data(self, property_dicts, mime_data):
        pass


class PropertyWindow:
    def add_context_menu_builder(self, context_menu_builder):
        pass

    def add_plugin_entry(
        self,
        key,
        layout_name,
        widget_creator,
        index,
        value_getter,
        value_setter,
        widget_value_setter,
        test_function,
    ):
        pass

    def add_value(self, table_view, value):
        pass

    def connect_signals(
        self,
    ):
        pass

    def connect_splitter_widget(self, widget):
        pass

    def connect_value_view(self, window):
        pass

    def create_window(self, som_property):
        pass

    def create_window_title(self, som_property):
        pass

    def get_allowed_data_types(
        self,
    ):
        pass

    def get_allowed_value_types(
        self,
    ):
        pass

    def get_context_menu_builders(
        self,
    ):
        pass

    def get_datatype_combobox(self, widget_ui):
        pass

    def get_description_textedit(self, widget_ui):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_from_window(self, window):
        pass

    def get_selected_rows(self, table_view):
        pass

    def get_selected_values(self, table_view):
        pass

    def get_splitter_settings_checkstate(self, widget):
        pass

    def get_splitter_settings_text(self, widget):
        pass

    def get_splitter_settings_widget(
        self,
    ):
        pass

    def get_ui(self, som_property):
        pass

    def get_unit_combobox(self, widget_ui):
        pass

    def get_valuetype_combobox(self, widget_ui):
        pass

    def get_window(self, som_property):
        pass

    def get_windows(
        self,
    ):
        pass

    def ignore_builder(self, table_view):
        pass

    def prefill_comboboxes(self, window):
        pass

    def remove_builder(self, table_view):
        pass

    def remove_plugin_entry(self, key):
        pass

    def remove_selected_values(self, table_view):
        pass

    def remove_window(self, window):
        pass

    def rename_property(self, som_property, value):
        pass

    def set_comboboxes_enabled(self, enabled_state, window):
        pass

    def set_datatype(self, som_property, value):
        pass

    def set_description(self, som_property, value):
        pass

    def set_optional(self, som_property, value):
        pass

    def set_selecteded_values_ignored(self, table_view, state):
        pass

    def set_splitter_settings_widget(self, widget):
        pass

    def set_unit(self, som_property, value):
        pass

    def set_value(self, table_view, row, value):
        pass

    def set_value_inherit_state(self, som_property, value):
        pass

    def set_values(self, table_view, start_row, values):
        pass

    def set_valuetype(self, som_property, value):
        pass

    def show_property_info(self, som_property):
        pass

    def unignore_builder(self, table_view):
        pass

    def update_unit_completer(self, window):
        pass


class Search:
    def _search(self, search_mode, search_items, data_getters):
        pass

    def connect_signals(
        self,
    ):
        pass

    def create_table_items(self, dialog, search_items, getter_methods):
        pass

    def fill_table(self, dialog, search_items, data_getters):
        pass

    def get_column_texts(self, search_mode):
        pass

    def get_dialogues(
        self,
    ):
        pass

    def get_info_from_item(self, item):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_row_matchscore(self, dialog, search_text, row, column_count):
        pass

    def get_search_mode(self, dialog):
        pass

    def get_search_text(self, dialog):
        pass

    def get_selected_item(self, dialog):
        pass

    def get_table(self, dialog):
        pass

    def get_threshold(
        self,
    ):
        pass

    def is_in_strict_model(self, dialog):
        pass

    def retranslate_title(self, dialog, search_mode):
        pass

    def search_class(self, searchable_classes):
        pass

    def search_property(self, searchable_properties):
        pass

    def set_info_of_item(self, item, info):
        pass


class Settings:
    def add_page_to_toolbox(self, widget_function, page_name, accept_function):
        pass

    def close(
        self,
    ):
        pass

    def create_dialog(
        self,
    ):
        pass

    def create_tab(self, tab_widget, tab_name):
        pass

    def get_accept_functions(
        self,
    ):
        pass

    def get_action(self, name):
        pass

    def get_page_dict(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_widget(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_widget(self, widget):
        pass


class UseCase:
    def _connect_views(self, proxy_view, view):
        pass

    def add_editable_header_to_view(self, view):
        pass

    def add_header_view(self, project):
        pass

    def add_models_to_window(self, project):
        pass

    def connect_class_views(
        self,
    ):
        pass

    def connect_models(
        self,
    ):
        pass

    def connect_project_view(
        self,
    ):
        pass

    def connect_property_views(
        self,
    ):
        pass

    def connect_signals(
        self,
    ):
        pass

    def create_context_menu(self, menu_list, pos):
        pass

    def create_header_views(self, project, first_columns):
        pass

    def create_window(
        self,
    ):
        pass

    def get_action(self, name):
        pass

    def get_active_class(
        self,
    ):
        pass

    def get_class_header_model(
        self,
    ):
        pass

    def get_class_model(
        self,
    ):
        pass

    def get_class_views(
        self,
    ):
        pass

    def get_mouse_press_checkstate(
        self,
    ):
        pass

    def get_project_model(
        self,
    ):
        pass

    def get_project_view(
        self,
    ):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property_header_model(
        self,
    ):
        pass

    def get_property_label(
        self,
    ):
        pass

    def get_property_model(
        self,
    ):
        pass

    def get_property_views(
        self,
    ):
        pass

    def get_window(
        self,
    ):
        pass

    def is_mouse_pressed(
        self,
    ):
        pass

    def set_action(self, name, action):
        pass

    def set_mouse_press_checkstate(self, checkstate):
        pass

    def set_mouse_pressed(self, pressed):
        pass

    def tree_move_click_drag(self, index):
        pass


class Util:
    def add_shortcut(self, sequence, window, function):
        pass

    def autofill_path(self, line_edit, appdata):
        pass

    def bool_to_checkstate(self, checkstate):
        pass

    def checkstate_to_bool(self, checkstate):
        pass

    def context_menu_create_action(self, menu_dict, name, action_func, is_sub_menu):
        pass

    def create_completer(self, texts, widget):
        pass

    def create_context_menu(self, menu_list):
        pass

    def create_directory(self, path):
        pass

    def create_file_selector(
        self,
        name,
        file_extension,
        appdata_text,
        request_folder,
        request_save,
        single_request,
    ):
        pass

    def create_progressbar(self, args, kwargs):
        pass

    def create_tempfile(self, suffix):
        pass

    def fill_file_selector(
        self,
        widget,
        name,
        file_extension,
        appdata_text,
        request_folder,
        request_save,
        single_request,
        update_appdata,
    ):
        pass

    def fill_list_widget_with_checkstate(self, list_widget, allowed_labels, all_labels):
        pass

    def fill_main_property(
        self, widget, pset_name, property_name, pset_placeholder, property_placeholder
    ):
        pass

    def get_combobox_values(self, combo_box):
        pass

    def get_greyed_out_brush(
        self,
    ):
        pass

    def get_new_name(self, standard_name, existing_names):
        pass

    def get_path_from_fileselector(self, file_selector):
        pass

    def get_properties(
        self,
    ):
        pass

    def get_property(self, widget):
        pass

    def get_standard_text_brush(
        self,
    ):
        pass

    def get_text_from_combobox(self, combobox):
        pass

    def get_window_title(self, window_name):
        pass

    def insert_tab_order(self, previous_widget, inserted_widget):
        pass

    def menu_bar_add_action(self, menu_bar, menu_dict, menu_path, function):
        pass

    def menu_bar_add_menu(self, menu_bar, menu_dict, menu_path):
        pass

    def menu_bar_create_actions(self, menu_dict, parent):
        pass

    def request_path(self, widget):
        pass

    def set_progress(self, progress_bar, value):
        pass

    def set_status(self, progress_bar, value):
        pass

    def transform_guid(self, guid, add_zero_width):
        pass

    def user_is_using_darkmode(
        self,
    ):
        pass
