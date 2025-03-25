from __future__ import annotations

from typing import Callable, TYPE_CHECKING, TextIO, Type

from PySide6.QtCore import QModelIndex, Qt,QSize
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QInputDialog,
    QLineEdit,
    QMenu,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QSplitter,
    QHeaderView)


import logging
import SOMcreator
import som_gui
import som_gui.core.tool
from som_gui import tool
from som_gui.module.property_ import ui as property_ui
from som_gui.module.project.constants import CLASS_REFERENCE

YELLOW = "#897e00"

if TYPE_CHECKING:
    from som_gui.module.filter_window.prop import (
        FilterWindowProperties,
        FilterCompareProperties,
    )
from som_gui.module.filter_window import ui, trigger, ui_header
from PySide6.QtCore import QCoreApplication


class FilterWindow(som_gui.core.tool.FilterWindow):
    @classmethod
    def get_properties(cls) -> FilterWindowProperties:
        return som_gui.FilterWindowProperties

    @classmethod
    def set_action(cls, name, action: QAction):
        cls.get_properties().actions[name] = action

    @classmethod
    def get_action(cls, name) -> QAction:
        return cls.get_properties().actions[name]

    @classmethod
    def get_project_table(cls) -> ui.ProjectView:
        return cls.get().ui.project_table

    @classmethod
    def get_class_trees(cls) -> list[ui.ClassTreeView]:
        return cls.get_properties().class_views

    @classmethod
    def get_class_model(cls) -> ui.ClassModel:
        return cls.get_properties().class_model

    @classmethod
    def get_pset_trees(cls) -> list[ui.PsetTreeView]:
        return cls.get_properties().pset_views

    @classmethod
    def get_pset_model(cls) -> ui.PsetModel:
        return cls.get_properties().pset_model

    @classmethod
    def create_widget(cls, project: SOMcreator.SOMProject) -> ui.FilterWidget:
        widget = ui.FilterWidget()
        cls.get_properties().widget = widget
        
        class_view_tree = ui.ClassTreeView(0)
        class_view_items = ui.ClassTreeView(1)
        cls.get_properties().class_views = [class_view_tree, class_view_items]
        class_model = ui.ClassModel(project)
        cls.get_properties().class_model = class_model
        names = [QCoreApplication.translate("FilterWidget","Class"),
                 QCoreApplication.translate("FilterWidget","Identifier")]
        cls.connect_views(
            project,
            class_model,
            widget.ui.class_splitter,
            class_view_tree,
            class_view_items,
            names,
        )

        pset_view_tree = ui.PsetTreeView(0)
        pset_view_items = ui.PsetTreeView(1)
        cls.get_properties().pset_views = [pset_view_tree, pset_view_items]

        pset_model = ui.PsetModel(project)
        cls.get_properties().pset_model = pset_model
        cls.connect_views(
            project,
            pset_model,
            widget.ui.property_splitter,
            pset_view_tree,
            pset_view_items,
            [QCoreApplication.translate("FilterWidget","PropertySet\nProperty")],
        )

        cls.get_properties().widget = widget
        return cls.get_properties().widget

    @classmethod
    def connect_views(
        cls,
        project: SOMcreator.SOMProject,
        tree_model: ui.TreeModel,
        splitter: QSplitter,
        view_1: ui.FilterTreeView,
        view_2: ui.FilterTreeView,
        first_columns: list[str],
    ):
        splitter.addWidget(view_1)
        splitter.addWidget(view_2)
        splitter.setHandleWidth(0)
        splitter.setChildrenCollapsible(False)
        view_1.setModel(tree_model)
        view_2.setModel(tree_model)
        view_2.setSelectionModel(view_1.selectionModel())
        cls.create_header_views(view_1,view_2,project,first_columns)
        

        view_1.header().setStretchLastSection(True)
        view_2.header().setStretchLastSection(True)

        sp = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
        )
        sp.setHorizontalStretch(1)

        view_2.setSizePolicy(sp)
        view_1.verticalScrollBar().valueChanged.connect(
            view_2.verticalScrollBar().setValue
        )
        view_2.verticalScrollBar().valueChanged.connect(
            view_1.verticalScrollBar().setValue
        )
        view_1.expanded.connect(view_2.expand)
        view_1.collapsed.connect(view_2.collapse)
        view_2.expanded.connect(view_1.expand)
        view_2.collapsed.connect(view_1.collapse)

    @classmethod
    def create_header_views(cls,view_1:ui.ClassTreeView|ui.PsetTreeView,view_2:ui.ClassTreeView|ui.PsetTreeView,project:SOMcreator.SOMProject,first_columns:list[str]):
        header_model =  ui_header.CustomHeaderModel(project, first_columns)
        header_view_1 = ui_header.CustomHeaderView(first_columns)
        header_view_2 = ui_header.CustomHeaderView(first_columns)
        baseSectionSize = QSize()
        baseSectionSize.setWidth(header_view_1.defaultSectionSize())
        baseSectionSize.setHeight(20)
        for row in range(header_model.rowCount()):
            for col in range(header_model.columnCount()):
                index = header_model.index(row, col)
                header_model.setData(index, baseSectionSize, Qt.ItemDataRole.SizeHintRole)
        header_view_1.setModel(header_model)
        header_view_2.setModel(header_model)
        view_1.setHeader(header_view_1)
        view_2.setHeader(header_view_2)


    @classmethod
    def connect_class_tree(cls, project: SOMcreator.SOMProject):
        class_tree = cls.get_class_trees()[0]
        class_tree.selectionModel().selectionChanged.connect(
            trigger.class_tree_clicked
        )

    @classmethod
    def connect_project_table(cls, project: SOMcreator.SOMProject):
        project_table = cls.get_project_table()
        model = ui.ProjectModel(project)
        project_table.setModel(model)
        model.data_changed_externally.connect(trigger.filter_changed_externally)
        horizontal_header = project_table.horizontalHeader()
        horizontal_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        horizontal_header.customContextMenuRequested.connect(
            trigger.pt_horizontal_context_requested
        )

        vertical_header = project_table.verticalHeader()
        vertical_header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        vertical_header.customContextMenuRequested.connect(
            trigger.pt_vertical_context_requested
        )

    @classmethod
    def get(cls) -> ui.FilterWidget | None:
        return cls.get_properties().widget

    @classmethod
    def add_usecase(cls, project: SOMcreator.SOMProject):

        text = QCoreApplication.translate("FilterWindow", "New UseCase")
        new_name = tool.Util.get_new_name(
            text, [uc.name for uc in project.get_usecases()]
        )
        logging.debug(f"Add UseCase '{new_name}'")
        usecase = SOMcreator.UseCase(new_name, new_name, new_name)
        model = cls.get_project_table().model()
        model.beginInsertColumns(
            QModelIndex(), model.columnCount(), model.columnCount()
        )
        model.project.add_usecase(usecase)
        model.endInsertColumns()

    @classmethod
    def remove_usecase(
        cls, usecase: SOMcreator.UseCase, project: SOMcreator.SOMProject
    ):
        logging.debug(f"remove UseCase '{usecase.name}'")
        model = cls.get_project_table().model()
        usecase_index = project.get_usecase_index(usecase)
        model.beginRemoveColumns(QModelIndex(), usecase_index, usecase_index)
        project.remove_usecase(usecase)
        model.endRemoveColumns()

    @classmethod
    def add_phase(cls, project: SOMcreator.SOMProject):
        text = QCoreApplication.translate("FilterWindow", "New Phase")
        new_name = tool.Util.get_new_name(
            text, [ph.name for ph in project.get_phases()]
        )
        logging.debug(f"Add Phase '{new_name}'")
        phase = SOMcreator.Phase(new_name, new_name, new_name)
        model = cls.get_project_table().model()
        model.beginInsertRows(QModelIndex(), model.rowCount(), model.rowCount())
        model.project.add_phase(phase)
        model.endInsertRows()

    @classmethod
    def remove_phase(cls, phase: SOMcreator.Phase, project: SOMcreator.SOMProject):
        logging.debug(f"remove Phase '{phase.name}'")
        model = cls.get_project_table().model()
        phase_index = project.get_phase_index(phase)
        model.beginRemoveRows(QModelIndex(), phase_index, phase_index)
        project.remove_phase(phase)
        model.endRemoveRows()

    @classmethod
    def rename_filter(cls, filter_: SOMcreator.UseCase | SOMcreator.Phase):
        title = QCoreApplication.translate("FilterWindow", "Edit Header")
        text = QCoreApplication.translate("FilterWindow", "Enter new header title:")

        new_name, ok = QInputDialog.getText(
            cls.get(), title, text, QLineEdit.EchoMode.Normal, filter_.name
        )
        if ok:
            filter_.name = new_name

    @classmethod
    def create_context_menu(cls, menu_list: list[tuple[str, Callable]], pos):
        menu = QMenu()
        actions = list()
        for [action_name, action_func] in menu_list:
            action = QAction(action_name)
            actions.append(action)
            action.triggered.connect(action_func)
        menu.addActions(actions)
        menu.exec(pos)

    @classmethod
    def set_active_class(cls, som_class: SOMcreator.SOMClass):
        cls.get_properties().active_class = som_class

    @classmethod
    def get_active_class(cls) -> SOMcreator.SOMClass:
        return cls.get_properties().active_class

    @classmethod
    def set_class_label(cls, value: str):
        return
        cls.get().ui.label.setText(value)

    @classmethod
    def is_tree_clicked(cls) -> bool:
        prop = cls.get_properties()
        return prop.tree_is_clicked

    @classmethod
    def tree_activate_click_drag(cls, index: QModelIndex):
        prop = cls.get_properties()
        prop.tree_is_clicked = True
        checkstate = not tool.Util.checkstate_to_bool(
            index.data(Qt.ItemDataRole.CheckStateRole)
        )
        prop.active_check_state = checkstate

    @classmethod
    def tree_move_click_drag(cls, index: QModelIndex):
        if not index.isValid():
            return
        if index.column() < index.model().check_column_index:
            return
        active_checkstate = cls.get_properties().active_check_state
        if active_checkstate is None:
            return
        model = index.model()
        if not Qt.ItemFlag.ItemIsEnabled in index.flags():
            return
        model.setData(index, active_checkstate, Qt.ItemDataRole.CheckStateRole)

    @classmethod
    def tree_release_click_drag(cls):
        prop = cls.get_properties()
        prop.tree_is_clicked = False
        prop.active_check_state = None

    @classmethod
    def set_settings_widget(cls, widget: ui.SettingsWidget):
        cls.get_properties().settings_widget = widget

    @classmethod
    def get_settings_widget(cls) -> ui.SettingsWidget:
        return cls.get_properties().settings_widget


class FilterCompare(som_gui.core.tool.FilterCompare):
    @classmethod
    def get_properties(cls) -> FilterCompareProperties:
        return som_gui.FilterCompareProperties

    @classmethod
    def reset(cls):
        prop = cls.get_properties()
        prop.usecase_list = list()
        prop.use_case_indexes = list()
        prop.phase_list = list()
        prop.phase_indexes = list()
        prop.projects = [None, None]
        prop.widget = None

    @classmethod
    def create_tree_selection_trigger(cls, widget: property_ui.PropertyWidget):
        widget.ui.tree_widget_class.itemSelectionChanged.connect(
            lambda: trigger.filter_tab_class_tree_selection_changed(widget)
        )

    @classmethod
    def find_matching_usecases(
        cls, proj0: SOMcreator.SOMProject = None, proj1: SOMcreator.SOMProject = None
    ):
        proj0 = proj0 or cls.get_project(0)
        proj1 = proj1 or cls.get_project(1)

        if not cls.get_usecase_list():
            usecases = set(proj0.get_usecases()).intersection(set(proj1.get_usecases()))
            cls.set_usecase_list(sorted(usecases, key=lambda x: x.name))
            for usecase in cls.get_usecase_list():
                index0 = proj0.get_usecase_index(usecase)
                index1 = proj1.get_usecase_index(usecase)
                cls.add_use_case_index_tuple((index0, index1))
        return cls.get_usecase_list()

    @classmethod
    def find_matching_phases(
        cls, proj0: SOMcreator.SOMProject = None, proj1: SOMcreator.SOMProject = None
    ):
        proj0 = proj0 or cls.get_project(0)
        proj1 = proj1 or cls.get_project(1)

        if not cls.get_properties().phase_list:
            phases = set(proj0.get_phases()).intersection(set(proj1.get_phases()))
            cls.set_phase_list(sorted(phases, key=lambda x: x.name))
            for phase in cls.get_phase_list():
                index0 = proj0.get_phase_index(phase)
                index1 = proj1.get_phase_index(phase)
                cls.add_phase_index_tuple((index0, index1))
        return cls.get_phase_list()

    @classmethod
    def append_collumns(cls, class_tree: QTreeWidget, pset_tree_widget: QTreeWidget):
        class_header_text = cls.get_existing_header_texts(class_tree)
        pset_header_text = cls.get_existing_header_texts(pset_tree_widget)

        match_list = cls.get_match_list()
        extra_header_texts = [f"{pp.name} - {uc.name}" for uc, pp in match_list]
        count = len(extra_header_texts)

        class_tree.setColumnCount(class_tree.columnCount() + count)
        pset_tree_widget.setColumnCount(pset_tree_widget.columnCount() + count)
        return
        class_tree.setHeaderLabels(class_header_text + extra_header_texts)
        pset_tree_widget.setHeaderLabels(pset_header_text + extra_header_texts)

    @classmethod
    def get_filter_list(cls, entity0, entity1) -> list[tuple[None | bool, None | bool]]:
        filter_list = list()
        for column, [usecase, phase] in enumerate(cls.get_match_list(), start=2):
            filter_list.append(
                (
                    (
                        entity0.get_filter_state(phase, usecase)
                        if entity0 is not None
                        else None
                    ),
                    (
                        entity1.get_filter_state(phase, usecase)
                        if entity1 is not None
                        else None
                    ),
                )
            )
        return filter_list

    @classmethod
    def are_all_filters_identical(
        cls, filter_list: list[tuple[None | bool, None | bool]]
    ) -> bool:
        return all(
            f0 == f1 for f0, f1 in filter_list if f0 is not None and f1 is not None
        )

    @classmethod
    def are_classes_identical(
        cls, class_0: SOMcreator.SOMClass, class_1: SOMcreator.SOMClass
    ) -> bool:
        filter_list = cls.get_filter_list(class_0, class_1)
        classes_are_identical = cls.are_all_filters_identical(filter_list)
        if not classes_are_identical:
            return False
        pset_lists = tool.PropertyCompare.get_pset_list(class_0)
        if pset_lists is None:
            return True
        for p0, p1 in pset_lists:
            if not cls.are_psets_identical(p0, p1):
                return False
        return True

    @classmethod
    def are_psets_identical(
        cls, pset0: SOMcreator.SOMPropertySet, pset1: SOMcreator.SOMPropertySet
    ) -> bool:
        filter_list = cls.get_filter_list(pset0, pset1)
        all_psets_are_identical = cls.are_all_filters_identical(filter_list)
        if not all_psets_are_identical:
            return False
        property_list = tool.PropertyCompare.get_property_list(pset0)
        if property_list is None:
            return True
        for a0, a1 in property_list:
            if not cls.are_properties_identical(a0, a1):
                return False
        return True

    @classmethod
    def are_properties_identical(
        cls, property_0: SOMcreator.SOMProperty, property_1: SOMcreator.SOMProperty
    ):
        filter_list = cls.get_filter_list(property_0, property_1)
        return cls.are_all_filters_identical(filter_list)

    @classmethod
    def fill_tree_with_checkstates(cls, item: QTreeWidgetItem) -> None:

        tree = item.treeWidget()
        entity_0, entity_1 = tool.PropertyCompare.get_entities_from_item(item)
        filter_list = cls.get_filter_list(entity_0, entity_1)
        for column, filter_state in enumerate(filter_list, start=2):
            widget = cls.create_combobox_widget(filter_state[0], filter_state[1])
            tree.setItemWidget(item, column, widget)
            if filter_state[0] != filter_state[1]:
                cls.set_tree_item_column_color(item, column, YELLOW)

        for child_index in range(item.childCount()):
            cls.fill_tree_with_checkstates(item.child(child_index))

    @classmethod
    def make_header_wordwrap(cls, tree: QTreeWidget) -> None:
        """because of long header texts make header wordwrap"""
        header = property_ui.WordWrapHeaderView(Qt.Orientation.Horizontal)
        tree.setHeader(header)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap
        )

    @classmethod
    def style_class_tree(cls, item: QTreeWidgetItem):
        entity_0: SOMcreator.SOMClass = item.data(0, CLASS_REFERENCE)
        entity_1: SOMcreator.SOMClass = item.data(1, CLASS_REFERENCE)
        for column, filter_state in enumerate(
            cls.get_filter_list(entity_0, entity_1), start=2
        ):
            if filter_state[0] != filter_state[1]:
                cls.set_tree_item_column_color(item, column, YELLOW)

        if not cls.are_classes_identical(entity_0, entity_1):
            cls.set_tree_item_column_color(item, 0, YELLOW)

        for child_index in range(item.childCount()):
            cls.style_class_tree(item.child(child_index))

    @classmethod
    def create_combobox_widget(cls, checkstate0: bool | None, checkstate1: bool | None):
        widget = QWidget()
        layout = QHBoxLayout()
        cb0 = QCheckBox()
        if checkstate0 is not None:
            cb0.setChecked(checkstate0)
        cb1 = QCheckBox()
        cb1.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        if checkstate1 is not None:
            cb1.setChecked(checkstate1)
        layout.addWidget(cb0)
        layout.addWidget(cb1)
        widget.setLayout(layout)
        cb0.setEnabled(False)
        cb1.setEnabled(False)
        return widget

    @classmethod
    def export_write_statechange(
        cls, file: TextIO, type_name: str, filter_list, indent: int
    ):
        matches = cls.get_match_list()
        for index, (f0, f1) in enumerate(filter_list):
            if f0 == f1:
                continue
            usecase, phase = matches[index]
            text = QCoreApplication.translate(
                "FilterWindow", "{}{} [{}][{}] state changed from {} to {}\n"
            )
            file.write(
                text.format("   " * indent, type_name, usecase.name, phase.name, f0, f1)
            )

    @classmethod
    def export_class_filter_differences(
        cls, file: TextIO, property_compare: Type[tool.PropertyCompare]
    ):
        project_0 = cls.get_project(0)
        class_dict = property_compare.get_class_dict()
        for class_0 in sorted(
            project_0.get_classes(filter=False), key=lambda x: x.name
        ):
            class_1 = class_dict[class_0]
            if class_1 is None:
                continue
            if cls.are_classes_identical(class_0, class_1):
                continue
            filter_list = cls.get_filter_list(class_0, class_1)
            text = QCoreApplication.translate("FilterWindow", "Class")

            file.write(f"\n{text} '{class_0.name}' ({class_0.ident_value}):\n")
            cls.export_write_statechange(file, text, filter_list, 1)
            pset_list = property_compare.get_properties().pset_lists.get(class_0)
            cls.export_pset_filter_differences(file, pset_list, property_compare)

    @classmethod
    def export_pset_filter_differences(
        cls, file, pset_list, property_compare: Type[tool.PropertyCompare]
    ):
        if pset_list is None:
            return
        for p0, p1 in sorted(
            pset_list, key=lambda x: x[0].name if x[0] is not None else "aaa"
        ):
            if p0 is None or p1 is None:
                continue
            if cls.are_psets_identical(p0, p1):
                continue
            text = QCoreApplication.translate("FilterWindow", "PropertySet")

            file.write(f"   {text} '{p0.name}':\n")
            filter_list = cls.get_filter_list(p0, p1)
            cls.export_write_statechange(file, text, filter_list, 2)
            property_list = property_compare.get_properties().properties_lists.get(p0)
            cls.export_property_filter_differnces(file, property_list)

    @classmethod
    def export_property_filter_differnces(
        cls,
        file,
        property_list: list[
            tuple[SOMcreator.SOMProperty | None, SOMcreator.SOMProperty | None]
        ],
    ):
        matches = cls.get_match_list()

        if property_list is None:
            return
        for p_0, p_1 in sorted(
            property_list, key=lambda x: x[0].name if x[0] is not None else "aaa"
        ):
            if p_0 is None or p_1 is None:
                continue
            if cls.are_properties_identical(p_0, p_1):
                continue
            filter_list = cls.get_filter_list(p_0, p_1)
            for index, (f0, f1) in enumerate(filter_list):
                if f0 == f1:
                    continue
                usecase, phase = matches[index]
                use_case_phase_text = f"[{usecase.name}][{phase.name}]"
                text = QCoreApplication.translate(
                    "FilterWindow",
                    "Property {0:30} {1:30} state changed from {2:5} to {3:5}\n",
                )
                text = f"      {text}"
                file.write(
                    text.format(f"'{p_0.name}'", use_case_phase_text, str(f0), str(f1))
                )

    # GETTER & SETTER

    @classmethod
    def set_projects(cls, project1, project2) -> None:
        cls.get_properties().projects = [project1, project2]

    @classmethod
    def get_project(cls, index=1) -> SOMcreator.SOMProject:
        return cls.get_properties().projects[index]

    @classmethod
    def create_widget(cls):
        if cls.get_properties().widget is None:
            cls.get_properties().widget = property_ui.PropertyWidget()
            cls.get_properties().widget.ui.table_widget_values.hide()
            cls.get_properties().widget.ui.table_infos.hide()
        return cls.get_properties().widget

    @classmethod
    def get_widget(cls) -> property_ui.PropertyWidget:
        return cls.get_properties().widget

    @classmethod
    def get_class_tree(cls):
        return cls.get_widget().ui.tree_widget_class

    @classmethod
    def get_usecase_list(cls) -> list[SOMcreator.UseCase]:
        return cls.get_properties().usecase_list

    @classmethod
    def set_usecase_list(cls, usecase_list: list[SOMcreator.UseCase]):
        cls.get_properties().usecase_list = usecase_list

    @classmethod
    def add_use_case_index_tuple(cls, value: tuple[int, int]):
        cls.get_properties().use_case_indexes.append(value)

    @classmethod
    def get_phase_list(cls) -> list[SOMcreator.Phase]:
        return cls.get_properties().phase_list

    @classmethod
    def set_phase_list(cls, phase_list: list[SOMcreator.Phase]):
        cls.get_properties().phase_list = phase_list

    @classmethod
    def add_phase_index_tuple(cls, value: tuple[int, int]):
        cls.get_properties().phase_indexes.append(value)

    @classmethod
    def get_match_list(cls) -> list[tuple[SOMcreator.UseCase, SOMcreator.Phase]]:
        usecases = cls.get_usecase_list()
        phases = cls.get_phase_list()
        if not cls.get_properties().match_list:
            cls.get_properties().match_list = [
                (usecase, phase) for usecase in usecases for phase in phases
            ]
        return cls.get_properties().match_list

    @classmethod
    def get_existing_header_texts(cls, tree_widget: QTreeWidget) -> list[str]:
        header = tree_widget.headerItem()
        return [header.text(index) for index in range(header.columnCount())]

    @classmethod
    def set_tree_item_column_color(cls, item: QTreeWidgetItem, column: int, color: str):
        tree = item.treeWidget()
        index = tree.indexFromItem(item, 0)
        tool.PropertyCompare.set_branch_color(tree, index, color)
        color = QColor(color)
        item.setBackground(column, color)
        item.setData(CLASS_REFERENCE + 1, column, 1)
        item.setBackground(0, color)
        item.setBackground(1, color)
        item.setData(0, CLASS_REFERENCE + 1, 1)
