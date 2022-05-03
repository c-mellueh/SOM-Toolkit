from PySide6.QtWidgets import QMessageBox, QInputDialog, QLineEdit


def msg_already_exists(icon):
    msgBox = QMessageBox()
    msgBox.setText("Object exists already!")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)

    msgBox.setWindowIcon(icon)
    msgBox.exec()


def msg_missing_input(icon):
    msgBox = QMessageBox()
    msgBox.setText("Object informations are missing!")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)

    msgBox.setWindowIcon(icon)
    msgBox.exec()


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
    msgBox = QMessageBox()
    msgBox.setText("can't delete Pset of Identifier!")
    msgBox.setWindowTitle(" ")
    msgBox.setIcon(QMessageBox.Icon.Warning)
    msgBox.setWindowIcon(icon)
    msgBox.exec()


def req_group_name(mainWindow):
    title = "Group Name"
    text = "Input Name of new Group"
    return QInputDialog.getText(mainWindow, title, text, echo=QLineEdit.EchoMode.Normal, text="")[0]
