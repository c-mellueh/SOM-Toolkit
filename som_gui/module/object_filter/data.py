from dataclasses import dataclass
import SOMcreator

import som_gui


def refresh():
    ObjectFilterData.is_loaded = False


@dataclass
class ObjectFilterData:
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


