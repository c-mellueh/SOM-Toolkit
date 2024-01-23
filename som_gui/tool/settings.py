import som_gui.core.tool
import som_gui.settings as settings

PATHS_SECTION = "paths"
OPEN_PATH = "open_path"
SAVE_PATH = "save_path"
EXPORT_PATH = "export_path"
IFC_PATH = "ifc_path"
ISSUE_PATH = "issue_path"
SEPERATOR_SECTION = "seperator"
SEPERATOR_STATUS = "seperator_status"
SEPERATOR = "seperator"
GROUP_FOLDER = "group_folder_path"
ATTRIBUTE_IMPORT_SECTION = "attribute_import"
EXISTING_ATTRIBUTE_IMPORT = "existing"
REGEX_ATTRIBUTE_IMPORT = "regex"
RANGE_ATTRIBUTE_IMPORT = "range"
COLOR_ATTTRIBUTE_IMPORT = "color"
PATH_SEPERATOR = " ;"
IFC_MOD = "ifc_modification"
GROUP_PSET = "group_pset"
GROUP_ATTRIBUTE = "group_attribute"
CREATE_EMPTY = "create_empty"


class Settings(som_gui.core.tool.Settings):
    @classmethod
    def get_open_path(self):
        return settings._get_path(OPEN_PATH)

    @classmethod
    def set_open_path(cls, path):
        settings._set_path(OPEN_PATH, path)

    @classmethod
    def set_save_path(cls, path):
        settings._set_path(SAVE_PATH, path)

    @classmethod
    def get_seperator(cls) -> str:
        return settings._get_string_setting(SEPERATOR_SECTION, SEPERATOR, ",")

    @classmethod
    def set_seperator_status(cls, value: bool) -> None:
        settings.set_setting(SEPERATOR_SECTION, SEPERATOR_STATUS, value)

    @classmethod
    def set_seperator(cls, value: str) -> None:
        settings.set_setting(SEPERATOR_SECTION, SEPERATOR, value)

    @classmethod
    def get_seperator_status(cls) -> bool:
        return settings._get_bool_setting(SEPERATOR_SECTION, SEPERATOR_STATUS)
