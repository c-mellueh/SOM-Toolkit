def refresh():
    UseCaseData.is_loaded = False


from som_gui.tool.project import Project


class UseCaseData:
    data = {}
    is_loaded = False

    @classmethod
    def load(cls):
        cls.is_loaded = True
        cls.data["available_use_cases"] = Project.get().get_use_case_list()
