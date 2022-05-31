from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit,QDialog,QDialogButtonBox,QGridLayout

def default_message(icon,text):
    msgBox = QMessageBox()
    msgBox.setText(text)
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)

    msgBox.setWindowIcon(icon)
    msgBox.exec()


def msg_already_exists(icon):
    text = "Object exists already!"
    default_message(icon,text)

def msg_identical_identifier(icon):
    text = "You cant create Objects with identical identifiers!"
    default_message(icon, text)


def msg_missing_input(icon):
    text = "Object informations are missing!"
    default_message(icon,text)


def msg_unsaved(icon):
    msgBox = QMessageBox()
    msgBox.setText("Warning, unsaved changes will be lost!")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Ok)
    msgBox.setWindowIcon(icon)
    if msgBox.exec() == msgBox.Ok:
        return True
    else:
        return False


def msg_delete_or_merge(icon):
    msgBox = QMessageBox()
    msgBox.setText("Warning, there is allready exisiting data!\n do you want to delete or merge?")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)

    msgBox.setStandardButtons(QMessageBox.Cancel)
    merge_button = msgBox.addButton("Merge", QMessageBox.NoRole)
    delete_button = msgBox.addButton("Delete", QMessageBox.YesRole)
    msgBox.setWindowIcon(icon)
    msgBox.exec()
    if msgBox.clickedButton() == merge_button:
        return False
    elif msgBox.clickedButton() == delete_button:
        return True
    else:
        return None


def msg_close(icon):
    text = "Do you want to save before exit?"

    msgBox = QMessageBox(QMessageBox.Icon.Warning,
                         "Message",
                         text,
                         QMessageBox.Cancel | QMessageBox.Save | QMessageBox.No)

    msgBox.setWindowIcon(icon)
    reply = msgBox.exec()
    return reply


def msg_del_ident_pset(icon):
    text = "can't delete Pset of Identifier!"
    default_message(icon, text)

def msg_mod_ident(icon):
    text = "Identifier can't be modified!"
    default_message(icon,text)

class GroupRequest(QDialog):
    def __init__(self,icon,parent = None,):
        super(GroupRequest, self).__init__(parent)
        self.group_name = QLineEdit(self)
        self.pset_name = QLineEdit(self)
        self.attribute_name = QLineEdit(self)
        self.attribute_value = QLineEdit(self)
        self.setWindowIcon(icon)

        self.group_name.setPlaceholderText("Name")
        self.pset_name.setPlaceholderText("PropertySet")
        self.attribute_value.setPlaceholderText("Value")
        self.attribute_name.setPlaceholderText("Attribute")

        self.input_fields = [self.group_name,self.pset_name,self.attribute_name,self.attribute_value]
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel,self)

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
            msg_missing_input(self.windowIcon())
        else:
            super(GroupRequest, self).accept()

    def get_text(self):
        return [text.text() for text in self.input_fields]

def req_group_name(mainWindow):
    dialog = GroupRequest(mainWindow.icon,mainWindow)

    if dialog.exec():
        return dialog.get_text()

    else:
        return [False,False,False,False]

def req_attribute_name(propertyWindow):
    text = QInputDialog.getText(propertyWindow,"New Attribute Name","New Attribute Name")
    return text