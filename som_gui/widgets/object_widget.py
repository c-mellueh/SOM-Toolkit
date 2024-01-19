from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QTreeWidgetItem,

)
from SOMcreator import classes


CHECK_POS = 3


class CustomObjectTreeItem(QTreeWidgetItem):
    def __init__(self, obj: classes.Object) -> None:
        super(CustomObjectTreeItem, self).__init__()
        self._object = obj
        self.refresh()

    def addChild(self, child: CustomObjectTreeItem) -> None:
        super(CustomObjectTreeItem, self).addChild(child)
        if child.object not in self.object.children:
            self.object.add_child(child.object)

    @property
    def object(self) -> classes.Object:
        return self._object

    def refresh(self) -> None:
        """
        set Values
        index 0: name
        index 1: ident_value
        index 2: abbreviation
        index 3: optional
        """

        values = [self.object.name, self.object.ident_value, self.object.abbreviation]

        for index, value in enumerate(values):
            self.setText(index, value)

        if self.object.optional:
            self.setCheckState(CHECK_POS, Qt.CheckState.Checked)
        else:
            self.setCheckState(CHECK_POS, Qt.CheckState.Unchecked)

    def update(self) -> None:
        check_state = self.checkState(CHECK_POS)

        if check_state == Qt.CheckState.Checked:
            check_bool = True
        elif check_state == Qt.CheckState.Unchecked:
            check_bool = False
        elif check_state == Qt.CheckState.PartiallyChecked:
            logging.error("Partially Checking not Allowed")
            check_bool = True
        else:
            check_bool = True
        self.object.optional = check_bool

    def expand_to_me(self) -> None:
        self.setExpanded(True)
        if self.parent() is not None:
            self.parent().expand_to_me()
