from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtWidgets import QApplication
import som_gui

if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Project, Popups
    from som_gui import tool
    from som_gui.module.class_tree import ui as class_tree_ui
from PySide6.QtCore import QCoreApplication, Qt, QModelIndex, QSortFilterProxyModel
from PySide6.QtGui import QCloseEvent, QDropEvent
import SOMcreator

initial_tree = True


def init(
    main_window: Type[tool.MainWindow],
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
    class_tool:Type[tool.Class]
):
    """
    Create the actions used in the MainMenuBar. using add_action and set_action. Afterwards the Actions can be called by get_action. This is mostly used in retranslate_ui
    :param main_window:
    :return:
    """
    from som_gui.module.main_window import trigger

    main_window.connect_signals()
    open_window_action = main_window.add_action(
        "menuEdit", "ToggleConsole", trigger.toggle_console
    )
    main_window.set_action(trigger.TOOGLE_CONSOLE_ACTION, open_window_action)

    main_window.get_ui().button_search.pressed.connect(
        lambda: class_tree.signaller.search.emit(main_window.get_class_tree())
    )
    # init ClassTree
    from som_gui.module.class_tree.ui import ClassModel

    tree = main_window.get_class_tree()
    filter_model = QSortFilterProxyModel()
    filter_model.setSourceModel(ClassModel())
    tree.setModel(filter_model)
    filter_model.sourceModel().update_data()
    tree.setSortingEnabled(True)
    tree.sortByColumn(0,Qt.SortOrder.AscendingOrder)
    class_tree.add_tree(tree)
    class_tree.connect_tree(tree)
    tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    main_window.connect_class_tree()

    main_window.get_ui().button_classes_add.clicked.connect(
        lambda: class_info.trigger_class_info_widget(0, main_window.get_active_class())
    )

def retranslate_ui(
    main_window: Type[tool.MainWindow], class_tree: Type[tool.ClassTree]
):
    """
    retranslates the UI and the Actions of the Main Window
    :param main_window:
    :return:
    """
    from som_gui.module.main_window import trigger

    action = main_window.get_action(trigger.TOOGLE_CONSOLE_ACTION)
    if main_window.is_console_visible():
        action.setText(QCoreApplication.translate("MainWindow", "Hide Console"))
    else:
        action.setText(QCoreApplication.translate("MainWindow", "Show Console"))
    main_window.get().ui.retranslateUi(main_window.get())

    tree = main_window.get_class_tree()
    # ToDo: rewrite header retranslation


def create_main_window(
    application: QApplication,
    main_window: Type[tool.MainWindow],
    property_set: Type[tool.PropertySet],
):
    """
    Creates the main window from the given application and hides the console.
    :param application:
    :param main_window:
    :return:
    """
    mw = main_window.create(application)
    mw.show()
    table = main_window.get_property_set_table_widget()
    property_set.set_sorting_indicator(table, 0)
    main_window.hide_console()


def close_event(
    event: QCloseEvent,
    main_window: Type[tool.MainWindow],
    popups_tool: Type[tool.Popups],
):
    """
    Overwrites Close Event of MainWindow. Asks Save before exiting the main window
    :param event:
    :param main_window:
    :param popups_tool:
    :return:
    """
    reply = popups_tool.request_save_before_exit()
    if reply is None:
        # Dont Close Window
        event.ignore()
        return
    if reply:
        # Save before Closing
        from som_gui.module.project import trigger

        trigger.save()
    # Close Windows
    main_window.get_app().closeAllWindows()
    event.accept()


def refresh_main_window(
    main_window_tool: Type[MainWindow], project_tool: Type[Project]
):
    """
    refresh Statusbar-Text and Window-Title
    :param main_window_tool:
    :param project_tool:
    :return:
    """
    proj = project_tool.get()
    version = f'{QCoreApplication.translate("MainWindow", "Version")}: {proj.version}'
    phase_names = ",".join(proj.get_phase_by_index(i).name for i in proj.active_phases)
    usecase_names = ",".join(
        proj.get_usecase_by_index(i).name for i in proj.active_usecases
    )
    status = " | ".join([proj.name, version, phase_names, usecase_names])
    main_window_tool.set_status_bar_text(status)
    main_window_tool.set_window_title(f"SOM-Toolkit v{som_gui.__version__}")


def toggle_console_clicked(
    main_window: Type[tool.MainWindow], class_tree: Type[tool.ClassTree]
):
    """
    TOggles if Console is Shown
    :param main_window:
    :return:
    """
    main_window.toggle_console()
    retranslate_ui(
        main_window, class_tree
    )  # Changes Text from Show to Hide / from Hide to Show


def set_active_class(
    som_class: SOMcreator.SOMClass,
    main_window: Type[tool.MainWindow],
    property_set_tool: Type[tool.PropertySet],
):
    if som_class is None:
        property_set_tool.clear_table()
        property_set_tool.set_enabled(False)
        return

    selected_pset = property_set_tool.get_active_property_set()
    main_window.set_active_class(som_class)
    property_set_tool.update_completer(som_class)
    property_set_tool.set_enabled(True)
    property_set_tool.trigger_table_repaint()

    # reselect the same pset that is allready selected
    if not selected_pset:
        return
    pset = {
        p.name: p
        for p in property_set_tool.get_property_sets(main_window.get_active_class())
    }.get(selected_pset.name)
    if pset:
        property_set_tool.select_property_set(pset)


def define_class_tree_context_menu(
    main_window: Type[tool.MainWindow],
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
):
    tree = main_window.get_class_tree()
    class_tree.clear_context_menu_list(tree)
    class_tree.add_context_menu_entry(
        tree,
        lambda: QCoreApplication.translate("Class", "Copy"),
        lambda: class_info.trigger_class_info_widget(2, main_window.get_active_class()),
        True,
        True,
        False,
    )
    class_tree.add_context_menu_entry(
        tree,
        lambda: QCoreApplication.translate("Class", "Delete"),
        lambda: class_tree.delete_selection(tree),
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        tree,
        lambda: QCoreApplication.translate("Class", "Extend"),
        lambda: class_tree.expand_selection(tree),
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        tree,
        lambda: QCoreApplication.translate("Class", "Collapse"),
        lambda: class_tree.collapse_selection(tree),
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        tree,
        lambda: QCoreApplication.translate("Class", "Group"),
        lambda: class_tree.group_selection(tree),
        True,
        True,
        True,
    )
    class_tree.add_context_menu_entry(
        tree,
        lambda: QCoreApplication.translate("Class", "Info"),
        lambda: class_info.trigger_class_info_widget(1, main_window.get_active_class()),
        True,
        True,
        False,
    )


def one_new_project(
    main_window: Type[tool.MainWindow],
    class_tree: Type[tool.ClassTree],
):
    return


def add_class_tree_shortcuts(
    class_tree: Type[tool.ClassTree],
    util: Type[tool.Util],
    main_window: Type[tool.MainWindow],
    class_info: Type[tool.ClassInfo],
):
    tree = main_window.get_class_tree()
    util.add_shortcut(
        "Ctrl+X", main_window.get(), lambda: class_tree.delete_selection(tree)
    )
    util.add_shortcut(
        "Ctrl+G", main_window.get(), lambda: class_tree.group_selection(tree)
    )
    util.add_shortcut(
        "Ctrl+F",
        main_window.get(),
        lambda: class_tree.signaller.search.emit(tree),
    )
    util.add_shortcut(
        "Ctrl+C",
        main_window.get(),
        lambda: class_info.trigger_class_info_widget(2, main_window.get_active_class()),
    )


def add_class_tree_columns(
    main_window: Type[tool.MainWindow], class_tree: Type[tool.ClassTree]
):
    tree = main_window.get_class_tree()
    class_tree.add_column_to_tree(
        tree,
        lambda: QCoreApplication.translate("Class", "Class"),
        0,
        lambda c: getattr(c, "name"),
    )
    class_tree.add_column_to_tree(
        tree,
        lambda: QCoreApplication.translate("Class", "Identifier"),
        1,
        lambda o: (
            getattr(o, "ident_value")
            if isinstance(o.identifier_property, SOMcreator.SOMProperty)
            else ""
        ),
    )
    class_tree.add_column_to_tree(
        tree,
        lambda: QCoreApplication.translate("Class", "Optional"),
        2,
        lambda o: o.is_optional(ignore_hirarchy=True),
        lambda o, v: o.set_optional(v),
        role=Qt.ItemDataRole.CheckStateRole,
    )


def drop_on_class_tree(
    event: QDropEvent,
    main_window: Type[tool.MainWindow],
    class_tree: Type[tool.ClassTree],
    project: Type[tool.Project],
):
    pos = event.pos()
    source_table = event.source()
    target = main_window.get_class_tree()
    # TodO: Handle Drop Events
    if source_table == target:
        dropped_on_index = class_tree.get_index_from_pos(target, pos)
        class_tree.handle_class_move(target, dropped_on_index)
        return
    classes = class_tree.get_classes_from_mimedata(event.mimeData())
    if not classes:
        return
    for som_class in classes:
        project.get().add_item(som_class)

