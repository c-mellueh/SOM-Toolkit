import som_gui.core.tool
import SOMcreator
import som_gui


class Project(som_gui.core.tool.Project):
    @classmethod
    def load_project(cls, path: str):
        proj = SOMcreator.Project()
        proj.open(path)
        return proj
