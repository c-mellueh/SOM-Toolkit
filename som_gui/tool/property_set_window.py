from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import (
    QDoubleValidator,
    QGuiApplication,
    QIntValidator,
    QRegularExpressionValidator,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QCompleter,
    QComboBox,
    QListWidget,
    QListWidgetItem,
)
from ifcopenshell.util.unit import unit_names, prefixes
import SOMcreator
import som_gui
import som_gui.core.tool
from SOMcreator.constants import value_constants
from SOMcreator.constants.value_constants import DATA_TYPES, VALUE_TYPES
from som_gui import tool
from som_gui.module.property_set_window import ui
from som_gui.module.property_set_window.constants import (
    SEPERATOR,
    SEPERATOR_SECTION,
    SEPERATOR_STATUS,
)

from som_gui.module.property_set_window import trigger


if TYPE_CHECKING:
    from som_gui.module.property_set_window.prop import PropertySetWindowProperties
    from som_gui.module.attribute.ui import UnitComboBox


class PropertySetWindow(som_gui.core.tool.PropertySetWindow):
    @classmethod
    def get_properties(cls) -> PropertySetWindowProperties:
        return som_gui.PropertySetWindowProperties

    @classmethod
    def get_open_windows(cls) -> list[ui.PropertySetWindow]:
        return list(cls.get_properties().property_set_windows.keys())

    @classmethod
    def get_active_attribute(
        cls, window: ui.PropertySetWindow
    ) -> None | SOMcreator.SOMProperty:
        attribute_name = cls.get_attribute_name_input(window)
        pset = cls.get_property_set_by_window(window)
        return tool.PropertySet.get_attribute_by_name(pset, attribute_name)

    @classmethod
    def get_inherit_checkbox_state(cls, window: ui.PropertySetWindow) -> bool:
        return window.ui.check_box_inherit.checkState() == Qt.CheckState.Checked

    @classmethod
    def set_inherit_checkbox_state(cls, state: bool, window: ui.PropertySetWindow):
        cs = Qt.CheckState.Checked if state else Qt.CheckState.Unchecked
        window.ui.check_box_inherit.setCheckState(cs)

    @classmethod
    def get_table(cls, window: ui.PropertySetWindow):
        return window.ui.table_widget

    @classmethod
    def get_window_by_property_set(cls, property_set: SOMcreator.SOMPropertySet):
        prop = cls.get_properties()
        return {pset: window for window, pset in prop.property_set_windows.items()}.get(
            property_set
        )

    @classmethod
    def get_property_set_by_window(
        cls, window: ui.PropertySetWindow
    ) -> SOMcreator.SOMPropertySet:
        prop = cls.get_properties()
        return prop.property_set_windows.get(window)

    @classmethod
    def get_attribute_name_input(cls, window: ui.PropertySetWindow):
        return window.ui.lineEdit_name.text()

    @classmethod
    def get_attribute_data(cls, window: ui.PropertySetWindow):
        d = dict()
        d["name"] = cls.get_attribute_name_input(window)
        d["data_type"] = window.ui.combo_data_type.currentText()
        d["value_type"] = window.ui.combo_value_type.currentText()
        d["values"] = cls.get_values(window)
        d["description"] = window.ui.description.toPlainText()
        d["inherit_value"] = cls.get_inherit_checkbox_state(window)
        d["unit"] = window.ui.combo_unit.currentText()
        return d

    @classmethod
    def get_input_value_lines(
        cls, window: ui.PropertySetWindow
    ) -> list[list[QLineEdit]]:
        lines = list()
        base_layout = window.ui.verticalLayout_2
        for row in range(base_layout.count()):
            hor_layout: QHBoxLayout = base_layout.itemAt(row)
            lines.append(
                [hor_layout.itemAt(col).widget() for col in range(hor_layout.count())]
            )
        return lines

    @classmethod
    def get_values(cls, window: ui.PropertySetWindow):
        lines = cls.get_input_value_lines(window)
        value_list = list()
        for row in lines:
            values = cls.format_values(
                [line.text() for line in row if line.text()], window
            )
            if not values:
                continue
            if len(values) > 1:
                value_list.append(values)
            else:
                value_list.append(values[0])
        return value_list

    @classmethod
    def format_values(cls, value_list: list[str], window: ui.PropertySetWindow):
        data_type = cls.get_data_type(window)
        if data_type not in (value_constants.REAL, value_constants.INTEGER):
            return [str(val) for val in value_list]
        values = [val.replace(".", "") for val in value_list]  # remove thousend Point
        values = [float(val.replace(",", ".")) for val in values if val]
        if data_type == value_constants.INTEGER:
            values = [int(val) for val in value_list]
        if len(values) < len(value_list):
            values += [None for _ in range(len(value_list) - len(values))]
        return values

    @classmethod
    def get_data_type(cls, window: ui.PropertySetWindow):
        return window.ui.combo_data_type.currentText()

    @classmethod
    def get_value_type(cls, window: ui.PropertySetWindow):
        return window.ui.combo_value_type.currentText()

    @classmethod
    def add_value_line(
        cls, column_count: int, window: ui.PropertySetWindow
    ) -> QHBoxLayout:
        new_layout = QHBoxLayout()
        for _ in range(column_count):
            new_layout.addWidget(ui.LineInput())
        window.ui.verticalLayout_2.addLayout(new_layout)
        return new_layout

    @classmethod
    def close_property_set_window(cls, window: ui.PropertySetWindow):
        logging.debug(f"Remove {window}")
        prop = cls.get_properties()
        if window in prop.property_set_windows:
            prop.property_set_windows.pop(window)
        else:
            logging.warning(
                f"PropertySetWindow can't be removed because it's not registred"
            )

    @classmethod
    def get_paste_text_list(cls):
        seperator = tool.Appdata.get_string_setting(SEPERATOR_SECTION, SEPERATOR, ",")
        seperator_status = tool.Appdata.get_bool_setting(
            SEPERATOR_SECTION, SEPERATOR_STATUS
        )
        text = QGuiApplication.clipboard().text()

        if not seperator_status:
            return [text]

        text_list = text.split(seperator)
        return text_list

    @classmethod
    def get_required_column_count(cls, window: ui.PropertySetWindow):
        value_type = cls.get_value_type(window)
        if value_type == value_constants.RANGE:
            return 2
        else:
            return 1

    @classmethod
    def bring_window_to_front(cls, window: ui.PropertySetWindow):
        window.raise_()

    @classmethod
    def create_window(cls, property_set: SOMcreator.SOMPropertySet):
        prop = cls.get_properties()
        window = ui.PropertySetWindow()
        prop.property_set_windows[window] = property_set
        return window

    @classmethod
    def get_allowed_value_types(cls):
        return VALUE_TYPES

    @classmethod
    def get_allowed_data_types(cls):
        return DATA_TYPES

    @classmethod
    def fill_window_ui(cls, window: ui.PropertySetWindow):
        window.ui.combo_value_type.clear()
        window.ui.combo_value_type.addItems(cls.get_allowed_value_types())
        window.ui.combo_data_type.clear()
        window.ui.combo_data_type.addItems(cls.get_allowed_data_types())
        window.ui.combo_value_type.setCurrentText(value_constants.LIST)
        window.ui.combo_data_type.setCurrentText(value_constants.LABEL)
        cls.add_value_line(1, window)

    @classmethod
    def update_datatype_completer(cls, window: ui.PropertySetWindow):
        cb = window.ui.combo_data_type
        cb.setCompleter(QCompleter([cb.itemText(i) for i in range(cb.count())]))

    @classmethod
    def update_valuetype_completer(cls, window: ui.PropertySetWindow):
        cb = window.ui.combo_value_type
        cb.setCompleter(QCompleter([cb.itemText(i) for i in range(cb.count())]))

    @classmethod
    def update_unit_completer(cls, window: ui.PropertySetWindow):
        cb = window.ui.combo_unit
        cb.setCompleter(QCompleter([cb.itemText(i) for i in range(cb.count())]))

    @classmethod
    def connect_window_triggers(cls, window):
        som_gui.module.property_set_window.trigger.connect_window(window)

    @classmethod
    def fill_window_title(
        cls, window: ui.PropertySetWindow, property_set: SOMcreator.SOMPropertySet
    ):
        title = (
            f"{property_set.som_class.name}:{property_set.name}"
            if property_set.som_class
            else f"{property_set.name}"
        )
        window.setWindowTitle(title)

    @classmethod
    def update_add_button(cls, window: ui.PropertySetWindow):
        attribute_name = cls.get_attribute_name_input(window)
        pset = cls.get_property_set_by_window(window)
        if attribute_name in [a.name for a in pset.get_properties(filter=False)]:
            text = QCoreApplication.translate("PropertySetWindow", "Update")
            cls.set_add_button_text(text, window)
        else:
            text = QCoreApplication.translate("PropertySetWindow", "Add")
            cls.set_add_button_text(text, window)

        cls.set_add_button_enabled(bool(attribute_name), window)

    @classmethod
    def toggle_comboboxes(
        cls, attribute: SOMcreator.SOMProperty, window: ui.PropertySetWindow
    ):
        is_child = attribute.is_child
        window.ui.combo_value_type.setEnabled(not is_child)
        window.ui.combo_data_type.setEnabled(not is_child)
        window.ui.combo_unit.setEnabled(not is_child)
        if is_child:
            t1 = QCoreApplication.translate(
                "PropertySetWindow",
                "Attribute was inherited -> Type change not possible",
            )
            t2 = QCoreApplication.translate(
                "PropertySetWindow",
                "Attribute was inherited -> DataType change not possible",
            )
            t3 = QCoreApplication.translate(
                "PropertySetWindow",
                "Attribute was inherited -> Unit change not possible",
            )
        else:
            t1 = t2 = t3 = ""
        window.ui.combo_value_type.setToolTip(t1)
        window.ui.combo_data_type.setToolTip(t2)
        window.ui.combo_unit.setToolTip(t3)

    @classmethod
    def set_attribute_name(cls, name: str, window: ui.PropertySetWindow):
        window.ui.lineEdit_name.setText(name)

    @classmethod
    def set_data_type(cls, data_type: str, window: ui.PropertySetWindow):
        window.ui.combo_data_type.setCurrentText(data_type)

    @classmethod
    def set_value_type(cls, value_type: str, window: ui.PropertySetWindow):
        window.ui.combo_value_type.setCurrentText(value_type)

    @classmethod
    def set_unit(cls, unit: str, window: ui.PropertySetWindow):
        window.ui.combo_unit.setCurrentText(unit or "")

    @classmethod
    def clear_values(cls, window: ui.PropertySetWindow):
        layout = window.ui.verticalLayout_2
        for row in reversed(range(layout.count())):
            item: QHBoxLayout = layout.itemAt(row)
            for col in reversed(range(item.count())):
                item.itemAt(col).widget().deleteLater()
            item.layout().deleteLater()
            layout.removeItem(item)

    @classmethod
    def set_values(
        cls, attribute: SOMcreator.SOMProperty, window: ui.PropertySetWindow
    ):
        inherits = attribute.is_inheriting_values
        parent_values = attribute.parent.value if attribute.parent else []
        for value in attribute.value:

            value = "" if value is None else value
            if isinstance(value, (list, set)):
                line_layout = cls.add_value_line(len(value), window)
                for col, v in enumerate(value):
                    v = "" if value is None else v
                    line_edit: ui.LineInput = line_layout.itemAt(col).widget()
                    line_edit.setText(cls.value_to_string(v))
            else:
                line_layout = cls.add_value_line(1, window)
                line_edit: ui.LineInput = line_layout.itemAt(0).widget()
                line_edit.setText(cls.value_to_string(value))

            # If Value is Inherited by Parent set layout disabled
            enabled = False if inherits and value in parent_values else True
            line_edit.setEnabled(enabled)

    @classmethod
    def set_description(cls, description: str, window: ui.PropertySetWindow):
        window.ui.description.setText(description)

    @classmethod
    def set_add_button_text(cls, text: str, window: ui.PropertySetWindow):
        button = window.ui.button_add
        button.setText(text)

    @classmethod
    def set_add_button_enabled(cls, enabled: bool, window: ui.PropertySetWindow):
        button = window.ui.button_add
        button.setEnabled(enabled)

    @classmethod
    def update_line_validators(cls, window: ui.PropertySetWindow):
        data_type = cls.get_data_type(window)
        value_type = cls.get_value_type(window)
        if data_type == value_constants.INTEGER:
            validator = QIntValidator()
        elif data_type == value_constants.REAL:
            validator = QDoubleValidator()
        elif value_type == value_constants.FORMAT:
            validator = QRegularExpressionValidator()
        else:
            validator = QRegularExpressionValidator()
        for row in cls.get_input_value_lines(window):
            for line in row:
                line.setValidator(validator)

    @classmethod
    def value_to_string(cls, value):
        if isinstance(value, str):
            return value
        if isinstance(value, int):
            return str(value)
        if isinstance(value, float):
            return str(value).replace(".", ",")

    @classmethod
    def set_value_columns(cls, column_count: int, window: ui.PropertySetWindow):
        main_layout = window.ui.verticalLayout_2
        for row_index in range(main_layout.count()):
            hor_layout: QHBoxLayout = main_layout.itemAt(row_index)
            existing_columns = hor_layout.count()
            dif = column_count - existing_columns
            if dif > 0:
                for _ in range(dif):
                    hor_layout.addWidget(ui.LineInput())
            elif dif < 0:
                for _ in range(abs(dif)):
                    item = hor_layout.itemAt(hor_layout.count() - 1)
                    item.widget().deleteLater()
                    hor_layout.removeItem(item)

    @classmethod
    def restrict_data_type_to_numbers(cls, window: ui.PropertySetWindow):
        active_type = window.ui.combo_data_type.currentText()
        data_types = [value_constants.REAL, value_constants.INTEGER]
        window.ui.combo_data_type.clear()
        window.ui.combo_data_type.addItems(data_types)
        if active_type in data_types:
            window.ui.combo_data_type.setCurrentText(active_type)

    @classmethod
    def remove_data_type_restriction(cls, window: ui.PropertySetWindow):
        active_type = window.ui.combo_data_type.currentText()
        data_type = cls.get_allowed_data_types()
        window.ui.combo_data_type.clear()
        window.ui.combo_data_type.addItems(data_type)
        window.ui.combo_data_type.setCurrentText(active_type)

    @classmethod
    def get_unit_combobox(cls, window: ui.PropertySetWindow) -> UnitComboBox:
        return window.ui.combo_unit

    ### Settings Window
    @classmethod
    def set_splitter_settings_widget(cls, widget: ui.SplitterSettings):
        cls.get_properties().splitter_settings = widget

    @classmethod
    def get_splitter_settings_widget(cls) -> ui.SplitterSettings:
        return cls.get_properties().splitter_settings

    @classmethod
    def connect_splitter_widget(cls, widget: ui.SplitterSettings):
        widget.ui.check_box_seperator.checkStateChanged.connect(
            lambda: trigger.splitter_checkstate_changed(widget)
        )

    @classmethod
    def get_splitter_settings_checkstate(cls, widget: ui.SplitterSettings) -> bool:
        return widget.ui.check_box_seperator.isChecked()

    @classmethod
    def get_splitter_settings_text(cls, widget: ui.SplitterSettings) -> str:
        return widget.ui.line_edit_seperator.text()
