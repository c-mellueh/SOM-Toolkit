class Search:
    pass
class Object:
    def create_object(self):
        pass
class UseCase:
    def create_use_case(self, name):
        pass

    def load_use_cases(self):
        pass

    def get_use_case_list(self):
        pass

    def set_header_labels(self,model, labels):
        pass


class Project:
    def load_project(self, path):
        pass

    def create_project(self): pass

    def get(self):
        pass

    def get_all_objects(self):
        pass

    def get_root_objects(self, filter):
        pass


class Settings:
    def get_open_path(self): pass
