from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Type
from som_gui import tool
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPalette, QStandardItem
from PySide6.QtWidgets import QLineEdit, QCompleter, QTableWidgetItem

if TYPE_CHECKING:
    from som_gui import tool
    import SOMcreator
    from som_gui.module.class_info import ui


def init(class_info: Type[tool.ClassInfo], main_window: Type[tool.MainWindow]):
    main_window.signaller.class_info_requested.connect(
        lambda som_class: class_info.trigger_class_info_widget(1, som_class)
    )


def retranslate_ui(class_info: Type[tool.ClassInfo]) -> None:
    pass


def create_class_info_widget(
    mode: int,
    som_class: SOMcreator.SOMClass,
    class_tool: Type[tool.Class],
    class_info: Type[tool.ClassInfo],
    predefined_property_set: Type[tool.PredefinedPropertySet],
    ifc_schema: Type[tool.IfcSchema],
    util: Type[tool.Util],
):
    """
    Opens Class Info Widget can be used for creation (mode 0), modification (mode 1) or copying (mode 2)
    """
    logging.debug(f"Create Class Info Widget Mode= {mode}")
    title = util.get_window_title(
        QCoreApplication.translate("Class Info", "Class Info")
    )
    if mode != 0 and not som_class:
        return
    dialog = class_info.create_dialog(title, ["IFC4_3"])
    class_info.set_active_class(som_class)
    predefined_psets = list(predefined_property_set.get_property_sets())
    class_info.connect_dialog(dialog, predefined_psets)
    class_info.oi_fill_properties(mode=mode)
    class_info.update_dialog(dialog)

    pset_names = [p.name for p in predefined_psets]
    if mode != 0:
        pset_names += list(som_class.get_properties())
    util.create_completer(pset_names, dialog.ui.combo_box_pset)

    for row, version in enumerate(ifc_schema.get_active_versions()):
        widget = ifc_schema.create_mapping_widget(som_class, version)
        dialog.ui.toolBox.addItem(widget,version)
        #dialog.ui.vertical_layout_ifc.insertWidget(row, widget)
    if dialog.exec():
        active_class = som_class
        data_dict = class_info.generate_datadict()
        if mode == 0:
            if som_class:
                data_dict["parent_uuid"] = som_class.uuid
            class_tool.signaller.create_class.emit(data_dict)
        elif mode == 1:
            class_tool.signaller.modify_class.emit(active_class, data_dict)
        elif mode == 2:
            class_tool.signaller.copy_class.emit(active_class, data_dict)
    class_info.reset()


def class_info_refresh(class_tool: Type[tool.Class], class_info: Type[tool.ClassInfo]):
    data_dict = class_info.generate_datadict()
    class_info.oi_set_values(data_dict)
    ident_value = data_dict["ident_value"]
    group = data_dict["is_group"]
    ident_filter = (
        class_info.get_active_class().ident_value
        if class_info.get_mode() == 1
        else None
    )
    if not class_tool.is_identifier_allowed(ident_value, [ident_filter]):
        class_info.oi_set_ident_value_color("red")
    else:
        class_info.oi_set_ident_value_color(QPalette().color(QPalette.Text).name())
    class_info.oi_change_visibility_identifiers(group)

