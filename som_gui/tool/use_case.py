from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import logging

import som_gui.core.tool
import som_gui
from PySide6.QtGui import QAction
from PySide6.QtCore import (
    Signal,
    QObject,
    QModelIndex,
    QItemSelectionModel,
    QSortFilterProxyModel,
    QSize,
    Qt,
)
from PySide6.QtWidgets import QLabel, QMenu
from som_gui.module.use_case import ui
from som_gui.module.use_case import trigger
import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.use_case.prop import UseCaseProperties


class Signaller(QObject):
    open_window = Signal()
    retranslate_ui = Signal()
    class_selection_changed = Signal()
    search_class = Signal()
    add_use_case = Signal()
    add_phase = Signal()
    remove_use_case = Signal(int)
    remove_phase = Signal(int)
    rename_filter = Signal(Qt.Orientation, int)


class UseCase(som_gui.core.tool.UseCase):
    signaller = Signaller()

    @classmethod
    def get_properties(cls) -> UseCaseProperties:
        return som_gui.UseCaseProperties

    @classmethod
    def set_action(cls, name, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name) -> QAction:
        return cls.get_properties().actions[name]

    @classmethod
    def connect_signals(cls):
        from som_gui.module.use_case import trigger

        cls.signaller.open_window.connect(trigger.open_window)
        cls.signaller.retranslate_ui.connect(trigger.retranslate_ui)
        cls.signaller.class_selection_changed.connect(trigger.class_selection_changed)
        cls.signaller.search_class.connect(trigger.search_class)
        cls.signaller.add_use_case.connect(trigger.add_use_case)
        cls.signaller.add_phase.connect(trigger.add_phase)
        cls.signaller.remove_use_case.connect(trigger.remove_use_case)
        cls.signaller.remove_phase.connect(trigger.remove_phase)
        cls.signaller.rename_filter.connect(trigger.rename_filter)

    @classmethod
    def get_window(cls) -> ui.Widget | None:
        return cls.get_properties().window

    @classmethod
    def create_window(cls):
        window = ui.Widget()
        cls.get_properties().window = window
        return window

    @classmethod
    def add_models_to_window(cls, project: SOMcreator.SOMProject):

        # Project Model
        project_model = ui.ProjectModel(project)
        project_view = cls.get_project_view()
        project_view.setModel(project_model)

        # Class Model
        class_view_1, class_view_2 = cls.get_class_views()
        class_model = ui.ClassModel(project)
        class_filter_model = ui.ClassFilterModel(class_model.fixed_column_count)
        class_filter_model.setSourceModel(class_model)
        class_view_1.setModel(class_filter_model)
        class_view_2.setModel(class_model)

        # Property MOdel
        property_view_1, property_view_2 = cls.get_property_views()
        property_model = ui.PropertyModel()
        property_filter_model = ui.ClassFilterModel(property_model.fixed_column_count)
        property_filter_model.setSourceModel(property_model)
        property_view_1.setModel(property_filter_model)
        property_view_2.setModel(property_model)

    @classmethod
    def connect_models(cls):
        project_model = cls.get_project_model()
        class_model = cls.get_class_model()
        property_model = cls.get_property_model()
        index = QModelIndex()

        # Project Model
        project_model.checkstate_changed.connect(
            lambda: class_model.resize_required.emit(index)
        )
        project_model.checkstate_changed.connect(property_model.resize_required.emit)
        project_model.data_changed_externally.connect(trigger.resize_project_model)

        # Class Model
        class_model.resize_required.connect(trigger.resize_class_model)
        class_model.resize_required.emit(QModelIndex())

        # Property Model
        property_model.resize_required.connect(trigger.resize_property_model)
        property_model.resize_required.emit()

    @classmethod
    def add_editable_header_to_view(cls, view: ui.ProjectView):
        """
        Adds header to the View that allow renaming the column/row on double click or context menu
        """
        view.setHorizontalHeader(ui.EditableHeader(Qt.Orientation.Horizontal))
        view.setVerticalHeader(ui.EditableHeader(Qt.Orientation.Vertical))

        vertical_header = view.verticalHeader()
        vertical_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        vertical_header.customContextMenuRequested.connect(
            lambda pos: trigger.header_context_requested(pos, Qt.Orientation.Vertical)
        )
        horizontal_header = view.horizontalHeader()
        horizontal_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(
            lambda pos: trigger.header_context_requested(pos, Qt.Orientation.Horizontal)
        )

    @classmethod
    def connect_project_view(cls):
        view = cls.get_project_view()
        view.mouse_moved.connect(trigger.mouse_move_event)
        view.mouse_released.connect(trigger.mouse_release_event)
        view.update_requested.connect(view.model().update_view)

    @classmethod
    def _connect_views(
        cls,
        proxy_view: ui.ClassView | ui.PropertyView,
        view: ui.ClassView | ui.PropertyView,
    ):
        """
        Connects the proxy view and the source view so that they are synchronized.
        """
        proxy_model: QSortFilterProxyModel = proxy_view.model()
        proxy_selection_model = proxy_view.selectionModel()
        selection_model = view.selectionModel()
        flags = (
            QItemSelectionModel.SelectionFlag.Rows
            | QItemSelectionModel.SelectionFlag.ClearAndSelect
        )

        def syncSelectionFromProxyToSource(selected, deselected):
            for index in selected.indexes():
                source_index = proxy_model.mapToSource(index)
                if source_index in selection_model.selectedIndexes():
                    return
                selection_model.select(source_index, flags)
                return

        def syncSelectionFromSourceToProxy(selected, deselected):
            for index in selected.indexes():
                proxy_index = proxy_model.mapFromSource(index)
                if proxy_index in proxy_selection_model.selectedIndexes():
                    return
                proxy_selection_model.select(proxy_index, flags)
                return

        proxy_selection_model.selectionChanged.connect(syncSelectionFromProxyToSource)
        selection_model.selectionChanged.connect(syncSelectionFromSourceToProxy)
        view.verticalScrollBar().valueChanged.connect(
            proxy_view.verticalScrollBar().setValue
        )
        proxy_view.verticalScrollBar().valueChanged.connect(
            view.verticalScrollBar().setValue
        )

        view.mouse_moved.connect(trigger.mouse_move_event)
        view.mouse_released.connect(trigger.mouse_release_event)
        view.update_requested.connect(view.update_view)

    @classmethod
    def connect_class_views(cls):
        """
        Connects the class ProxyView and ClassView so that they are synchronized.
        adds the signal for class selection changed
        """
        proxy_view, view = cls.get_class_views()
        proxy_model: QSortFilterProxyModel = proxy_view.model()

        cls._connect_views(proxy_view, view)
        view.selectionModel().selectionChanged.connect(
            lambda x, y: cls.signaller.class_selection_changed.emit()
        )
        # expand
        view.expanded.connect(
            lambda index: proxy_view.expand(proxy_model.mapFromSource(index))
        )
        proxy_view.expanded.connect(
            lambda index: view.expand(proxy_model.mapToSource(index))
        )
        # collapsed
        view.collapsed.connect(
            lambda index: proxy_view.collapse(proxy_model.mapFromSource(index))
        )
        proxy_view.collapsed.connect(
            lambda index: view.collapse(proxy_model.mapToSource(index))
        )

        view.clicked.connect(lambda x: view.update_requested.emit())
        view.clicked.connect(lambda x: cls.get_property_views()[1].repaint())

    @classmethod
    def connect_property_views(cls):
        """
        Connects the Property ProxyView and PropertyView so that they are synchronized.
        """
        cls._connect_views(*cls.get_property_views())

    @classmethod
    def get_project_view(cls) -> ui.ProjectView:
        window = cls.get_window()
        if window is None:
            return None
        return window.ui.project_tableView

    @classmethod
    def add_header_view(cls, project: SOMcreator.SOMProject):
        # Class Header
        cv1, cv2 = cls.get_class_views()
        hv1, hv2 = cls.create_header_views(project, ["Class", "Identifier"])
        cv1.setHeader(hv1)
        cv2.setHeader(hv2)
        cv2.hideColumn(0)
        cv2.hideColumn(1)

        # Property Header
        pv1, pv2 = cls.get_property_views()
        hv1, hv2 = cls.create_header_views(project, ["PropertySet", "Property"])
        pv1.setHorizontalHeader(hv1)
        pv2.setHorizontalHeader(hv2)
        pv2.hideColumn(0)
        pv2.hideColumn(1)

    @classmethod
    def create_header_views(
        cls, project: SOMcreator.SOMProject, first_columns: list[str]
    ):
        """
        Create CustomHeaderViews for the Class and Property View. They are multiRow First row is UseCase and second row is Phase.
        """
        header_model = ui.CustomHeaderModel(project, first_columns)
        header_view_1 = ui.CustomHeaderView(first_columns)
        header_view_2 = ui.CustomHeaderView(first_columns)
        baseSectionSize = QSize()
        baseSectionSize.setWidth(header_model.base_width)
        baseSectionSize.setHeight(header_model.base_height)
        for row in range(header_model.rowCount()):
            for col in range(header_model.columnCount()):
                index = header_model.index(row, col)
                header_model.setData(
                    index, baseSectionSize, Qt.ItemDataRole.SizeHintRole
                )
        filter_model = ui.ClassFilterModel(len(first_columns))
        filter_model.setSourceModel(header_model)
        header_view_1.setModel(filter_model)
        header_view_2.setModel(header_model)
        header_view_1.setStretchLastSection(True)
        header_view_2.setStretchLastSection(True)
        return header_view_1, header_view_2

    @classmethod
    def create_context_menu(cls, menu_list: list[tuple[str, Callable]], pos):
        """
        Creates a context menu with the given list of actions and their corresponding functions.
        """
        menu = QMenu()
        actions = list()
        for [action_name, action_func] in menu_list:
            action = QAction(action_name)
            actions.append(action)
            action.triggered.connect(action_func)
        menu.addActions(actions)
        menu.exec(pos)

    @classmethod
    def tree_move_click_drag(cls, index: QModelIndex):
        """
        Handles the click and drag event for the tree view. It sets the checkstate of the item to the active checkstate.
        """
        active_checkstate = cls.get_mouse_press_checkstate()
        if active_checkstate is None or not index.isValid():
            return
        model = index.model()

        if isinstance(model, (ui.ClassModel, ui.PropertyModel)):
            fixed_column_count = model.fixed_column_count
        else:
            fixed_column_count = 0

        if (
            index.column() < fixed_column_count
            or not Qt.ItemFlag.ItemIsEnabled in index.flags()
        ):
            return

        model.setData(index, active_checkstate, Qt.ItemDataRole.CheckStateRole)
        model.dataChanged.emit(
            model.createIndex(0, 0),
            model.createIndex(model.rowCount(), model.columnCount()),
        )

    @classmethod
    def get_project_model(cls) -> ui.ProjectModel:
        pv = cls.get_project_view()
        if pv is None:
            return None
        return pv.model()

    @classmethod
    def get_class_views(cls) -> tuple[ui.ClassView, ui.ClassView]:
        window = cls.get_window()
        if window is None:
            return None, None
        return window.ui.class_treeView_fixed, window.ui.class_treeView_extendable

    @classmethod
    def get_class_model(cls) -> ui.ClassModel | None:
        view1, view2 = cls.get_class_views()
        if view2.model() is None:
            return view1.model().sourceModel()
        return view2.model()

    @classmethod
    def get_property_views(cls) -> tuple[ui.PropertyView, ui.PropertyView]:
        window = cls.get_window()
        if window is None:
            return None, None
        return (
            window.ui.property_TableView_fixed,
            window.ui.property_TableView_extendable,
        )

    @classmethod
    def get_property_model(cls) -> ui.PropertyModel | None:
        view1, view2 = cls.get_property_views()
        if view2 is None:
            return None
        return view2.model()

    @classmethod
    def get_class_header_model(cls) -> ui.CustomHeaderModel | None:
        view1, view2 = cls.get_class_views()
        if view2 is None:
            return None
        return view2.header().model()

    @classmethod
    def get_property_header_model(cls) -> ui.CustomHeaderModel | None:
        view1, view2 = cls.get_property_views()
        if view2 is None:
            return None
        return view2.horizontalHeader().model()

    @classmethod
    def get_property_label(cls) -> QLabel:
        window = cls.get_window()
        if window is None:
            return None
        return window.ui.property_label

    @classmethod
    def get_active_class(cls) -> SOMcreator.SOMClass | None:
        view1, view2 = cls.get_class_views()
        if not view1:
            return None
        indexes = view1.selectedIndexes()
        if not indexes:
            return None
        return view1.model().mapToSource(indexes[0]).internalPointer()

    @classmethod
    def is_mouse_pressed(cls) -> bool:
        return cls.get_properties().mouse_is_pressed

    @classmethod
    def set_mouse_pressed(cls, pressed: bool):
        cls.get_properties().mouse_is_pressed = pressed

    @classmethod
    def set_mouse_press_checkstate(cls, checkstate: bool):
        cls.get_properties().mouse_press_checkstate = checkstate

    @classmethod
    def get_mouse_press_checkstate(cls) -> bool:
        return cls.get_properties().mouse_press_checkstate
