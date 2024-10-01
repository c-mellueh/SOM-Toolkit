from __future__ import annotations
from typing import TYPE_CHECKING

import SOMcreator

import som_gui.core.tool
from som_gui.module.modelcheck_external import ui
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu

from som_gui import tool
from SOMcreator.external_software.IDS import main
from SOMcreator.io.bim_collab_zoom import modelcheck as bc_modelcheck
from SOMcreator.io.desite import modelcheck

if TYPE_CHECKING:
    from som_gui.module.modelcheck_external.prop import ModelcheckExternalProperties

class ModelcheckExternal(som_gui.core.tool.ModelcheckExternal):
    @classmethod
    def get_properties(cls) -> ModelcheckExternalProperties:
        return som_gui.ModelcheckExternalProperties

    @classmethod
    def is_window_allready_build(cls):
        return bool(cls.get_properties().window)

    @classmethod
    def get_window(cls) -> ui.ModelcheckExternalWindow:
        return cls.get_properties().window

    @classmethod
    def create_window(cls):
        prop = cls.get_properties()
        prop.window = ui.ModelcheckExternalWindow()
        return prop.window

    @classmethod
    def create_menubar(cls, window: QMainWindow, main_pset_name: str, main_attribute_name: str):
        desite_menu = [["Export Javascript Regeln", lambda: cls.export_desite_js(main_pset_name, main_attribute_name)],
                       ["Export Javascript (schnelle Prüfung)",
                        lambda: cls.export_desite_fast(main_pset_name, main_attribute_name)],
                       ["Export Attribut Regeln",
                        lambda: cls.export_desite_attribute_table(main_pset_name, main_attribute_name)],
                       ["Export Modelcheck-CSV", lambda: cls.export_desite_csv()]
                       ]

        bim_collab_menu = [["SmartViews exportieren", cls.export_bimcollab]]

        building_smart_menu = [["IDS exportieren", cls.export_ids]]

        menu_bar = [["Desite MD Pro", desite_menu], ["BIMcollab ZOOM", bim_collab_menu],
                    ["buildingSMART", building_smart_menu]]

        qt_menu_bar = QMenuBar()
        window.setMenuBar(qt_menu_bar)
        for name, menu_list in menu_bar:
            menu = QMenu(qt_menu_bar)
            menu.setTitle(name)
            qt_menu_bar.addAction(menu.menuAction())

            for action_name, action_function in menu_list:
                action = QAction(window)
                action.setText(action_name)
                menu.addAction(action)
                action.triggered.connect(action_function)

    @classmethod
    def get_data_dict(cls):
        check_state_dict = tool.ModelcheckWindow.get_item_checkstate_dict()
        data_dict = tool.Modelcheck.build_data_dict(check_state_dict)
        return data_dict

    @classmethod
    def export_ids(cls):
        file_format = "IDS (*.ids);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return
        data_dict = cls.get_data_dict()
        main.export(tool.Project.get(), data_dict, path)

    @classmethod
    def export_bimcollab(cls):
        file_format = "BIMcollab-SmartView (*.bcsv);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return
        data_dict = cls.get_data_dict()
        bc_modelcheck.export(data_dict, path, tool.Project.get().author)

    @classmethod
    def export_desite_fast(cls, pset_name: str, attribute_name: str):
        file_format = "Desite QA-XML (*.qa.xml);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return

        data_dict = cls.get_data_dict()
        modelcheck.fast_check(tool.Project.get(), pset_name, attribute_name, data_dict, path)

    @classmethod
    def export_desite_csv(cls):
        file_format = "CSV (*.csv);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return
        data_dict = cls.get_data_dict()
        modelcheck.csv_export(data_dict, path)

    @classmethod
    def export_desite_js(cls, main_pset_name, main_attribute_name):
        file_format = "Desite QA-XML (*.qa.xml);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return
        data_dict = cls.get_data_dict()
        modelcheck.export(tool.Project.get(), data_dict, path, main_pset=main_pset_name,
                          main_attribute=main_attribute_name,
                          object_structure=cls._build_tree())

    @classmethod
    def export_desite_attribute_table(cls, main_pset_name: str, main_attribute_name: str):
        file_format = "Desite QA-XML (*.qa.xml);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return

        data_dict = cls.get_data_dict()
        project = tool.Project.get()
        modelcheck.export(project, data_dict, path, main_pset=main_pset_name, main_attribute=main_attribute_name,
                          object_structure=cls._build_tree(),
                          export_type=modelcheck.TABLE_EXPORT)

    @classmethod
    def _build_tree(cls) -> dict[SOMcreator.Object, set[SOMcreator.Object]]:
        return {obj: set(obj.get_children(filter=True)) for obj in tool.Project.get().get_objects(filter=False)}
