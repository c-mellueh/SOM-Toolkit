from __future__ import annotations
from PySide6.QtCore import QCoreApplication, QModelIndex, Qt, QPoint
from PySide6.QtGui import QMouseEvent
from typing import TYPE_CHECKING, Type
import logging
import SOMcreator

if TYPE_CHECKING:
    from som_gui import tool
from som_gui.module.use_case import ui


def create_main_menu_actions(
    use_case: Type[tool.UseCase], main_window: Type[tool.MainWindow]
):
    action = main_window.add_action(
        "menuEdit", "UsecaseWindow", use_case.signaller.open_window.emit
    )
    use_case.set_action("open_window", action)
    use_case.connect_signals()


def retranslate_ui(use_case: Type[tool.UseCase], util: Type[tool.Util]):
    action = use_case.get_action("open_window")
    text = QCoreApplication.translate("UsecaseWindow", "Usecases")
    action.setText(text)

    window = use_case.get_window()
    if not window:
        return
    title = QCoreApplication.translate("UsecaseWindow", "Usecases")
    window.ui.retranslateUi(window)
    window.setWindowTitle(util.get_window_title(title))

    t1 = QCoreApplication.translate("UsecaseWindow", "Class")
    t2 = QCoreApplication.translate("UsecaseWindow", "Identifier")
    use_case.get_class_header_model().first_columns = [t1, t2]

    t1 = QCoreApplication.translate("UsecaseWindow", "PropertySet")
    t2 = QCoreApplication.translate("UsecaseWindow", "Property")
    use_case.get_property_header_model().first_columns = [t1, t2]


def open_window(
    use_case: Type[tool.UseCase],
    project: Type[tool.Project],
    util: Type[tool.Util],
):
    window = use_case.create_window()
    use_case.add_models_to_window(project.get())
    use_case.connect_models()
    use_case.connect_project_view()
    use_case.connect_class_views()
    use_case.connect_property_views()
    use_case.add_header_view(project.get())
    util.add_shortcut("Ctrl+F", window, use_case.signaller.search_class.emit)
    util.add_shortcut("Ctrl+U", window, use_case.signaller.add_use_case.emit)
    util.add_shortcut("Ctrl+P", window, use_case.signaller.add_phase.emit)

    use_case.signaller.retranslate_ui.emit()
    window.show()


def search_class(
    use_case: Type[tool.UseCase],
    search: Type[tool.Search],
    project: Type[tool.Project],
):
    som_class = search.search_class(list(project.get().get_classes(filter=True)))
    if som_class is None:
        return
    class_view = use_case.get_class_views()[1]
    class_model = use_case.get_class_model()
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


def update_project_table_size(use_case: Type[tool.UseCase]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = use_case.get_project_model()
    old_row_count = model.old_row_count
    old_column_count = model.old_column_count
    new_row_count = model.rowCount()
    new_col_count = model.columnCount()
    model.old_row_count = new_row_count
    model.old_column_count = new_col_count
    logging.debug(
        f"Filter Changed Externally. rowCount: {model.old_row_count} -> {model.rowCount()} columnCount:{model.old_column_count} -> {model.columnCount()}"
    )

    if old_row_count == 0:
        model.beginResetModel()
        model.endResetModel()
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
        # Insert Colums (UseCases)
        if old_column_count < new_col_count:
            model.beginInsertColumns(index, old_column_count, new_col_count - 1)
            model.endInsertColumns()
    use_case.get_project_view().update_requested.emit()


def update_class_tree_size(index: QModelIndex, use_case: Type[tool.UseCase]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = use_case.get_class_model()
    model.update_data()
    old_row_count = model.row_count_dict.get(index) or 0
    old_column_count = model.old_column_count
    new_row_count = model.get_row_count(index)
    new_column_count = model.columnCount()
    model.row_count_dict[index] = new_row_count
    model.old_column_count = new_column_count
    header_model = use_case.get_class_header_model()
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
    use_case.get_class_views()[1].update_requested.emit()


def update_property_table_size(use_case: Type[tool.UseCase]):
    """
    gets Called if Filters get Added or Removed externally. For example by Console Script.
    :param filter_window:
    :return:
    """
    model = use_case.get_property_model()
    logging.debug(
        f"Filter Changed Externally. rowCount: {model.old_row_count} -> {model.rowCount()} columnCount:{model.old_column_count} -> {model.columnCount()}"
    )
    model.update_data()
    use_case.get_class_views()[0].selectedIndexes()
    old_row_count = model.old_row_count
    old_column_count = model.old_column_count
    new_row_count = model.rowCount()
    new_col_count = model.columnCount()
    header_model = use_case.get_property_header_model()
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
    use_case.get_property_views()[1].update_requested.emit()


def update_class_selection(use_case: Type[tool.UseCase]):
    som_class = use_case.get_active_class()
    use_case.get_property_label().setText(som_class.name if som_class else "")
    property_model = use_case.get_property_model()
    property_model.som_class = som_class
    property_model.update_data()
    property_model.resize_required.emit()


def add_use_case(
    use_case: Type[tool.UseCase],
    util: Type[tool.Util],
):

    model = use_case.get_project_model()
    project = model.project
    text = QCoreApplication.translate("UsecaseWindow", "New UseCase")
    new_name = util.get_new_name(text, [uc.name for uc in project.get_usecases()])
    logging.debug(f"Add UseCase '{new_name}'")
    new_use_case = SOMcreator.UseCase(new_name, new_name, new_name)
    model.beginInsertColumns(QModelIndex(), model.columnCount(), model.columnCount())
    use_case_index = project.add_usecase(new_use_case)
    model.endInsertColumns()
    use_case.signaller.rename_filter.emit(Qt.Orientation.Horizontal, use_case_index)


def remove_use_case(
    use_case_index: int,
    use_case: Type[tool.UseCase],
):
    model = use_case.get_project_model()
    project = model.project
    selected_use_case = project.get_usecase_by_index(use_case_index)
    logging.debug(f"remove UseCase '{selected_use_case.name}'")
    model.beginRemoveColumns(QModelIndex(), use_case_index, use_case_index)
    project.remove_usecase(selected_use_case)
    model.endRemoveColumns()


def add_phase(
    use_case: Type[tool.UseCase],
    util: Type[tool.Util],
):

    text = QCoreApplication.translate("FilterWindow", "New Phase")
    model = use_case.get_project_model()
    project = model.project
    new_name = util.get_new_name(text, [ph.name for ph in project.get_phases()])
    logging.debug(f"Add Phase '{new_name}'")
    phase = SOMcreator.Phase(new_name, new_name, new_name)
    model.beginInsertRows(QModelIndex(), model.rowCount(), model.rowCount())
    phase_index = project.add_phase(phase)
    model.endInsertRows()
    use_case.signaller.rename_filter.emit(Qt.Orientation.Vertical, phase_index)


def remove_phase(
    phase_index: int,
    use_case: Type[tool.UseCase],
):
    model = use_case.get_project_model()
    project = model.project
    phase = model.project.get_phase_by_index(phase_index)
    logging.debug(f"remove Phase '{phase.name}'")
    phase_index = project.get_phase_index(phase)
    model.beginRemoveRows(QModelIndex(), phase_index, phase_index)
    model.project.remove_phase(phase)
    model.endRemoveRows()


def create_context_menu(
    local_pos: QPoint,
    orientation: Qt.Orientation,
    use_case: Type[tool.UseCase],
    project: Type[tool.Project],
):
    proj = project.get()

    menu_list = list()
    project_view = use_case.get_project_view()
    header = (
        project_view.horizontalHeader()
        if orientation == Qt.Orientation.Horizontal
        else project_view.verticalHeader()
    )
    if orientation == Qt.Orientation.Horizontal:  # use_case
        index = header.logicalIndexAt(local_pos)

        del_uc = QCoreApplication.translate("FilterWindow", "Delete UseCase")
        rename_uc = QCoreApplication.translate("FilterWindow", "Rename UseCase")
        add_uc = QCoreApplication.translate("FilterWindow", "Add UseCase")

        if len(proj.get_usecases()) > 1:
            menu_list.append(
                (del_uc, lambda: use_case.signaller.remove_use_case.emit(index))
            )
        menu_list.append(
            (
                rename_uc,
                lambda: use_case.signaller.rename_filter.emit(
                    Qt.Orientation.Horizontal, index
                ),
            )
        )
        menu_list.append((add_uc, lambda: use_case.signaller.add_use_case.emit()))
        pos = header.viewport().mapToGlobal(local_pos)

    elif orientation == Qt.Orientation.Vertical:
        index = header.logicalIndexAt(local_pos)
        del_ph = QCoreApplication.translate("FilterWindow", "Delete Phase")
        rename_ph = QCoreApplication.translate("FilterWindow", "Rename Phase")
        add_ph = QCoreApplication.translate("FilterWindow", "Add Phase")

        if len(proj.get_phases()) > 1:
            menu_list.append(
                (del_ph, lambda: use_case.signaller.remove_phase.emit(index))
            )
        menu_list.append(
            (
                rename_ph,
                lambda: use_case.signaller.rename_filter.emit(
                    Qt.Orientation.Vertical, index
                ),
            )
        )
        menu_list.append((add_ph, lambda: use_case.signaller.add_phase.emit()))
        pos = header.viewport().mapToGlobal(local_pos)
    use_case.create_context_menu(menu_list, pos)


def rename_filter(
    orientation: Qt.Orientation, logical_index: int, use_case: Type[tool.UseCase]
):
    project_view = use_case.get_project_view()
    header: ui.EditableHeader = (
        project_view.horizontalHeader()
        if orientation == Qt.Orientation.Horizontal
        else project_view.verticalHeader()
    )
    header.edit_header_text(logical_index)


def mouse_move_event(
    event: QMouseEvent, source, use_case: Type[tool.UseCase], util: Type[tool.Util]
):
    view = source
    index: QModelIndex = view.indexAt(event.pos())
    if not use_case.is_mouse_pressed():
        use_case.set_mouse_pressed(True)
        checkstate = not util.checkstate_to_bool(
            index.data(Qt.ItemDataRole.CheckStateRole)
        )
        use_case.set_mouse_press_checkstate(checkstate)
    use_case.tree_move_click_drag(index)


def mouse_release_event(
    view: ui.ClassView | ui.PropertyView | ui.ProjectView,
    use_case: Type[tool.UseCase],
):
    use_case.set_mouse_pressed(False)
    use_case.set_mouse_press_checkstate(None)
    if isinstance(view, ui.ClassView):
        view.update_requested.emit()
    elif isinstance(view, ui.PropertyView):
        view.update_requested.emit()
    else:
        view.update_requested.emit()
