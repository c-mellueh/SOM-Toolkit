from dataclasses import dataclass


@dataclass
class UseCaseProperties:
    active_use_case_index: int
    active_use_case_name: str
    use_case_list = list[str]
