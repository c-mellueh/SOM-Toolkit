from __future__ import annotations
from PySide6.QtCore import QCoreApplication,QModelIndex
from typing import TYPE_CHECKING, Type
import logging
if TYPE_CHECKING:
    from som_gui import tool

def create_main_menu_actions(
    usecases: Type[tool.Usecases], main_window: Type[tool.MainWindow]
):
    action = main_window.add_action("menuEdit", "UsecaseWindow", usecases.signaller.open_window.emit)
    usecases.set_action("open_window", action)
    usecases.connect_signals()

def retranslate_ui(usecases: Type[tool.Usecases], util: Type[tool.Util]):
    action = usecases.get_action("open_window")
    action.setText(QCoreApplication.translate("UsecaseWindow", "Usecases"))

    window = usecases.get_window()
    if window:
        title = QCoreApplication.translate("UsecaseWindow", "Project Filter")
        window.ui.retranslateUi(window)
        window.setWindowTitle(util.get_window_title(title))

def open_window(
    usecases: Type[tool.Usecases],
    project: Type[tool.Project],
    util: Type[tool.Util],
    search: Type[tool.Search],
):

    window = usecases.get_window()
    if window:
        window.show()
        window.activateWindow()
        return

    window = usecases.create_window()
    usecases.add_models_to_window(project.get())
    #ToDo: Add Shortcut FUnction
    # util.add_shortcut(
    #     "Ctrl+F", widget, lambda: search_class(filter_window, search, project)
    # )
    # filter_window.connect_project_table(project.get())
    # filter_window.connect_class_tree(project.get())
    usecases.signaller.retranslate_ui.emit()
    window.show()

def filter_changed_externally(usecases: Type[tool.Usecases]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = usecases.get_project_model()
    logging.debug(
        f"Filter Changed Externally. rowCount: {model.last_row_count} -> {model.rowCount()} columnCount:{model.last_col_count} -> {model.columnCount()}"
    )

    # Remove Rows (Phases)
    if model.last_row_count > model.rowCount():
        model.beginRemoveRows(QModelIndex(), model.rowCount(), model.last_row_count - 1)
        model.endRemoveRows()

    # Insert Rows (Phases)
    if model.last_row_count < model.rowCount():
        model.beginInsertRows(QModelIndex(), model.last_row_count + 1, model.rowCount())
        model.endInsertRows()

    # Remove Colums (UseCases)
    if model.last_col_count > model.columnCount():
        model.beginRemoveColumns(
            QModelIndex(), model.columnCount(), model.last_col_count - 1
        )
        model.endRemoveColumns()

    # Insert Colums (UseCases)
    if model.last_col_count < model.columnCount():
        model.beginInsertColumns(
            QModelIndex(), model.last_col_count + 1, model.columnCount()
        )
        model.endInsertColumns()