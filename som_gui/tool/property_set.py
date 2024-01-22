from __future__ import annotations
import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui.tool import Object, Project
from PySide6.QtWidgets import QTableWidgetItem, QCompleter, QTableWidget, QWidget, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QValidator, QIntValidator, QDoubleValidator, QRegularExpressionValidator
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.attribute import trigger as attribute_trigger
from som_gui.module.property_set import trigger as property_set_trigger
from SOMcreator.constants.json_constants import INHERITED_TEXT
from SOMcreator.constants.value_constants import VALUE_TYPE_LOOKUP, DATA_TYPES
from SOMcreator.constants import value_constants
from som_gui.icons import get_link_icon
from typing import TYPE_CHECKING
from som_gui.module.property_set import ui as ui_property_set

if TYPE_CHECKING:
    from som_gui.module.property_set.prop import PropertySetProperties
    from som_gui.module.property_set.ui import PropertySetWindow
from som_gui.module.property_set import ui


class PropertySet(som_gui.core.tool.PropertySet):
    @classmethod
    def get_property_set_from_window(cls, window: QWidget) -> SOMcreator.PropertySet:
        prop = cls.get_pset_properties()
        return prop.property_set_windows.get(window)

    @classmethod
    def get_selected_property_set(cls):
        active_window = som_gui.MainUi.window.app.activeWindow()
        return cls.get_property_set_from_window(active_window)

    @classmethod
    def get_pset_from_item(cls, item: QTableWidgetItem):
        return item.data(CLASS_REFERENCE)

    @classmethod
    def get_existing_psets_in_table(cls, table: QTableWidget):
        psets = set()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            psets.add(cls.get_pset_from_item(item))
        return psets

    @classmethod
    def clear_table(cls):
        table = cls.get_table()
        for row in reversed(range(table.rowCount())):
            table.removeRow(row)

    @classmethod
    def get_property_sets(cls) -> set[SOMcreator.PropertySet]:
        active_object = Object.get_active_object()
        if active_object is None:
            return set()
        return set(active_object.property_sets)

    @classmethod
    def get_table(cls):
        return som_gui.MainUi.ui.table_pset

    @classmethod
    def get_row_from_pset(cls, property_set: SOMcreator.PropertySet):
        table = cls.get_table()
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if cls.get_pset_from_item(item) == property_set:
                return row

    @classmethod
    def remove_property_sets_from_table(cls, property_sets: set[SOMcreator.PropertySet], table: QTableWidget):
        rows = sorted(cls.get_row_from_pset(p) for p in property_sets)
        for row in reversed(rows):
            table.removeRow(row)

    @classmethod
    def add_property_sets_to_table(cls, property_sets: set[SOMcreator.PropertySet], table: QTableWidget):
        for property_set in property_sets:
            items = [QTableWidgetItem() for _ in range(3)]
            row = table.rowCount()
            table.setRowCount(row + 1)
            [item.setData(CLASS_REFERENCE, property_set) for item in items]
            [table.setItem(row, col, item) for col, item in enumerate(items)]
            check_state = Qt.CheckState.Checked if property_set.optional else Qt.CheckState.Unchecked
            items[0].setText(f"{property_set.name}")
            if property_set.is_child:
                text = property_set.parent.name if property_set.parent.object is not None else INHERITED_TEXT
                items[1].setText(text)
                items[0].setIcon(get_link_icon())
            items[2].setCheckState(check_state)

    @classmethod
    def get_predefined_psets(cls) -> set[SOMcreator.PropertySet]:
        proj = Project.get()
        return proj.get_predefined_psets()

    @classmethod
    def get_selecte_property_set(cls) -> SOMcreator.PropertySet | None:
        table = cls.get_table()
        items = table.selectedItems()
        if not items:
            return
        item = items[0]
        return cls.get_pset_from_item(item)

    @classmethod
    def update_completer(cls):
        psets = [pset.name for pset in cls.get_predefined_psets()]
        completer = QCompleter(psets)
        som_gui.MainUi.ui.lineEdit_ident_pSet.setCompleter(completer)
        som_gui.MainUi.ui.lineEdit_pSet_name.setCompleter(completer)

    @classmethod
    def set_enabled(cls, enabled: bool):
        layout = som_gui.MainUi.ui.box_layout_pset
        layout.setEnabled(enabled)

    @classmethod
    def get_pset_properties(cls) -> PropertySetProperties:
        return som_gui.PropertySetProperties

    @classmethod
    def set_active_property_set(cls, property_set: SOMcreator.PropertySet):
        prop = cls.get_pset_properties()
        prop.active_pset = property_set
        obj = Object.get_active_object()

    @classmethod
    def get_active_property_set(cls) -> SOMcreator.PropertySet:
        prop = cls.get_pset_properties()
        return prop.active_pset

    @classmethod
    def open_pset_window(cls, property_set: SOMcreator.PropertySet):
        prop = cls.get_pset_properties()
        window = ui.PropertySetWindow()
        prop.property_set_windows[window] = property_set
        window.show()
        window.widget.combo_type.clear()
        window.widget.combo_type.addItems(cls.get_allowed_value_types())

        window.widget.combo_data_type.clear()
        window.widget.combo_data_type.addItems(cls.get_allowed_data_types())
        attribute_trigger.connect_attribute_table(window.widget.table_widget)
        property_set_trigger.connect_property_set_window(window)

        title = f"{property_set.object.name}:{property_set.name}" if property_set.object else f"{property_set.name}"
        window.setWindowTitle(title)
        return window

    @classmethod
    def pw_toggle_comboboxes(cls, attribute: SOMcreator.Attribute, window: PropertySetWindow):
        is_child = attribute.is_child
        window.widget.combo_type.setEnabled(not is_child)
        window.widget.combo_data_type.setEnabled(not is_child)
        t1 = "Attribut wurde geerbt -> Keine Änderung des Types möglich" if is_child else ""
        t2 = "Attribut wurde geerbt -> Keine Änderung des Datentyps möglich" if is_child else ""
        window.widget.combo_type.setToolTip(t1)
        window.widget.combo_data_type.setToolTip(t2)

    @classmethod
    def pw_set_attribute_name(cls, name: str, window: PropertySetWindow):
        window.widget.lineEdit_name.setText(name)

    @classmethod
    def pw_set_data_type(cls, data_type: str, window: PropertySetWindow):
        window.widget.combo_data_type.setCurrentText(data_type)

    @classmethod
    def pw_set_value_type(cls, value_type: str, window: PropertySetWindow):
        window.widget.combo_type.setCurrentText(value_type)

    @classmethod
    def pw_add_value_line(cls, column_count: int, window: PropertySetWindow) -> QHBoxLayout:
        new_layout = QHBoxLayout()
        for _ in range(column_count):
            new_layout.addWidget(ui_property_set.LineInput())
        window.widget.verticalLayout_2.addLayout(new_layout)
        return new_layout

    @classmethod
    def get_input_value_lines(cls, window: PropertySetWindow) -> list[list[QLineEdit]]:
        lines = list()
        base_layout = window.widget.verticalLayout_2
        for row in range(base_layout.count()):
            hor_layout: QHBoxLayout = base_layout.itemAt(row)
            lines.append([hor_layout.itemAt(col).widget() for col in range(hor_layout.count())])
        return lines

    @classmethod
    def pw_clear_values(cls, window: PropertySetWindow):
        layout = window.widget.verticalLayout_2
        for row in reversed(range(layout.count())):
            item: QHBoxLayout = layout.itemAt(row)
            for col in reversed(range(item.count())):
                item.itemAt(col).widget().deleteLater()
            item.layout().deleteLater()
            layout.removeItem(item)

    @classmethod
    def pw_set_values(cls, values: list[str | list[str]], window: PropertySetWindow):
        for value in values:
            value = "" if value is None else value
            if isinstance(value, (list, set)):
                line_layout = cls.pw_add_value_line(len(value), window)
                for col, v in enumerate(value):
                    v = "" if value is None else v
                    line_edit: ui_property_set.LineInput = line_layout.itemAt(col).widget()
                    line_edit.setText(cls.value_to_string(v))
            else:
                line_layout = cls.pw_add_value_line(1, window)
                line_edit: ui_property_set.LineInput = line_layout.itemAt(0).widget()
                line_edit.setText(cls.value_to_string(value))

    @classmethod
    def pw_set_description(cls, description: str, window: PropertySetWindow):
        window.widget.description.setText(description)

    @classmethod
    def pw_set_add_button_text(cls, text: str, window: PropertySetWindow):
        button = window.widget.button_add
        button.setText(text)

    @classmethod
    def pw_get_attribute_name(cls, window: PropertySetWindow):
        return window.widget.lineEdit_name.text()

    @classmethod
    def get_allowed_value_types(cls):
        return VALUE_TYPE_LOOKUP.keys()

    @classmethod
    def get_allowed_data_types(cls):
        return DATA_TYPES

    @classmethod
    def pw_get_data_type(cls, window: PropertySetWindow):
        return window.widget.combo_data_type.currentText()

    @classmethod
    def pw_get_value_type(cls, window: PropertySetWindow):
        return window.widget.combo_type.currentText()

    @classmethod
    def format_values(cls, value_list: list[str], window: PropertySetWindow):
        data_type = cls.pw_get_data_type(window)
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
    def value_to_string(cls, value):
        if isinstance(value, str):
            return value
        if isinstance(value, int):
            return str(value)
        if isinstance(value, float):
            return str(value).replace(".", ",")

    @classmethod
    def pw_get_values(cls, window: PropertySetWindow):
        lines = cls.get_input_value_lines(window)
        value_list = list()
        for row in lines:
            values = cls.format_values([line.text() for line in row], window)
            if len(values) > 1:
                value_list.append(values)
            else:
                value_list.append(values[0])
        return value_list

    @classmethod
    def pw_get_attribute_data(cls, window: PropertySetWindow):
        d = dict()
        d["name"] = cls.pw_get_attribute_name(window)
        d["data_type"] = window.widget.combo_data_type.currentText()
        d["value_type"] = window.widget.combo_type.currentText()
        d["values"] = cls.pw_get_values(window)
        d["description"] = window.widget.description.toPlainText()
        return d

    @classmethod
    def update_line_validators(cls, window: PropertySetWindow):
        data_type = cls.pw_get_data_type(window)
        value_type = cls.pw_get_value_type(window)
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
    def set_value_columns(cls, column_count: int, window: PropertySetWindow):
        main_layout = window.widget.verticalLayout_2
        for row_index in range(main_layout.count()):
            hor_layout: QHBoxLayout = main_layout.itemAt(row_index)
            existing_columns = hor_layout.count()
            dif = column_count - existing_columns
            if dif > 0:
                for _ in range(dif):
                    hor_layout.addWidget(ui_property_set.LineInput())
            elif dif < 0:
                for _ in range(abs(dif)):
                    item = hor_layout.itemAt(hor_layout.count() - 1)
                    item.widget().deleteLater()
                    hor_layout.removeItem(item)

    @classmethod
    def restrict_data_type_to_numbers(cls, window: PropertySetWindow):
        active_type = window.widget.combo_data_type.currentText()
        data_types = [value_constants.REAL, value_constants.INTEGER]
        window.widget.combo_data_type.clear()
        window.widget.combo_data_type.addItems(data_types)
        if active_type in data_types:
            window.widget.combo_data_type.setCurrentText(active_type)

    @classmethod
    def remove_data_type_restriction(cls, window: PropertySetWindow):
        active_type = window.widget.combo_data_type.currentText()
        data_type = cls.get_allowed_data_types()
        window.widget.combo_data_type.clear()
        window.widget.combo_data_type.addItems(data_type)
        window.widget.combo_data_type.setCurrentText(active_type)
