import logging
from typing import TYPE_CHECKING, Type
from som_gui import tool
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QPalette


def retranslate_ui(class_info: Type[tool.ClassInfo]) -> None:
    header = class_info.get_class_tree().headerItem()
    for column, name in enumerate(class_info.get_header_names()):
        header.setText(column, name)


def create_class_info_widget(
    mode: int,
    class_info: Type[tool.ClassInfo],
    predefined_property_set: Type[tool.PredefinedPropertySet],
    util: Type[tool.Util],
):
    """
    Opens Class Info Widget can be used for creation (mode 0), modification (mode 1) or copying (mode 2)
    """
    logging.debug(f"Create Class Info Widget Mode= {mode}")
    title = util.get_window_title(
        QCoreApplication.translate("Class Info", "Class Info")
    )
    dialog = class_info.oi_create_dialog(title)

    predefined_psets = predefined_property_set.get_property_sets()
    class_info.oi_connect_dialog(dialog, predefined_psets)
    class_info.oi_fill_properties(mode=mode)
    class_info.oi_update_dialog(dialog)
    if mode == 0:
        names = [p.name for p in predefined_psets]
        util.create_completer(names, dialog.widget.combo_box_pset)
    if dialog.exec():
        if mode == 0:
            class_info.trigger_class_creation()
        elif mode == 1:
            class_info.trigger_class_modification()
        elif mode == 2:
            class_info.trigger_class_copy()


def class_info_refresh(class_info: Type[tool.ClassInfo]):
    data_dict = class_info.oi_get_values()
    class_info.oi_set_values(data_dict)
    ident_value = data_dict["ident_value"]
    group = data_dict["is_group"]
    ident_filter = (
        class_info.get_active_class().ident_value
        if class_info.oi_get_mode() == 1
        else None
    )
    if not class_info.is_identifier_allowed(ident_value, [ident_filter]):
        class_info.oi_set_ident_value_color("red")
    else:
        class_info.oi_set_ident_value_color(QPalette().color(QPalette.Text).name())
    class_info.oi_change_visibility_identifiers(group)


def class_info_add_ifc(class_info: Type[tool.ClassInfo]):
    class_info.add_ifc_mapping("")
