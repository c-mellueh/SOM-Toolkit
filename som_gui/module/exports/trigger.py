from som_gui import tool
from som_gui.core import exports as core


def connect():
    tool.MainWindow.add_action("Datei/Export/Vestra",
                               lambda: core.export_vestra_mapping(tool.Exports, tool.MainWindow, tool.Project,
                                                                  tool.Settings))
    tool.MainWindow.add_action("Datei/Export/Card1",
                               lambda: core.export_card_1(tool.Exports, tool.MainWindow, tool.Project, tool.Settings))
    tool.MainWindow.add_action("Datei/Export/Excel",
                               lambda: core.export_excel(tool.Exports, tool.MainWindow, tool.Project, tool.Settings,
                                                         tool.Popups))
    tool.MainWindow.add_action("Datei/Export/Allplan",
                               lambda: core.export_allplan_excel(tool.Exports, tool.MainWindow, tool.Project,
                                                                 tool.Popups, tool.Settings))
    tool.MainWindow.add_action("Datei/Export/Abkürzungen",
                               lambda: core.export_desite_abbreviation(tool.Exports, tool.MainWindow, tool.Project,
                                                                       tool.Settings, tool.Popups))
    tool.MainWindow.add_action("Desite/Lesezeichen",
                               lambda: core.export_bookmarks(tool.Exports, tool.MainWindow, tool.Project, tool.Popups))
    tool.MainWindow.add_action("Desite/Mapping Script",
                               lambda: core.export_mapping_script(tool.Exports, tool.MainWindow, tool.Project,
                                                                  tool.Popups, tool.Settings))


def on_new_project():
    pass
