from __future__ import annotations
from typing import TYPE_CHECKING, Type
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QStandardItemModel

if TYPE_CHECKING:
    from som_gui import tool


def create_main_menu_actions(modelcheck_external: Type[tool.ModelcheckExternal], main_window: Type[tool.MainWindow]):
    from som_gui.module.modelcheck_external import trigger
    open_window_action = main_window.add_action("menuExport", "modelcheck", trigger.open_window)
    modelcheck_external.set_action("open_window", open_window_action)


def retranslate_ui(modelcheck_external: Type[tool.ModelcheckExternal], util: Type[tool.Util]):
    open_window_action = modelcheck_external.get_action("open_window")
    title = QCoreApplication.translate("Modelcheck", "Modelcheck")

    open_window_action.setText(title)
    if modelcheck_external.get_window() is None:
        return

    window = modelcheck_external.get_window()
    window.ui.retranslateUi(window)
    window.setWindowTitle(util.get_window_title(title))
    window.menuBar().clear()
    modelcheck_external.create_menubar(window)
    object_model: QStandardItemModel = window.ui.object_tree.model()
    headers = [QCoreApplication.translate("Modelcheck", "Object"),
               QCoreApplication.translate("Modelcheck", "Identifier")]
    object_model.setHorizontalHeaderLabels(headers)

    pset_model: QStandardItemModel = window.ui.property_set_tree.model()
    headers = [QCoreApplication.translate("Modelcheck", "PropertySet,Attribute")]
    pset_model.setHorizontalHeaderLabels(headers)


def open_window(modelcheck_external: Type[tool.ModelcheckExternal], modelcheck_window: Type[tool.ModelcheckWindow]):
    window = modelcheck_external.create_window()
    modelcheck_window.get_properties().property_set_tree = window.ui.property_set_tree
    modelcheck_window.get_properties().object_tree = window.ui.object_tree
    modelcheck_window.get_properties().object_label = window.ui.label_object

    modelcheck_external.create_menubar(window)
    from som_gui.module.modelcheck_external import trigger
    trigger.retranslate_ui()
    window.show()


def close_window(modelcheck_external: Type[tool.ModelcheckExternal]):
    modelcheck_external.get_window().close()
    modelcheck_external.get_window().hide()
