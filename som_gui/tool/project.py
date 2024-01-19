import logging

import som_gui.core.tool
import SOMcreator
import som_gui
from som_gui.module.project.prop import ProjectProperties, InfoDict
from som_gui.module.project.constants import VERSION, AUTHOR, NAME, PROJECT_PHASE
from PySide6.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel, QWidget
from PySide6.QtGui import QShortcut, QKeySequence
from typing import Callable
from som_gui import tool
import os
from PySide6.QtWidgets import QFileDialog


class Project(som_gui.core.tool.Project):

    @classmethod
    def add_shortcut(cls, sequence: str, window: QWidget, function: Callable):
        prop: ProjectProperties = som_gui.ProjectProperties
        shortcut = QShortcut(QKeySequence(sequence), window)
        if not hasattr(prop, "shortcuts"):
            prop.shourtcuts = list()
        prop.shourtcuts.append(shortcut)
        shortcut.activated.connect(function)

    @classmethod  # TODO: Move to Filehandling Module
    def get_path(cls, title: str, file_text: str) -> str:
        main_window = som_gui.MainUi.window
        cur_path = tool.Settings.get_open_path()
        if not os.path.exists(cur_path):
            cur_path = os.getcwd() + "/"
        return QFileDialog.getOpenFileName(main_window, title, str(cur_path), file_text)[0]

    @classmethod
    def create_project(cls):

        proj = SOMcreator.Project()
        prop: ProjectProperties = som_gui.ProjectProperties
        prop.active_project = proj
        prop.project_infos = list()
        cls.create_project_infos()
        som_gui.on_new_project()

    @classmethod
    def get_project_phase_list(cls):
        proj = cls.get()
        return proj.get_project_phase_list()

    @classmethod
    def reset_project_infos(cls):
        prop: ProjectProperties = som_gui.ProjectProperties
        prop.project_infos = list()

    @classmethod
    def add_project_setting(cls, get_function: Callable, set_function: Callable, name: str,
                            options: Callable | None = None):
        value = get_function()
        d = {"set_function": set_function, "display_name": name, "value": str(value),
             "get_function": get_function}
        if options is not None:
            d["options"] = options

        prop: ProjectProperties = som_gui.ProjectProperties
        prop.project_infos.append(d)

    @classmethod
    def set_project_version(cls, version: str):
        proj = cls.get()
        proj.version = version

    @classmethod
    def set_project_author(cls, author: str):
        proj = cls.get()
        proj.author = author

    @classmethod
    def set_project_name(cls, name: str):
        proj = cls.get()
        proj.name = name

    @classmethod
    def set_project_phase(cls, phase: str):
        proj = cls.get()
        proj.current_project_phase = phase

    @classmethod
    def get_project_version(cls):
        proj = cls.get()
        return proj.version

    @classmethod
    def get_project_author(cls):
        proj = cls.get()
        return proj.author

    @classmethod
    def get_project_name(cls):
        proj = cls.get()
        return proj.name

    @classmethod
    def get_project_phase(cls):
        proj = cls.get()
        return proj.current_project_phase

    @classmethod
    def create_project_infos(cls):
        logging.debug(f"Create Project Infos")
        cls.add_project_setting(cls.get_project_version, cls.set_project_version, VERSION)
        cls.add_project_setting(cls.get_project_author, cls.set_project_author, AUTHOR)
        cls.add_project_setting(cls.get_project_name, cls.set_project_name, NAME)
        cls.add_project_setting(cls.get_project_phase, cls.set_project_phase, PROJECT_PHASE,
                                cls.get_project_phase_list)

    @classmethod
    def load_project(cls, path: str):
        from som_gui.filehandling.open_file import import_node_pos, fill_ui
        logging.info("Load Project")
        main_window = som_gui.MainUi.window
        tool.Settings.set_open_path(path)
        tool.Settings.set_save_path(path)
        prop: ProjectProperties = som_gui.ProjectProperties
        proj = SOMcreator.Project()
        project_dict = proj.open(path)
        prop.active_project = proj
        cls.create_project_infos()
        som_gui.on_new_project()
        main_window.project, main_dict = proj, project_dict
        import_node_pos(main_dict, main_window.graph_window)
        fill_ui(main_window)
        main_window.generate_window_title()
        main_window.graph_window.create_missing_scenes()
        return proj, project_dict

    @classmethod
    def get(cls) -> SOMcreator.Project:
        return som_gui.ProjectProperties.active_project

    @classmethod
    def get_all_objects(cls) -> list[SOMcreator.Object]:
        proj: SOMcreator.Project = som_gui.ProjectProperties.active_project
        return list(proj.get_all_objects())

    @classmethod
    def get_root_objects(cls, filter=True):
        proj: SOMcreator.Project = som_gui.ProjectProperties.active_project
        if proj is None:
            return []
        if filter:
            return [obj for obj in proj.objects if obj.parent is None]
        else:
            return [obj for obj in proj.get_all_objects() if obj.parent is None]

    @classmethod
    def get_project_infos(cls):
        prop: ProjectProperties = som_gui.ProjectProperties
        return prop.project_infos

    @classmethod
    def add_setting_to_dialog(cls, setting_dict: InfoDict):
        value = setting_dict["value"]
        prop: ProjectProperties = som_gui.ProjectProperties
        layout: QFormLayout = prop.settings_window.layout()
        dialog = prop.settings_window
        if "options" in setting_dict:
            option = setting_dict["options"]()
            edit = QComboBox(dialog)
            edit.addItems(option)
            edit.setCurrentText(value)
        else:
            edit = QLineEdit(dialog)
            edit.setText(value)
        layout.insertRow(layout.rowCount() - 1, setting_dict["display_name"], edit)

    @classmethod
    def refresh_info_dict(cls, info_dict: InfoDict, index):
        prop: ProjectProperties = som_gui.ProjectProperties
        layout_item = prop.settings_window.layout().itemAt(index, QFormLayout.FieldRole)
        widget = layout_item.widget()
        if isinstance(widget, QComboBox):
            value = widget.currentText()
        elif isinstance(widget, QLineEdit):
            value = widget.text()
        else:
            return
        info_dict["value"] = value

    @classmethod
    def update_setting(cls, info_dict: InfoDict):
        value = info_dict["value"]
        # TODO: add value to set function
        info_dict["set_function"](value)
