from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QDialog, QListWidgetItem, QCompleter, \
    QTableWidgetItem
from SOMcreator import classes
from thefuzz import fuzz

from .. import icons
from ..icons import get_icon
from ..qt_designs import ui_delete_request, ui_group_name_request, ui_search, ui_attribute_mapping

if TYPE_CHECKING:
    from ..main_window import MainWindow

UMLAUT_DICT = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss'}
CLASS_REFERENCE = Qt.ItemDataRole.UserRole + 1


def default_message(text):
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.setWindowTitle("Warning")
    msg_box.setIcon(QMessageBox.Icon.Warning)

    msg_box.setWindowIcon(icon)
    msg_box.exec()


def msg_already_exists():
    text = "Objekt existiert bereits!"
    default_message(text)


def msg_ident_already_exists():
    text = "Identifier existiert bereits!"
    default_message(text)


def msg_abbrev_already_exists():
    text = "Kürzel existiert bereits!"
    default_message(text)


def msg_attribute_already_exists():
    text = "Attribut existiert bereits!"
    default_message(text)


def msg_identical_identifier():
    text = "You cant create Objects with identical identifiers!"
    default_message(text)


def msg_missing_input():
    text = "Missing Input(s)!"
    default_message(text)


def msg_unsaved():
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText("Warning, unsaved changes will be lost!")
    msg_box.setWindowTitle(" ")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
    msg_box.setWindowIcon(icon)
    if msg_box.exec() == msg_box.StandardButton.Ok:
        return True
    else:
        return False


def msg_delete_or_merge():
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText("Warning, there is allready exisiting data!\n do you want to delete or merge?")
    msg_box.setWindowTitle(" ")
    msg_box.setIcon(QMessageBox.Icon.Warning)

    msg_box.setStandardButtons(QMessageBox.StandardButton.Cancel)
    merge_button = msg_box.addButton("Merge", QMessageBox.ButtonRole.NoRole)
    delete_button = msg_box.addButton("Delete", QMessageBox.ButtonRole.YesRole)
    msg_box.setWindowIcon(icon)
    msg_box.exec()
    if msg_box.clickedButton() == merge_button:
        return False
    elif msg_box.clickedButton() == delete_button:
        return True
    else:
        return None


def msg_close():
    icon = icons.get_icon()
    text = "Do you want to save before exit?"

    msg_box = QMessageBox(QMessageBox.Icon.Warning,
                          "Message",
                          text,
                          QMessageBox.StandardButton.Cancel |
                          QMessageBox.StandardButton.Save |
                          QMessageBox.StandardButton.No)

    msg_box.setWindowIcon(icon)
    reply = msg_box.exec()
    return reply


def msg_del_ident_pset():
    text = "can't delete Pset of Identifier!"
    default_message(text)


def msg_mod_ident():
    text = "Identifier can't be modified!"
    default_message(text)


def req_group_name(main_window, prefil: list[str] = None):
    def change_visibility(checked):
        enable = not checked
        widget.pset_name.setEnabled(enable)
        widget.attribute_name.setEnabled(enable)
        widget.attribute_value.setEnabled(enable)

    dialog = QDialog(main_window)
    widget = ui_group_name_request.Ui_Dialog()
    widget.setupUi(dialog)
    widget.checkBox.toggled.connect(change_visibility)
    input_fields = [widget.group_name, widget.pset_name, widget.attribute_name, widget.attribute_value,
                    widget.abbreviation]
    if prefil is not None:
        for i, field in enumerate(input_fields[:-1]):
            pl_text = prefil[i]
            field.setText(pl_text)

    if dialog.exec():
        return [input_field.text() for input_field in input_fields], widget.checkBox.isChecked()
    else:
        return [False, False, False, False, False], widget.checkBox.isChecked()


def req_pset_name(main_window: MainWindow, old):
    text = QInputDialog.getText(main_window, "New PropertySet Name ", "New PropertySet Name", text=old)
    return text


def req_attribute_name(main_window: MainWindow, old):
    text = QInputDialog.getText(main_window, "New Attribute Name ", "New Attribute Name", text=old)
    return text


def req_merge_pset():
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText("Pset exists in Predefined Psets, do you want to merge?")
    msg_box.setWindowTitle(" ")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
    msg_box.setWindowIcon(icon)

    statement = msg_box.exec()
    if statement == msg_box.StandardButton.Yes:
        return True
    elif statement == msg_box.StandardButton.No:
        return False
    else:
        return None


def msg_del_items(string_list, item_type=1) -> (bool, bool):
    """
    item_type 1= Object,2= Node, 3 = PropertySet, 4 = Attribute
    """
    parent = QDialog()
    widget = ui_delete_request.Ui_Dialog()
    widget.setupUi(parent)
    parent.setWindowIcon(get_icon())
    if len(string_list) <= 1:
        if item_type == 1:
            widget.label.setText("Dieses Objekt löschen?")
        if item_type == 2:
            widget.label.setText("Diese Node löschen?")
        if item_type == 3:
            widget.label.setText("Dieses PropertySet löschen?")
        if item_type == 4:
            widget.label.setText("Dieses Attribut löschen?")
    else:
        if item_type == 1:
            widget.label.setText("Diese Objekte löschen?")
        if item_type == 2:
            widget.label.setText("Diese Nodes öschen?")
        if item_type == 3:
            widget.label.setText("Diese PropertySets löschen?")
        if item_type == 4:
            widget.label.setText("Diese Attribute löschen?")

    for text in string_list:
        widget.listWidget.addItem(QListWidgetItem(text))
    result = parent.exec()
    check_box_state = True if widget.check_box_recursion.checkState() == Qt.CheckState.Checked else False
    return bool(result), check_box_state


def req_boq_pset(main_window, words):
    input_dialog = QInputDialog(main_window)
    input_dialog.setWindowTitle("Bill of Quantities")
    input_dialog.setLabelText("BoQ PropertySet Name")
    input_dialog.setTextValue("BoQ")
    line_edit: QLineEdit = input_dialog.findChild(QLineEdit)

    completer = QCompleter(words)
    line_edit.setCompleter(completer)
    ok = input_dialog.exec()
    if ok == 1:
        return True, input_dialog.textValue()
    else:
        return False, None


def attribute_mapping(attribute: classes.Attribute):
    parent = QDialog()
    widget = ui_attribute_mapping.Ui_Dialog()
    widget.setupUi(parent)
    widget.label_name.setText(f"RevitMapping {attribute.name}")
    widget.line_edit_revit_mapping.setText(attribute.revit_name)

    if parent.exec():
        attribute.revit_name = widget.line_edit_revit_mapping.text()


def req_export_pset_name(main_window):
    return QInputDialog.getText(main_window, "PropertySet name", "What's the name of the Export PropertySet?")


def req_worksheet_name(main_window, worksheet_names: list[str]):
    index = 0
    test = "SOM-MaKa"
    if test in worksheet_names:
        index = worksheet_names.index(test)
    text, ok = QInputDialog.getItem(main_window, "Worksheet Name", "Name of Mapping Worksheet", worksheet_names, index)
    return text, ok


class SearchWindow(QDialog):

    def __init__(self, main_window: MainWindow, text_matrix: list[list[str]], connection_list: list,
                 header_list: list[str], threshold: int = 65):
        super(SearchWindow, self).__init__()

        def connect_items():
            self.widget.lineEdit.textChanged.connect(self.search)
            self.widget.tableWidget.itemDoubleClicked.connect(self.item_clicked)

        self.widget = ui_search.Ui_Dialog()
        self.widget.setupUi(self)
        main_window.search_ui = self
        self.table = self.widget.tableWidget

        self.item_cols = len(text_matrix[0])
        self.threshold = threshold
        self.project: classes.Project = main_window.project
        self.data = None

        self.style_window(header_list)
        self.fill_table(text_matrix, connection_list)
        connect_items()

    def style_window(self, header_list: list[str]) -> None:
        self.widget.tableWidget.verticalHeader().setVisible(False)
        self.table.setColumnCount(self.item_cols + 1)
        self.table.sortByColumn(self.item_cols, Qt.SortOrder.DescendingOrder)
        self.table.hideColumn(self.item_cols)
        table_header = self.widget.tableWidget.horizontalHeader()
        table_header.setStretchLastSection(True)
        table_header.setSectionResizeMode(0, table_header.ResizeMode.ResizeToContents)
        self.table.setHorizontalHeaderLabels(header_list)
        self.setWindowTitle("Search")
        self.setWindowIcon(get_icon())

    def fill_table(self, text_matrix: list[list[str]], connection_list: list) -> None:
        for row, (text_list, connection_item) in enumerate(zip(text_matrix, connection_list)):
            item_list = [QTableWidgetItem(text) for text in text_list]
            [item.setData(CLASS_REFERENCE, connection_item) for item in item_list]
            self.table.insertRow(self.table.rowCount())
            for col, value in enumerate(item_list):
                self.table.setItem(self.table.rowCount() - 1, col, value)

    def item_clicked(self, table_item: QTableWidgetItem) -> None:
        self.data = table_item.data(CLASS_REFERENCE)
        self.accept()

    def check_row(self, search_text: str, row: int) -> float:
        model = self.widget.tableWidget.model()
        texts = [model.data(model.index(row, col)).lower() for col in range(self.item_cols)]
        ratio = max(fuzz.ratio(search_text, text) for text in texts)
        model.setData(model.index(row, self.item_cols), ratio, Qt.ItemDataRole.DisplayRole)
        return ratio

    def search(self) -> None:
        self.table.setSortingEnabled(False)
        search_text = self.widget.lineEdit.text().lower()
        search_text = search_text.translate(UMLAUT_DICT)
        for row in range(self.table.model().rowCount()):
            ratio = self.check_row(search_text, row)
            if ratio > self.threshold:
                self.table.showRow(row)
            else:
                self.table.hideRow(row)
        self.table.setSortingEnabled(True)


def new_file_clicked(main_window: MainWindow):
    new_file = msg_unsaved()
    if new_file:
        project_name = QInputDialog.getText(main_window, "New Project", "new Project Name:", QLineEdit.EchoMode.Normal,
                                            "")
        if project_name[1]:
            main_window.clear_all()
            main_window.setWindowTitle(main_window.project.name)
            main_window.project.name = project_name[0]
