from dataclasses import dataclass
from som_gui.module.use_case.ui import UseCaseWindow


@dataclass
class UseCaseProperties:
    active_use_case_index: int
    active_use_case_name: str
    use_case_list: list[str]
    use_case_window: UseCaseWindow = None
