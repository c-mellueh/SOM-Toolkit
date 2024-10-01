from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class ProjectFilter:
    name: str
    long_name: str = field(compare=False)
    description: str = field(compare=False)
    filter_type: int = field(init=False)  # 0 = UseCase ,1 = Phase


class UseCase(ProjectFilter):
    filter_type = 0


class Phase(ProjectFilter):
    filter_type = 1
