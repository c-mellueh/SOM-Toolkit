class Popups:
    def create_warning_popup(self, text):    pass


class MainWindow:
    pass

class Attribute:
    pass

class PropertySet:
    def get_property_sets(self): pass

class Search:
    def activate_item(self): pass

    def check_row(self, table, search_text, row, column_count): pass

    def create_table_items(self): pass

    def fill_dialog(self): pass

    def get_dialog(self): pass

    def get_search_mode(self): pass

    def get_search_properties(self): pass

    def refresh_dialog(self): pass

    def search_object(self): pass


class Object:
    def add_context_menu_entry(self, name, function, single, multi): pass

    def add_ifc_mapping(self, mapping): pass

    def autofit_tree(self): pass

    def change_object_info(self, obj, data_dict): pass

    def clear_context_menu_list(self): pass

    def collapse_selection(self): pass

    def copy_object(self, obj, data_dict): pass

    def create_context_menu(self): pass

    def create_ifc_completer(self): pass

    def create_item(self, obj): pass

    def create_object(self, data_dict): pass

    def delete_object(self, obj, recursive): pass

    def delete_selection(self): pass

    def drop_indication_pos_is_on_item(self): pass

    def expand_selection(self): pass

    def expand_to_item(self, item): pass

    def fill_object_entry(self, obj): pass

    def fill_object_tree(self, objects, parent_item): pass

    def find_attribute(self, obj, pset_name, attribute_name): pass

    def get_active_object(self): pass

    def get_existing_abbriviations(self): pass

    def get_existing_ident_values(self): pass

    def get_ifc_mappings(self): pass

    def get_item_from_object(self, obj): pass

    def get_item_from_pos(self, pos): pass

    def get_object_from_item(self, item): pass

    def get_object_info_properties(): pass

    def get_object_tree(self): pass

    def get_selected_items(self): pass

    def get_selected_objects(self): pass

    def group_objects(self, parent, children): pass

    def group_selection(self): pass

    def handle_attribute_issue(self, result): pass

    def is_abbreviation_allowed(self, abbreviation, ignore): pass

    def is_identifier_allowed(self, identifier, ignore): pass

    def oi_change_visibilit_identifiers(self, hide): pass

    def oi_create_dialog(self): pass

    def oi_fill_properties(self, mode): pass

    def oi_get_focus_object(self): pass

    def oi_get_mode(self): pass

    def oi_get_values(self): pass

    def oi_set_abbrev_value_color(self, color): pass

    def oi_set_ident_value_color(self, color): pass

    def set_values(self, data_dict): pass

    def oi_update_attribute_combobox(self): pass

    def oi_update_dialog(self): pass

    def resize_tree(self): pass

    def select_object(self, obj): pass

    def set_active_object(self, obj): pass

    def set_ident_value(self, obj, value): pass

    def update_check_state(self, item): pass

    def update_item(self, item, obj): pass


class UseCase:
    def add_use_case(self, use_case_name): pass

    def add_use_case_to_settings_window(self): pass

    def create_context_menu(self, global_pos, action_dict): pass

    def create_row(self, entity, use_case_list): pass

    def create_tree(self, entities, parent_item, use_case_list, pre_header_text_length, model): pass

    def create_tree_models(self): pass

    def delete_use_case_window(self): pass

    def fill_object_tree(self): pass

    def get_active_object(self): pass

    def get_active_use_case(self): pass

    def get_attribute_dict(self): pass

    def get_check_statuses(self, index): pass

    def get_enabled_statuses(self, index): pass

    def get_header_texts(self): pass

    def get_index_by_object(self, obj): pass

    def get_linked_data(self, index): pass

    def get_new_use_case_name(self, standar_name, existing_names): pass

    def get_object_dict(self): pass

    def get_object_model(self): pass

    def get_object_tree(self): pass

    def get_pset_dict(self): pass

    def get_pset_model(self): pass

    def get_title_count_by_index(self, index): pass

    def get_title_length_by_model(self, model): pass

    def get_use_case_list(self): pass

    def get_use_case_state(self, use_case_name, entity): pass

    def is_object_enabled(self, index): pass

    def is_tree_clicked(self): pass

    def load_use_cases(self): pass

    def remove_use_case(self, use_case_index): pass

    def rename_use_case(self, use_case_index, new_name): pass

    def request_rename_use_case_name(self, old_name): pass

    def reset_use_case_data(self): pass

    def resize_tree(self): pass

    def set_active_object(self, obj): pass

    def set_header_labels(self, model, labels): pass

    def set_use_case(self, value): pass

    def toggle_checkstate(self, index): pass

    def tree_activate_click_drag(self, index): pass

    def tree_move_click_drag(self, index): pass

    def tree_release_click_drag(self, index): pass

    def update_active_object_label(self): pass

    def update_attribute_data(self): pass

    def update_attribute_use_cases(self): pass

    def update_enable_status(self, item, model): pass

    def update_object_data(self, obj): pass

    def update_object_use_cases(self): pass

    def update_project_use_cases(self): pass

    def update_pset_data(self): pass

    def update_pset_tree(self): pass

    def update_pset_use_cases(self): pass

    def set_active_use_case(self, value): pass


class Project:
    def add_project_setting(self, get_function, set_function, name, options): pass

    def add_setting_to_dialog(self, setting_dict): pass

    def add_shortcut(self, sequence, window, function): pass

    def create_project(self): pass

    def create_project_infos(self): pass

    def get(self): pass

    def get_all_objects(self): pass

    def get_path(self, title, file_text): pass

    def get_project_author(self): pass

    def get_project_infos(self): pass

    def get_project_name(self): pass

    def get_project_phase(self): pass

    def get_project_pase_list(self): pass

    def get_project_version(self): pass

    def get_root_objects(self, filter): pass

    def load_project(self, path): pass

    def refresh_info_dict(self, info_dict, index): pass

    def reset_project_infos(self): pass

    def set_project_author(self, author): pass

    def set_project_name(self, name): pass

    def set_project_phase(self, phase): pass

    def set_project_version(self): pass

    def update_setting(self, info_dict): pass


class Settings:
    def get_open_path(self): pass

    def set_open_path(self, path): pass

    def set_save_path(self, path): pass
