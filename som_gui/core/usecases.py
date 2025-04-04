from __future__ import annotations
from PySide6.QtCore import QCoreApplication, QModelIndex
from typing import TYPE_CHECKING, Type
import logging

if TYPE_CHECKING:
    from som_gui import tool


def create_main_menu_actions(
    usecases: Type[tool.Usecases], main_window: Type[tool.MainWindow]
):
    action = main_window.add_action(
        "menuEdit", "UsecaseWindow", usecases.signaller.open_window.emit
    )
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
    usecases.connect_models()
    usecases.connect_views()
    # ToDo: Add Shortcut FUnction
    # util.add_shortcut(
    #     "Ctrl+F", widget, lambda: search_class(filter_window, search, project)
    # )
    # filter_window.connect_project_table(project.get())
    # filter_window.connect_class_tree(project.get())
    usecases.signaller.retranslate_ui.emit()
    window.show()


def update_project_table_size(usecases: Type[tool.Usecases]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = usecases.get_project_model()
    logging.debug(
        f"Filter Changed Externally. rowCount: {model.old_row_count} -> {model.rowCount()} columnCount:{model.old_column_count} -> {model.columnCount()}"
    )

    # Remove Rows (Phases)
    if model.old_row_count > model.rowCount():
        model.beginRemoveRows(QModelIndex(), model.rowCount(), model.old_row_count - 1)
        model.endRemoveRows()

    # Insert Rows (Phases)
    if model.old_row_count < model.rowCount():
        model.beginInsertRows(QModelIndex(), model.old_row_count + 1, model.rowCount())
        model.endInsertRows()

    # Remove Colums (UseCases)
    if model.old_column_count > model.columnCount():
        model.beginRemoveColumns(
            QModelIndex(), model.columnCount(), model.old_column_count - 1
        )
        model.endRemoveColumns()

    # Insert Colums (UseCases)
    if model.old_column_count < model.columnCount():
        model.beginInsertColumns(
            QModelIndex(), model.old_column_count + 1, model.columnCount()
        )
        model.endInsertColumns()


def update_class_tree_size(index: QModelIndex, usecases: Type[tool.Usecases]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = usecases.get_class_model()
    model.update_data()
    old_row_count = model.row_count_dict.get(index) or 0
    old_column_count = model.old_column_count
    new_row_count = model.get_row_count(index)
    new_column_count = model.columnCount()

    if new_row_count==old_row_count and new_column_count == old_column_count:
        logging.info(f"No Change Required")
        return
    logging.info(
        f"ClassModel Update Size rowCount: {old_row_count} -> {new_row_count} columnCount:{old_column_count} -> {new_column_count} {index}"
    )

    # Remove Rows (Phases)
    if old_row_count > new_row_count:
        model.beginRemoveRows(
            index, new_row_count, old_row_count - 1
        )
        print("Remove Rows")
        model.endRemoveRows()

    # Insert Rows (Phases)
    if old_row_count < new_row_count:
        model.beginInsertRows(
            index, old_row_count, new_row_count +1
        )
        print("Insert Rows")

        model.endInsertRows()

    # Remove Colums (UseCases)
    if old_column_count > new_column_count:
        model.beginRemoveColumns(
            index, new_column_count, old_column_count - 1
        )
        print("Remove Columns")

        model.endRemoveColumns()

    # Insert Colums (UseCases)
    if old_column_count < new_column_count:
        model.beginInsertColumns(
            index, old_column_count + 1, new_column_count 
        )
        print("Insert Columns")

        model.endInsertColumns()

    model.row_count_dict[index] = new_row_count
    model.old_column_count = new_column_count

    logging.info("Update Done")
    model.dataChanged.emit(
            model.createIndex(0, 0),
            model.createIndex(model.rowCount(), model.columnCount()),
        )