from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar

import SOMcreator
import som_gui.core.tool
from SOMcreator.exporter.IDS import main
from SOMcreator.exporter.bim_collab_zoom import modelcheck as bc_modelcheck
from SOMcreator.exporter.desite import modelcheck
from som_gui import tool
from som_gui.module.modelcheck_external import trigger, ui

if TYPE_CHECKING:
    from som_gui.module.modelcheck_external.prop import ModelcheckExternalProperties


class ModelcheckExternal(som_gui.core.tool.ModelcheckExternal):
    @classmethod
    def get_properties(cls) -> ModelcheckExternalProperties:
        return som_gui.ModelcheckExternalProperties

    @classmethod
    def set_action(cls, name: str, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name):
        return cls.get_properties().actions[name]

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
        prop.window.ui.buttonBox.rejected.connect(trigger.close_window)
        return prop.window

    @classmethod
    def create_menubar(cls, window: QMainWindow):

        menu_bar = list()
        js_text = QCoreApplication.translate("Modelcheck", "Export Javascript Rules")
        jsf_text = QCoreApplication.translate(
            "Modelcheck", "Export Javascript (fast Check)"
        )
        ar_text = QCoreApplication.translate("Modelcheck", "Export Property Rules")
        csv_text = QCoreApplication.translate("Modelcheck", "Export Modelcheck-CSV")

        desite_menu = [
            [js_text, cls.export_desite_js],
            [jsf_text, cls.export_desite_fast],
            [ar_text, cls.export_desite_property_table],
            [csv_text, cls.export_desite_csv],
        ]

        desite_text = QCoreApplication.translate("Modelcheck", "Desite MD Pro")
        menu_bar.append([desite_text, desite_menu])

        sm_text = QCoreApplication.translate("Modelcheck", "Export SmartViews")
        bim_collab_text = QCoreApplication.translate("Modelcheck", "BIMcollab ZOOM")
        menu_bar.append([bim_collab_text, [[sm_text, cls.export_bimcollab]]])

        ids_text = QCoreApplication.translate("Modelcheck", "Export IDS")
        building_smart_text = QCoreApplication.translate("Modelcheck", "buildingSMART")
        menu_bar.append([building_smart_text, [[ids_text, cls.export_ids]]])

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
    def get_main_property(cls) -> tuple[str, str]:
        widget = cls.get_window().ui.main_property_widget
        return widget.ui.le_pset_name.text(), widget.ui.le_property_name.text()

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
    def export_desite_fast(cls):
        pset_name, property_name = cls.get_main_property()
        file_format = "Desite QA-XML (*.qa.xml);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return

        data_dict = cls.get_data_dict()
        modelcheck.fast_check(
            tool.Project.get(), pset_name, property_name, data_dict, path
        )

    @classmethod
    def export_desite_csv(cls):
        file_format = "CSV (*.csv);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return
        data_dict = cls.get_data_dict()
        modelcheck.csv_export(data_dict, path)

    @classmethod
    def export_desite_js(cls):
        pset_name, property_name = cls.get_main_property()

        file_format = "Desite QA-XML (*.qa.xml);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return
        data_dict = cls.get_data_dict()
        class_structure = cls._build_tree()
        modelcheck.export(
            tool.Project.get(),
            data_dict,
            path,
            main_pset=pset_name,
            main_property=property_name,
            class_structure=class_structure,
        )

    @classmethod
    def export_desite_property_table(cls):
        pset_name, property_name = cls.get_main_property()

        file_format = "Desite QA-XML (*.qa.xml);;all (*.*)"
        path = tool.Popups.get_save_path(file_format, cls.get_window())
        if not path:
            return

        data_dict = cls.get_data_dict()
        project = tool.Project.get()
        modelcheck.export(
            project,
            data_dict,
            path,
            main_pset=pset_name,
            main_property=property_name,
            class_structure=cls._build_tree(),
            export_type=modelcheck.TABLE_EXPORT,
        )

    @classmethod
    def _build_tree(cls) -> dict[SOMcreator.SOMClass, SOMcreator.SOMClass]:
        return {obj: obj.parent for obj in tool.Project.get().get_classes(filter=False)}
