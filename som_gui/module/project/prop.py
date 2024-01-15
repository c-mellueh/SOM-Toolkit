from dataclasses import dataclass
from SOMcreator import Project


@dataclass
class ProjectProperties:
    active_project: Project
    project_name: str
    author: str
    version: str
