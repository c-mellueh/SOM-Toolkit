from dataclasses import dataclass
from som_gui.tool.project import Project
import SOMcreator

import som_gui


def refresh():
    UseCaseData.is_loaded = False


@dataclass
class UseCaseData:
    data = {}
    is_loaded = False

    @classmethod
    def load(cls):
        cls.data["data_classes"] = cls.load_data_classes()

    @classmethod
    def load_data_classes(cls):
        proj: SOMcreator.Project = som_gui.ProjectProperties.active_project
        if proj is None:
            return list()
        use_case_list = proj.get_use_case_list()
        return use_case_list


