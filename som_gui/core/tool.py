class Attribute:
    def add_attribute_data_value(self, name, getter, setter): pass

    def create_attribute(self, property_set, attribute_data): pass

    def delete(self, attribute): pass

    def get_attribute_data(self, attribute): pass

    def get_attribute_data_type(self, attribute): pass

    def get_attribute_description(self, attribute): pass

    def get_attribute_name(self, attribute): pass

    def get_attribute_properties(self): pass

    def get_attribute_value_type(self, attribute): pass

    def get_attribute_values(self, attribute): pass

    def get_inherit_state(self, attribute): pass

    def is_attribute_optional(self, attribute): pass

    def set_attribute_data(self, attribute, data_dict): pass

    def set_attribute_data_type(self, value, attribute): pass

    def set_attribute_description(self, value, attribute): pass

    def set_attribute_name(self, value, attribute): pass

    def set_attribute_optional(self, optional, attribute): pass

    def set_attribute_value_type(self, value, attribute): pass

    def set_attribute_values(self, value, attribute): pass

    def set_inherit_state(self, state, attribute): pass


class AttributeTable:
    def add_attributes_to_table(self, attributes, table): pass

    def add_column_to_table(self, name, get_function): pass

    def add_parent_of_selected_attribute(self): pass

    def delete_selected_attributes(self): pass

    def edit_selected_attribute_name(self): pass

    def format_attribute_table_value(self, item, value): pass

    def format_row(self, row): pass

    def get_active_table(self): pass

    def get_attribute_from_item(self, item): pass

    def get_attribute_table_header_names(self): pass

    def get_existing_attributes_in_table(self, table): pass

    def get_item_from_pos(self, table, pos): pass

    def get_possible_parent(self, attribute): pass

    def get_properties(self): pass

    def get_property_set_by_table(self, table): pass

    def get_row_from_attribute(self, attribute, table): pass

    def remove_attributes_from_table(self, attributes, table): pass

    def remove_parent_of_selected_attribute(self): pass

    def set_active_attribute(self, attribute): pass

    def set_active_table(self, table): pass

    def update_row(self, table, index): pass


class IfcImporter:
    def autofill_ifcpath(self, line_edit): pass

    def check_inputs(self, ifc_paths, main_pset, main_attribute): pass

    def create_importer(self): pass

    def create_runner(self, status_label, path): pass

    def create_thread_pool(self): pass

    def fill_main_attribute(self, widget, pset, attribute): pass

    def get_ifc_paths(self, widget): pass

    def get_main_attribute(self, widget): pass

    def get_main_pset(self, widget): pass

    def get_properties(self): pass

    def open_file_dialog(self, window, base_path): pass

    def set_progress(self, widget, value): pass

    def set_progressbar_visible(self, widget, visible): pass

    def set_status(self, widget, status): pass


class MainWindow:
    def add_action(self, menu_path, function): pass

    def add_menu(self, menu_path): pass

    def create_actions(self, menu_dict, parent): pass

    def create_status_label(self): pass

    def get(self): pass

    def get_app(self): pass

    def get_properties(self): pass

    def get_menu_bar(self): pass

    def get_menu_dict(self): pass

    def get_object_infos(self): pass

    def get_pset_name(self): pass

    def get_ui(self): pass

    def set(self, window): pass

    def set_status_bar_text(self, text): pass

    def set_window_title(self, title): pass


class Modelcheck:
    def abort(self): pass

    def add_issues(self, guid, description, issue_type, attribute, pset_name, attribute_name, value): pass

    def attribute_issue(self, guid, pset_name, attribute_name, element_type): pass

    def build_data_dict(self, check_state_dict): pass


    def build_ident_dict(self, objects): pass

    def check_datatype(self, value, attribute): pass

    def check_for_attributes(self, element, obj): pass

    def check_format(self, value, attribute): pass

    def check_list(self, value, attribute): pass

    def check_range(self, value, attribute): pass

    def check_values(self, value, attribute): pass

    def commit_sql(self): pass

    def connect_to_data_base(self, path): pass

    def create_modelcheck_runner(self, ifc_file): pass

    def create_new_sql_database(self): pass

    def create_tables(self): pass

    def datatype_issue(self, guid, attribute, element_type, datatype, value): pass

    def db_create_entity(self, element, bauteil_klasse): pass

    def disconnect_from_data_base(self): pass

    def empty_group_issue(self, element): pass

    def empty_value_issue(self, guid, pset_name, attribute_name, element_type): pass

    def entity_is_in_group(self, entity): pass

    def entity_should_be_tested(self, entity): pass

    def format_issue(self, guid, attribute, value): pass

    def get_active_element(self): pass

    def get_active_element_type(self): pass

    def get_active_guid(self): pass


    def get_attribute_value(self, entity, pset_name, attribute_name): pass

    def get_current_runner(self): pass

    def get_cursor(self): pass

    def get_data_dict(self): pass

    def get_database_path(self): pass

    def get_element_count(self): pass

    def get_entities_without_group_assertion(self, ifc): pass

    def get_group_count(self): pass

    def get_guids(self): pass

    def get_ident_dict(self): pass

    def get_ident_value(self, entity): pass

    def get_ifc_name(self): pass

    def get_main_attribute_name(self): pass

    def get_main_pset_name(self): pass

    def get_object_checked_count(self): pass

    def get_object_count(self): pass

    def get_object_representation(self, entity): pass

    def get_parent_entity(self, entity): pass

    def get_properties(self): pass

    def get_root_groups(self, ifc): pass


    def guid_issue(self, guid, file1, file2): pass

    def ident_issue(self, guid, pset_name, attribute_name): pass

    def ident_pset_issue(self, guid, pset_name): pass

    def ident_unknown(self, guid, pset_name, attribute_name, value): pass

    def increment_checked_items(self): pass

    def is_aborted(self): pass

    def is_attribute_existing(self, entity, pset_name, attribute_name): pass


    def is_pset_existing(self, entity, pset_name): pass

    def is_root_group(self, group): pass

    def iterate_group_structure(self, entity): pass

    def list_issue(self, guid, attribute, element_type, value): pass

    def parent_issue(self, element, parent_element): pass

    def property_set_issue(self, guid, pset_name, element_type): pass

    def range_issue(self, guid, attribute, element_type, value): pass

    def remove_existing_issues(self, creation_date): pass

    def repetetive_group_issue(self, element): pass

    def reset_abort(self): pass

    def reset_guids(self): pass

    def set_active_element(self, element): pass

    def set_active_element_type(self, value): pass

    def set_current_runner(self, runner): pass

    def set_data_dict(self, value): pass

    def set_database_path(self, path): pass

    def set_ifc_name(self, value): pass

    def set_main_attribute_name(self, value): pass

    def set_main_pset_name(self, value): pass

    def set_object_checked_count(self, value): pass

    def set_object_count(self, value): pass

    def set_parent_entity(self, entity, parent_entity): pass

    def set_progress(self, value): pass

    def set_status(self, text): pass

    def set_sub_entities(self, entity, sub_entities): pass


    def subgroup_issue(self, child_ident): pass

    def transform_guid(self, guid, add_zero_width): pass


class ModelcheckExternal:
    def _build_tree(self): pass

    def create_menubar(self, window, main_pset_name, main_attribute_name): pass

    def create_window(self): pass

    def export_bimcollab(self): pass

    def export_desite_attribute_table(self, main_pset_name, main_attribute_name): pass

    def export_desite_csv(self): pass

    def export_desite_fast(self, pset_name, attribute_name): pass

    def export_desite_js(self, main_pset_name, main_attribute_name): pass

    def export_ids(self): pass

    def get_data_dict(self): pass

    def get_properties(self): pass

    def get_window(self): pass

    def is_window_allready_build(self): pass


class ModelcheckResults:
    def autofit_column_width(self, worksheet): pass

    def create_table(self, worksheet, last_cell): pass

    def create_workbook(self): pass

    def fill_worksheet(self, issues, ws): pass

    def get_export_path(self): pass

    def get_max_width(self, worksheet): pass

    def get_properties(self): pass

    def last_modelcheck_finished(self): pass

    def query_issues(self, path): pass

    def set_export_path(self, value): pass


class ModelcheckWindow:
    def _update_pset_row(self, item, enabled): pass

    def add_splitter(self, layout, orientation, widget_1, widget_2): pass

    def autofill_export_path(self): pass

    def check_export_path(self, export_path): pass

    def check_selection(self, widget): pass

    def close_window(self): pass

    def collapse_selection(self, widget): pass

    def connect_buttons(self, buttons): pass

    def connect_check_widget(self, widget): pass

    def connect_ifc_import_runner(self, runner): pass

    def connect_modelcheck_runner(self, runner): pass

    def create_checkbox_widget(self): pass

    def create_context_menu(self, pos, funcion_list, widget): pass

    def create_export_line(self, widget): pass

    def create_import_runner(self, ifc_import_path): pass

    def create_object_tree_row(self, obj): pass

    def create_pset_tree_row(self, entity, parent_item): pass

    def create_window(self): pass

    def destroy_import_runner(self, runner): pass

    def expand_selection(self, widget): pass

    def fill_object_tree(self, entities, parent_item, model, tree): pass

    def fill_pset_tree(self, property_sets, enabled, tree): pass

    def get_buttons(self): pass

    def get_export_path(self, widget): pass

    def get_ifc_import_widget(self): pass

    def get_item_check_state(self, item): pass

    def get_item_checkstate_dict(self): pass

    def get_item_status_dict(self): pass

    def get_modelcheck_threadpool(self): pass

    def get_object_tree(self): pass

    def get_properties(self): pass

    def get_pset_tree(self): pass

    def get_selected_items(self, widget): pass

    def get_selected_object(self): pass

    def get_window(self): pass

    def is_initial_paint(self): pass

    def is_window_allready_build(self): pass

    def modelcheck_is_running(self): pass

    def open_export_dialog(self, base_path, file_text): pass

    def read_inputs(self): pass

    def resize_object_tree(self): pass

    def set_abort_button_text(self, text): pass

    def set_export_line_text(self, text): pass

    def set_importer_widget(self, widget): pass

    def set_item_check_state(self, item, cs): pass

    def set_progress(self, value): pass

    def set_pset_tree_title(self, text): pass

    def set_run_button_enabled(self, state): pass

    def set_selected_object(self, obj): pass

    def set_status(self, text): pass

    def show_pset_tree_title(self, show): pass

    def uncheck_selection(self, widget): pass

    def update_object_tree_row(self, parent_item, row_index): pass


class Object:
    def add_context_menu_entry(self, name, function, single, multi): pass

    def add_ifc_mapping(self, mapping): pass

    def autofit_tree(self): pass

    def change_object_info(self, obj, data_dict): pass

    def check_object_creation_input(self, data_dict): pass

    def clear_context_menu_list(self): pass

    def clear_object_input(self, ui): pass

    def collapse_selection(self): pass

    def copy_object(self, obj, data_dict): pass

    def create_completer(self, texts, lineedit): pass

    def create_context_menu(self): pass

    def create_ifc_completer(self): pass

    def create_item(self, obj): pass

    def create_object(self, data_dict, property_set, attribute): pass

    def delete_object(self, obj, recursive): pass

    def delete_selection(self): pass

    def drop_indication_pos_is_on_item(self): pass

    def expand_selection(self): pass

    def expand_to_item(self, item): pass

    def fill_object_entry(self, obj): pass

    def fill_object_tree(self, objects, parent_item): pass

    def find_attribute(self, obj, pset_name, attribute_name): pass

    def get_active_object(self): pass

    def get_all_objects(self): pass

    def get_existing_abbriviations(self): pass

    def get_existing_ident_values(self): pass

    def get_ifc_mappings(self): pass

    def get_item_from_object(self, obj): pass

    def get_item_from_pos(self, pos): pass

    def get_object_from_item(self, item): pass

    def get_object_info_properties(self): pass

    def get_object_tree(self): pass

    def get_properties(self): pass

    def get_selected_items(self): pass

    def get_selected_objects(self): pass

    def group_objects(self, parent, children): pass

    def group_selection(self): pass

    def handle_attribute_issue(self, result): pass

    def is_identifier_allowed(self, identifier, ignore): pass

    def oi_change_visibilit_identifiers(self, hide): pass

    def oi_change_visibility_identifiers(self, hide): pass

    def oi_create_dialog(self): pass

    def oi_fill_properties(self, mode): pass

    def oi_get_focus_object(self): pass

    def oi_get_mode(self): pass

    def oi_get_values(self): pass

    def oi_set_abbrev_value_color(self, color): pass

    def oi_set_abbreviation(self, value): pass

    def oi_set_ident_value_color(self, color): pass

    def oi_set_values(self, data_dict): pass

    def oi_update_attribute_combobox(self): pass

    def oi_update_dialog(self): pass

    def resize_tree(self): pass

    def select_object(self, obj): pass

    def set_active_object(self, obj): pass

    def set_ident_value(self, obj, value): pass

    def set_values(self, data_dict): pass

    def update_check_state(self, item): pass

    def update_item(self, item, obj): pass


class ObjectFilter:
    def add_use_case_to_settings_window(self): pass

    def create_header_data(self, filter_matrix): pass

    def create_row(self, entity, filter_index_list): pass

    def create_tree(self, entities, parent_item, filter_index_list, pre_header_text_length, model, tree): pass

    def create_tree_models(self): pass

    def create_window(self): pass

    def delete_use_case_window(self): pass

    def fill_object_tree(self, root_objects): pass

    def format_object_tree_header(self): pass

    def get_active_checkstate(self): pass

    def get_active_object(self): pass

    def get_active_use_case(self): pass

    def get_active_use_case_name(self): pass

    def get_attribute_dict(self): pass

    def get_check_state(self, project_phase_index, use_case_index, entity): pass

    def get_check_statuses(self, index): pass

    def get_checkstate(self, index): pass

    def get_enabled_statuses(self, index): pass

    def get_filter_indexes(self): pass

    def get_filter_matrix(self): pass

    def get_filter_names(self): pass

    def get_header_texts(self): pass

    def get_index_by_object(self, obj): pass

    def get_linked_data(self, index): pass

    def get_new_use_case_name(self, standard_name, existing_names): pass

    def get_object_dict(self): pass

    def get_object_model(self): pass

    def get_object_tree(self): pass

    def get_objectfilter_properties(self): pass

    def get_pset_dict(self): pass

    def get_pset_model(self): pass

    def get_pset_tree(self): pass

    def get_title_count_by_index(self, index): pass

    def get_title_lenght_by_model(self, model): pass

    def get_use_case_list(self): pass

    def get_use_case_name_list(self): pass

    def get_widget(self): pass

    def is_object_enabled(self, index): pass

    def is_tree_clicked(self): pass

    def load_use_cases(self): pass

    def reset_use_case_data(self): pass

    def resize_tree(self, tree): pass

    def set_active_object(self, obj): pass

    def set_header_data(self, header_data): pass

    def set_header_labels(self, model, labels): pass

    def set_use_case(self, use_case_name): pass

    def toggle_checkstate(self, index): pass

    def tree_activate_click_drag(self, index): pass

    def tree_move_click_drag(self, index): pass

    def tree_release_click_drag(self, index): pass

    def update_active_object_label(self): pass

    def update_attribute_data(self): pass

    def update_attribute_uses_cases(self): pass

    def update_enable_status(self, item, model): pass

    def update_object_data(self, obj): pass

    def update_object_use_cases(self): pass

    def update_pset_data(self): pass

    def update_pset_tree(self): pass

    def update_pset_use_cases(self): pass


class Popups:
    def _request_text_input(self, title, request_text, prefill, parent): pass

    def create_file_dne_warning(self, path): pass

    def create_folder_dne_warning(self, path): pass

    def create_warning_popup(self, text, title): pass

    def error_convert_double(): pass

    def error_convert_integer(): pass

    def file_in_use_warning(self, title, text, detail): pass

    def get_new_use_case_name(self, old_name, parent): pass

    def get_path(self, file_format, window): pass

    def get_phase_name(self, old_name, parent): pass

    def get_project_name(self): pass

    def get_save_path(self, base_path): pass

    def msg_unsaved(self): pass

    def request_attribute_name(self, old_name, parent): pass

    def request_property_set_merge(self, name, mode): pass

    def request_save_before_exit(self): pass


class PredefinedPropertySet:
    def add_objects_to_table_widget(self, property_sets, table_widget): pass

    def add_property_sets_to_widget(self, property_sets, list_widget): pass

    def clear_object_table(self): pass

    def close_window(self): pass

    def connect_triggers(self, window): pass

    def create_property_set(self): pass

    def create_window(self): pass

    def delete_selected_objects(self): pass

    def delete_selected_property_set(self): pass

    def get_active_property_set(self): pass

    def get_existing_psets_in_list_widget(self, pset_list): pass

    def get_existing_psets_in_table_widget(self, object_table): pass

    def get_object_table_widget(self): pass

    def get_properties(self): pass

    def get_property_sets(self): pass

    def get_pset_list_widget(self): pass

    def get_selected_linked_psets(self): pass

    def get_selected_property_set(self): pass

    def get_window(self): pass

    def is_edit_mode_active(self): pass

    def remove_property_sets_from_list_widget(self, property_sets, list_widget): pass

    def remove_property_sets_from_table_widget(self, property_sets, table_widget): pass

    def remove_selected_links(self): pass

    def rename_selected_property_set(self): pass

    def set_active_property_set(self, property_set): pass

    def set_window(self, window): pass

    def update_object_widget(self): pass

    def update_pset_widget(self): pass


class Project:
    def add_node_pos(self, main_window, main_dict, path): pass

    def add_project_setting(self, get_function, set_function, name, options): pass

    def add_setting_to_dialog(self, setting_dict): pass

    def add_shortcut(self, sequence, window, function): pass

    def create_combobox(self, filter_1): pass

    def create_mapping_window(self, filter_1, filter_2): pass

    def create_project(self): pass

    def create_project_infos(self): pass

    def fill_mapping_table(self, table, filter_1, filter_2): pass

    def get(self): pass

    def get_all_objects(self): pass

    def get_filter_matrix(self): pass

    def get_mapping_from_table(self, table): pass

    def get_new_name(self, standard_name, existing_names): pass

    def get_path(self, title, file_text): pass

    def get_phase_mapping(self, p1, p2): pass

    def get_phases(self): pass

    def get_project_author(self): pass

    def get_project_infos(self): pass

    def get_project_name(self): pass

    def get_project_pase_list(self): pass

    def get_project_phase(self): pass

    def get_project_phase_list(self): pass

    def get_project_phase_name(self): pass

    def get_project_phase_name_list(self): pass

    def get_properties(self): pass

    def get_project_version(self): pass

    def get_root_objects(self, filter_objects): pass

    def get_use_case_mapping(self, p1, p2): pass

    def get_use_cases(self): pass

    def import_node_pos(self, proj): pass

    def load_project(self, path): pass

    def merge_projects(self, project_1, project_2): pass

    def refresh_info_dict(self, info_dict, index): pass

    def reset_project_infos(self): pass

    def set_active_project(self, proj): pass

    def set_project_author(self, author): pass

    def set_project_name(self, name): pass

    def set_project_phase(self, phase_name): pass

    def set_project_version(self, version): pass

    def update_setting(self, info_dict): pass


class ProjectFilter:
    def add_phase(self): pass

    def add_use_case(self): pass

    def create_context_menu(self, value, menu_list, pos): pass

    def create_dialog(self): pass

    def create_header(self): pass

    def delete_dialog(self): pass

    def delete_filter(self): pass

    def fill_filter_properties(self): pass

    def get_filter_matrix(self): pass

    def get_filter_state(self, phase, use_case): pass

    def get_header_item(self, section, orientation): pass

    def get_phase_list(self): pass

    def get_properties(self): pass

    def get_table(self): pass

    def get_use_case_list(self): pass

    def rename_filter(self): pass

    def set_column(self, column, use_case): pass

    def set_row(self, row, phase): pass

    def set_selected_header(self, item): pass

    def set_state(self, use_case, phase, state): pass

    def update_item(self, row, column): pass


class PropertySet:
    def add_property_sets_to_table(self, property_sets, table): pass

    def check_if_pset_allready_exists(self, pset_name, active_object): pass

    def clear_table(self): pass

    def create_context_menu(self, global_pos, function_list): pass

    def create_property_set(self, name, obj, parent): pass

    def delete_table_pset(self): pass

    def get_active_property_set(self): pass

    def get_attribute_by_name(self, property_set, name): pass

    def get_existing_psets_in_table(self, table): pass

    def get_inheritable_property_sets(self, obj): pass

    def get_property_set_from_item(self, item): pass

    def get_property_set_from_row(self, row, table): pass

    def get_property_sets(self): pass

    def get_pset_from_index(self, index): pass

    def get_pset_from_item(self, item): pass

    def get_pset_properties(self): pass

    def get_row_from_pset(self, property_set): pass

    def get_selecte_property_set_from_table(self): pass

    def get_table(self): pass

    def pset_table_is_editing(self): pass

    def remove_property_sets_from_table(self, property_sets, table): pass

    def rename_table_pset(self): pass

    def select_property_set(self, property_set): pass

    def set_active_property_set(self, property_set): pass

    def set_enabled(self, enabled): pass

    def set_pset_name_by_row(self, pset, row, table): pass

    def update_completer(self, obj): pass

    def update_property_set_table(self, table): pass

    def update_table_row(self, table, row): pass


class PropertySetWindow:
    def add_value_line(self, column_count, window): pass

    def bring_window_to_front(self, window): pass

    def clear_values(self, window): pass

    def close_property_set_window(self, window): pass

    def connect_window_triggers(self, window): pass

    def create_window(self, property_set): pass

    def fill_window_title(self, window, property_set): pass

    def fill_window_ui(self, window): pass

    def format_values(self, value_list, window): pass

    def get_active_attribute(self, window): pass

    def get_allowed_data_types(self): pass

    def get_allowed_value_types(self): pass

    def get_attribute_data(self, window): pass

    def get_attribute_name_input(self, window): pass

    def get_data_type(self, window): pass

    def get_inherit_checkbox_state(self, window): pass

    def get_input_value_lines(self, window): pass

    def get_paste_text_list(self): pass

    def get_properties(self): pass

    def get_property_set_by_window(self, window): pass

    def get_required_column_count(self, window): pass

    def get_seperator_state(self, window): pass

    def get_table(self, window): pass

    def get_value_type(self, window): pass

    def get_values(self, window): pass

    def get_window_by_property_set(self, property_set): pass

    def remove_data_type_restriction(self, window): pass

    def restrict_data_type_to_numbers(self, window): pass

    def set_active_window(self, window): pass

    def set_add_button_enabled(self, enabled, window): pass

    def set_add_button_text(self, text, window): pass

    def set_attribute_name(self, name, window): pass

    def set_data_type(self, data_type, window): pass

    def set_description(self, description, window): pass

    def set_inherit_checkbox_state(self, state, window): pass

    def set_seperator(self, window): pass

    def set_value_columns(self, column_count, window): pass

    def set_value_type(self, value_type, window): pass

    def set_values(self, attribute, window): pass

    def toggle_comboboxes(self, attribute, window): pass

    def update_add_button(self, window): pass

    def update_line_validators(self, window): pass

    def value_to_string(self, value): pass


class Search:
    def activate_item(self): pass

    def check_row(self, table, search_text, row, column_count): pass

    def create_table_items(self): pass

    def fill_dialog(self): pass

    def get_column_texts(self): pass

    def get_dialog(self): pass

    def get_search_mode(self): pass

    def get_search_properties(self): pass

    def refresh_dialog(self): pass

    def search_attribute(self): pass

    def search_object(self): pass


class Settings:
    def _get_path(self, value): pass

    def _set_path(self, path, value): pass

    def get_export_path(self): pass

    def get_ifc_path(self): pass

    def get_issue_path(self): pass

    def get_open_path(self): pass

    def get_save_path(self): pass

    def get_seperator(self): pass

    def get_seperator_status(self): pass

    def set_export_path(self, path): pass

    def set_ifc_path(self, path): pass

    def set_issue_path(self, path): pass

    def set_open_path(self, path): pass

    def set_save_path(self, path): pass

    def set_seperator(self, value): pass

    def set_seperator_status(self, value): pass


class Util:
    pass


class Exports:
    pass
