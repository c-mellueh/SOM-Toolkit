import som_gui.core.tool
import SOMcreator
import som_gui


class Project(som_gui.core.tool.Project):
    @classmethod
    def load_project(cls, path: str):
        proj = SOMcreator.Project()
        project_dict = proj.open(path)
        som_gui.ProjectProperties.active_project = proj
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
        if filter:
            return [obj for obj in proj.objects if obj.parent is None]
        else:
            return [obj for obj in proj.get_all_objects() if obj.parent is None]
