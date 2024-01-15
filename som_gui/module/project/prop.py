from dataclasses import dataclass
from SOMcreator import Project


@dataclass
class ProjectProperties:
    project_name: str
    author: str
    version: str
    active_project: Project | None = None
