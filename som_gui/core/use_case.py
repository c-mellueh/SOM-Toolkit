from som_gui.tool.use_case import UseCase


def create_use_case(use_case_tool: UseCase):
    use_case_tool.create_use_case("Test")


def load_use_cases(use_case_tool: UseCase):
    use_case_tool.load_use_cases()
