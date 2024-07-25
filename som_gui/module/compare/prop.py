import SOMcreator
from SOMcreator import Project
class CompareProperties():
    projects = [None, None]
    uuid_dicts = [None, None]
    ident_dicts = [None, None]
    window = None
    object_dicts = [None, None]
    missing_objects: list[list[SOMcreator.Object]] = [None, None]
    object_tree_item_dict = dict()
