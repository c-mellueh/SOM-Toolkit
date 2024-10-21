from som_gui import tool
from som_gui.core import exports as core
from . import ui

def connect():
    tool.MainWindow.add_action("Datei/Export/Vestra",
                               lambda: core.export_vestra_mapping(tool.Exports, tool.MainWindow, tool.Project,
                                                                  tool.Appdata))
    tool.MainWindow.add_action("Datei/Export/Card1",
                               lambda: core.export_card_1(tool.Exports, tool.MainWindow, tool.Project, tool.Appdata))
    tool.MainWindow.add_action("Datei/Export/Excel",
                               lambda: core.export_excel(tool.Exports, tool.MainWindow, tool.Project, tool.Appdata,
                                                         tool.Popups))
    tool.MainWindow.add_action("Datei/Export/Allplan",
                               lambda: core.export_allplan_excel(tool.Exports, tool.MainWindow, tool.Project,
                                                                 tool.Popups, tool.Appdata))
    tool.MainWindow.add_action("Datei/Export/Abkürzungen",
                               lambda: core.export_desite_abbreviation(tool.MainWindow, tool.Project,
                                                                       tool.Appdata, tool.Popups))
    tool.MainWindow.add_action("Desite/Lesezeichen",
                               lambda: core.export_bookmarks(tool.Exports, tool.MainWindow, tool.Project, tool.Popups,
                                                             tool.Appdata))
    tool.MainWindow.add_action("Desite/Mapping Script",
                               lambda: core.export_mapping_script(tool.Exports, tool.MainWindow, tool.Project,
                                                                  tool.Popups, tool.Appdata))
    tool.Settings.add_page_to_toolbox(lambda: core.create_settings_ui(tool.Exports, tool.Appdata), "Path", "Export",
                                      lambda: core.settings_accepted(tool.Exports, tool.Appdata))


def retranslate_ui():
    pass
def on_new_project():
    pass
