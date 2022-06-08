import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QDialog, QDialogButtonBox, QGridLayout,QListWidgetItem

import desiteRuleCreator.icons as icons
from desiteRuleCreator.QtDesigns import ui_delete_request


def default_message(text):
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.setWindowTitle(" ")
    msg_box.setIcon(QMessageBox.Icon.Warning)

    msg_box.setWindowIcon(icon)
    msg_box.exec()



def msg_already_exists():
    text = "Object exists already!"
    default_message(text)


def msg_identical_identifier():
    text = "You cant create Objects with identical identifiers!"
    default_message(text)


def msg_missing_input():
    text = "Object informations are missing!"
    default_message(text)


def msg_unsaved():
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText("Warning, unsaved changes will be lost!")
    msg_box.setWindowTitle(" ")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg_box.setDefaultButton(QMessageBox.Ok)
    msg_box.setWindowIcon(icon)
    if msg_box.exec() == msg_box.Ok:
        return True
    else:
        return False


def msg_delete_or_merge():
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText("Warning, there is allready exisiting data!\n do you want to delete or merge?")
    msg_box.setWindowTitle(" ")
    msg_box.setIcon(QMessageBox.Icon.Warning)

    msg_box.setStandardButtons(QMessageBox.Cancel)
    merge_button = msg_box.addButton("Merge", QMessageBox.NoRole)
    delete_button = msg_box.addButton("Delete", QMessageBox.YesRole)
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
                         QMessageBox.Cancel | QMessageBox.Save | QMessageBox.No)

    msg_box.setWindowIcon(icon)
    reply = msg_box.exec()
    return reply


def msg_del_ident_pset():
    text = "can't delete Pset of Identifier!"
    default_message(text)


def msg_mod_ident():
    text = "Identifier can't be modified!"
    default_message(text)

class DeleteRequest(QDialog):
    def __init__(self, parent=None, ):
        super(DeleteRequest, self).__init__(parent)
        icon = icons.get_icon()

        self.group_name = QLineEdit(self)
        self.pset_name = QLineEdit(self)
        self.attribute_name = QLineEdit(self)
        self.attribute_value = QLineEdit(self)
        self.setWindowIcon(icon)

        self.group_name.setPlaceholderText("Name")
        self.pset_name.setPlaceholderText("PropertySet")
        self.attribute_value.setPlaceholderText("Value")
        self.attribute_name.setPlaceholderText("Attribute")

        self.input_fields = [self.group_name, self.pset_name, self.attribute_name, self.attribute_value]
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.pset_name, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.attribute_name, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.attribute_value, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 2)
        self.gridLayout.addWidget(self.group_name, 0, 0, 1, 3)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("New Group")

class GroupRequest(QDialog):
    def __init__(self, parent=None, ):
        super(GroupRequest, self).__init__(parent)
        icon = icons.get_icon()
        self.group_name = QLineEdit(self)
        self.pset_name = QLineEdit(self)
        self.attribute_name = QLineEdit(self)
        self.attribute_value = QLineEdit(self)
        self.setWindowIcon(icon)

        self.group_name.setPlaceholderText("Name")
        self.pset_name.setPlaceholderText("PropertySet")
        self.attribute_value.setPlaceholderText("Value")
        self.attribute_name.setPlaceholderText("Attribute")

        self.input_fields = [self.group_name, self.pset_name, self.attribute_name, self.attribute_value]
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.pset_name, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.attribute_name, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.attribute_value, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 2)
        self.gridLayout.addWidget(self.group_name, 0, 0, 1, 3)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("New Group")

    def accept(self) -> None:
        is_empty = [True for text in self.input_fields if not bool(text.text())]
        if is_empty:
            msg_missing_input()
        else:
            super(GroupRequest, self).accept()

    def get_text(self):
        return [text.text() for text in self.input_fields]


def req_group_name(main_window):
    dialog = GroupRequest(main_window)

    if dialog.exec():
        return dialog.get_text()

    else:
        return [False, False, False, False]


def req_attribute_name(property_window):
    text = QInputDialog.getText(property_window, "New Attribute Name", "New Attribute Name")
    return text

def req_pset_name(main_window):
    text = QInputDialog.getText(main_window, "New PropertySet Name ", "New PropertySet Name")
    return text

def req_merge_pset():
    icon = icons.get_icon()
    msg_box= QMessageBox()
    msg_box.setText("Pset exists in Predefined Psets, do you want to merge?")
    msg_box.setWindowTitle(" ")
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    msg_box.setDefaultButton(QMessageBox.Yes)
    msg_box.setWindowIcon(icon)

    statement = msg_box.exec()
    if statement == msg_box.Yes:
        return True
    elif statement == msg_box.No:
        return False
    else:
        return None

def msg_del_items(string_list):
    parent = QDialog()
    widget = ui_delete_request.Ui_Dialog()
    widget.setupUi(parent)
    if len(string_list) <=1:
        widget.label.setText("Delete this item?")
    else:
        widget.label.setText("Delete these items?")

    for text in string_list:
        widget.listWidget.addItem(QListWidgetItem(text))

    if parent.exec():
        return True
    else:
        return False