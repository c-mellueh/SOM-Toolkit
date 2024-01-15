import som_gui.core.tool
import SOMcreator
import som_gui


class Project(som_gui.core.tool.Project):
    @classmethod
    def load_project(cls, path: str):
        proj = SOMcreator.Project()
        proj.open(path)
        som_gui.ProjectProperties.active_project = proj
        return proj

    @classmethod
    def get(cls) -> SOMcreator.Project:
        return som_gui.ProjectProperties.active_project
