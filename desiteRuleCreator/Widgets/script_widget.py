from PySide6.QtCore import Slot, Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QTextFormat
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit

from desiteRuleCreator.QtDesigns import ui_mainwindow
from SOMcreator import classes
from desiteRuleCreator.Windows import popups
from desiteRuleCreator.data import custom_qt

def init(main_window):
    def connect():
        ui.pushButton_add_script.clicked.connect(main_window.add_script)
        ui.pushButton_delete_script.clicked.connect(main_window.delete_selected_scripts)
        ui.listWidget_scripts.itemClicked.connect(main_window.script_list_clicked)
        ui.pushButton_burger.clicked.connect(main_window.change_script_list_visibility)
        ui.listWidget_scripts.itemChanged.connect(main_window.code_item_changed)

    ui: ui_mainwindow.Ui_MainWindow = main_window.ui

    ui.verticalLayout_2.removeWidget(ui.code_edit)
    ui.code_edit.deleteLater()
    ui.code_edit = CodeEditor()
    ui.verticalLayout_2.addWidget(ui.code_edit)
    ui.code_edit.show()
    connect()
    set_enable(main_window, False)


def item_changed(main_window, item: classes.Script):
    item.name = item.text()
    main_window.ui.label_script_name.setText(item.name)


def selection_changed(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    sel_items = ui.listWidget_scripts.selectedItems()

    if len(sel_items) != 1:
        value = False
    else:
        value = True

    for button in code_buttons(main_window):
        button.setEnabled(value)

    ui.code_edit.setEnabled(value)
    pass


def clicked(main_window, item: classes.Script):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    ui.code_edit.setEnabled(True)
    edit: QPlainTextEdit = ui.code_edit
    edit.setPlainText(item.code)
    # ui.code_edit.setText(item.code)

    for button in code_buttons(main_window):
        button.setEnabled(True)


def change_script_list_visibility(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui

    if ui.widget_vertical_stack.isHidden():
        ui.widget_vertical_stack.show()
    else:
        ui.widget_vertical_stack.hide()

    for script in main_window.active_object.scripts:
        print(script.name)


def script_buttons(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    buttons = [
        ui.pushButton_add_script,
        ui.pushButton_delete_script,
        ui.pushButton_import_script
    ]
    return buttons


def code_buttons(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    buttons = [
        ui.pushButton_burger,
        ui.pushButton_left,
        ui.pushButton_right
    ]
    return buttons


def show(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    tree_item: custom_qt.CustomObjectTreeItem = main_window.selected_object()
    if tree_item is not None:
        obj = tree_item.object
        for script in obj.scripts:
            ui.listWidget_scripts.addItem(script)


def delete_objects(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui

    string_list = [x.text() for x in ui.listWidget_scripts.selectedItems()]

    delete_request = popups.msg_del_items(string_list)
    if delete_request:

        for script in ui.listWidget_scripts.selectedItems():
            item: classes.Script = ui.listWidget_scripts.takeItem(ui.listWidget_scripts.indexFromItem(script).row())
            item.object.delete_script(item)
        ui.code_edit.clear()
        selection_changed(main_window)


def set_enable(main_window, value: bool):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    ui.tab_code.setEnabled(value)
    if not value:
        ui.tabWidget.setTabText(ui.tabWidget.indexOf(ui.tab_code), "Code")
        for i in reversed(range(ui.listWidget_scripts.count())):
            ui.listWidget_scripts.takeItem(i)
        ui.code_edit.clear()

    if ui.listWidget_scripts.count() < 1:
        code_value = False
    else:
        code_value = True

    for el in code_buttons(main_window):
        el.setEnabled(code_value)
    ui.code_edit.setEnabled(code_value)
    ui.label_script_name.setEnabled(code_value)
    ui.label_script_name.setText(" ")


def add_script(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    script = classes.Script("NewScript", main_window.active_object)
    ui.listWidget_scripts.addItem(script)
    ui.listWidget_scripts.setCurrentItem(script)
    selection_changed(main_window)
    item_changed(main_window, script)


def update_script(main_window):
    ui: ui_mainwindow.Ui_MainWindow = main_window.ui
    script_list = main_window.ui.listWidget_scripts
    selected_items = script_list.selectedItems()

    if len(selected_items) == 1:
        item: classes.Script = selected_items[0]
        item.code = ui.code_edit.toPlainText()
        ui.label_script_name.setText(item.name)
        ui.label_script_name.setEnabled(True)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self._code_editor = editor

    def sizeHint(self):
        return QSize(self._code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._code_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def lineNumberAreaPaintEvent(self, event):
        with QPainter(self.line_number_area) as painter:
            painter.fillRect(event.rect(), Qt.lightGray)
            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            offset = self.contentOffset()
            top = self.blockBoundingGeometry(block).translated(offset).top()
            bottom = top + self.blockBoundingRect(block).height()

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = str(block_number + 1)
                    painter.setPen(Qt.black)
                    width = self.line_number_area.width()
                    height = self.fontMetrics().height()
                    painter.drawText(0, top, width, height, Qt.AlignRight, number)

                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                block_number += 1

    @Slot()
    def update_line_number_area_width(self, newBlockCount):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @Slot()
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    @Slot()
    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)

            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)
