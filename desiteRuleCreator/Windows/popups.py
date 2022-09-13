import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QDialog, QDialogButtonBox, QGridLayout,QListWidgetItem,QCompleter
import desiteRuleCreator.icons as icons
from desiteRuleCreator.QtDesigns import ui_delete_request,ui_groupReq

def default_message(text):
    icon = icons.get_icon()
    msg_box = QMessageBox()
    msg_box.setText(text)
    msg_box.setWindowTitle("Warning")
    msg_box.setIcon(QMessageBox.Icon.Warning)

    msg_box.setWindowIcon(icon)
    msg_box.exec()

def msg_select_only_one():
    text = "Select only one item!"
    default_message(text)

def msg_recursion():
    text = "Object can't be added because of Recursion!"
    default_message(text)

def msg_already_exists():
    text = "Object exists already!"
    default_message(text)

def msg_attribute_already_exists():
    text = "Object exists already!"
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


def req_group_name(main_window,prefil:list[str]= None):
    def change_visibility(checked):
        enable = not checked
        widget.pset_name.setEnabled(enable)
        widget.attribute_name.setEnabled(enable)
        widget.attribute_value.setEnabled(enable)


    dialog = QDialog(main_window)
    widget = ui_groupReq.Ui_Dialog()
    widget.setupUi(dialog)
    widget.radioButton.toggled.connect(change_visibility)
    input_fields = [widget.group_name, widget.pset_name, widget.attribute_name, widget.attribute_value]
    if prefil is not None:
        for i,field in enumerate(input_fields[:-1]):
            pl_text = prefil[i]
            field.setText(pl_text)

    if dialog.exec():
        return [input_field.text() for input_field in input_fields],widget.radioButton.isChecked()
    else:
        return [False, False, False, False], widget.radioButton.isChecked()


def req_new_name(property_window,base_text = ""):
    text = QInputDialog.getText(property_window, "New Name", "New Name",text = base_text)
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

def req_boq_pset(main_window,words):
    input_dialog = QInputDialog(main_window)
    input_dialog.setWindowTitle("Bill of Quantities")
    input_dialog.setLabelText("BoQ PropertySet Name")
    input_dialog.setTextValue("BoQ")
    line_edit:QLineEdit = input_dialog.findChild(QLineEdit)

    completer = QCompleter(words)
    line_edit.setCompleter(completer)
    ok = input_dialog.exec()
    if ok ==1:
        return True,input_dialog.textValue()
    else:
        return False,None