import som_gui.core.tool
import SOMcreator
import som_gui
from som_gui.module.project.prop import ProjectProperties, InfoDict
from som_gui.module.project.constants import VERSION, AUTHOR, NAME, PROJECT_PHASE
from PySide6.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel
from typing import Callable


class Project(som_gui.core.tool.Project):
    @classmethod
    def get_project_phase_list(cls):
        proj = cls.get()
        return proj.get_project_phase_list()

    @classmethod
    def reset_project_infos(cls):
        prop: ProjectProperties = som_gui.ProjectProperties
        prop.project_infos = list()

    @classmethod
    def add_project_info(cls, get_function: Callable, set_function: Callable, name: str,
                         options: Callable | None = None):
        value = get_function()
        d = {"set_function": set_function, "display_name": name, "value": str(value),
             "get_function": get_function}
        if options is not None:
            d["options"] = options

        prop: ProjectProperties = som_gui.ProjectProperties
        prop.project_infos.append(d)

    @classmethod
    def update_project_version(cls):
        prop: ProjectProperties = som_gui.ProjectProperties
        proj = cls.get()
        for info_dict in prop.project_infos:
            if info_dict["display_name"] == VERSION:
                proj.version = info_dict["value"]

    @classmethod
    def update_project_author(cls):
        prop: ProjectProperties = som_gui.ProjectProperties
        proj = cls.get()
        for info_dict in prop.project_infos:
            if info_dict["display_name"] == AUTHOR:
                proj.author = info_dict["value"]

    @classmethod
    def update_project_name(cls):
        prop: ProjectProperties = som_gui.ProjectProperties
        proj = cls.get()
        for info_dict in prop.project_infos:
            if info_dict["display_name"] == NAME:
                proj.name = info_dict["value"]

    @classmethod
    def update_project_phase(cls):
        prop: ProjectProperties = som_gui.ProjectProperties
        proj = cls.get()
        for info_dict in prop.project_infos:
            if info_dict["display_name"] == PROJECT_PHASE:
                proj.current_project_phase = info_dict["value"]

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
    def load_project(cls, path: str):

        print("Load Project")
        prop: ProjectProperties = som_gui.ProjectProperties
        proj = SOMcreator.Project()
        project_dict = proj.open(path)
        prop.active_project = proj

        cls.add_project_info(cls.get_project_version, cls.update_project_version, VERSION)
        cls.add_project_info(cls.get_project_author, cls.update_project_author, AUTHOR)
        cls.add_project_info(cls.get_project_name, cls.update_project_name, NAME)
        cls.add_project_info(cls.get_project_phase, cls.update_project_phase, PROJECT_PHASE, cls.get_project_phase_list)
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
    def get_project_info_options(cls):
        prop: ProjectProperties = som_gui.ProjectProperties

    @classmethod
    def add_setting_to_dialog(cls, info_dict: InfoDict):
        value = info_dict["value"]
        prop: ProjectProperties = som_gui.ProjectProperties
        layout: QFormLayout = prop.settings_window.layout()
        dialog = prop.settings_window
        if "options" in info_dict:
            option = info_dict["options"]()
            edit = QComboBox(dialog)
            edit.addItems(option)
            edit.setCurrentText(value)
        else:
            edit = QLineEdit(dialog)
            edit.setText(value)
        layout.insertRow(layout.rowCount() - 1, info_dict["display_name"], edit)

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
        info_dict["set_function"]()
