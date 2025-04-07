from __future__ import annotations
from PySide6.QtCore import QCoreApplication, QModelIndex
from typing import TYPE_CHECKING, Type
import logging
import SOMcreator

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
    window = usecases.create_window()
    usecases.add_models_to_window(project.get())
    usecases.connect_models()
    usecases.connect_class_views()
    usecases.connect_property_views()
    usecases.add_header_view(project.get())
    util.add_shortcut("Ctrl+F", window, usecases.signaller.search_class.emit)
    usecases.signaller.retranslate_ui.emit()
    window.show()


def search_class(
    usecases: Type[tool.Usecases],
    search: Type[tool.Search],
    project: Type[tool.Project],
):
    som_class = search.search_class(list(project.get().get_classes(filter=True)))
    if som_class is None:
        return
    class_view = usecases.get_class_views()[1]
    class_model = usecases.get_class_model()
    parent_list = [som_class]
    parent = som_class.parent
    while parent is not None:
        parent_list.append(parent)
        parent = parent.parent
    # needs to happen top down. DataModel creates children only if parent is already created
    # You can't combine the parent search with expanding the Tree it needs to happen in two steps
    for item in reversed(parent_list):
        index: QModelIndex = class_model.class_index_dict.get(item)
        class_view.expand(index)
    flags = (
        class_view.selectionModel().SelectionFlag.ClearAndSelect
        | class_view.selectionModel().SelectionFlag.Rows
    )
    class_view.selectionModel().select(index, flags)
    class_view.scrollTo(
        index.sibling(index.row(), 0), class_view.ScrollHint.EnsureVisible
    )


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
        print("Insert Project Rows")
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
    model.row_count_dict[index] = new_row_count
    model.old_column_count = new_column_count
    header_model = usecases.get_class_header_model()
    logging.info(
        f"ClassModel Update Size rowCount: {old_row_count} -> {new_row_count} columnCount:{old_column_count} -> {new_column_count} {index}"
    )
    if old_row_count == new_row_count and old_column_count == new_column_count:
        return

    # Remove Rows (Phases)
    if old_row_count > new_row_count:
        model.beginRemoveRows(index, new_row_count, old_row_count - 1)
        model.endRemoveRows()

    # Insert Rows (Phases)
    if old_row_count < new_row_count:
        model.beginInsertRows(index, old_row_count, new_row_count - 1)
        model.endInsertRows()

    # Remove Colums (UseCases)
    if old_column_count > new_column_count:
        model.beginRemoveColumns(index, new_column_count, old_column_count - 1)
        model.endRemoveColumns()
        header_model.beginRemoveColumns(
            QModelIndex(), new_column_count, old_column_count - 1
        )
        header_model.endRemoveColumns()

    # Insert Colums (UseCases)
    if old_column_count < new_column_count:
        model.beginInsertColumns(index, old_column_count, new_column_count - 1)
        model.endInsertColumns()
        header_model.beginInsertColumns(
            QModelIndex(), old_column_count, new_column_count - 1
        )
        header_model.endInsertColumns()
    usecases.get_class_views()[1].update_requested.emit()


def update_property_table_size(usecases: Type[tool.Usecases]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = usecases.get_property_model()
    logging.debug(
        f"Filter Changed Externally. rowCount: {model.old_row_count} -> {model.rowCount()} columnCount:{model.old_column_count} -> {model.columnCount()}"
    )
    model.update_data()
    usecases.get_class_views()[0].selectedIndexes()
    old_row_count = model.old_row_count
    old_column_count = model.old_column_count
    new_row_count = model.rowCount()
    new_col_count = model.columnCount()
    header_model = usecases.get_property_header_model()
    model.old_row_count = new_row_count
    model.old_column_count = new_col_count
    if old_row_count == 0:
        model.beginResetModel()
        model.endResetModel()
        header_model.beginResetModel()
        header_model.endResetModel()

    else:
        index = QModelIndex()
        # Remove Rows (Phases)
        if old_row_count > new_row_count:
            model.beginRemoveRows(index, new_row_count, old_row_count - 1)
            model.endRemoveRows()

        # Insert Rows (Phases)
        if old_row_count < new_row_count:
            model.beginInsertRows(index, old_row_count, new_row_count - 1)
            model.endInsertRows()

        # Remove Colums (UseCases)
        if old_column_count > new_col_count:
            model.beginRemoveColumns(index, new_col_count, old_column_count - 1)
            model.endRemoveColumns()
            header_model.beginRemoveColumns(index, new_col_count, old_column_count - 1)
            header_model.endRemoveColumns()
        # Insert Colums (UseCases)
        if old_column_count < new_col_count:
            model.beginInsertColumns(index, old_column_count, new_col_count - 1)
            model.endInsertColumns()
            header_model.beginInsertColumns(index, old_column_count, new_col_count - 1)
            header_model.endInsertColumns()
    usecases.get_property_views()[1].update_requested.emit()


def update_class_selection(usecases: Type[tool.Usecases]):
    som_class = usecases.get_active_class()
    usecases.get_property_label().setText(som_class.name if som_class else "")
    property_model = usecases.get_property_model()
    property_model.som_class = som_class
    property_model.update_data()
    property_model.resize_required.emit()
