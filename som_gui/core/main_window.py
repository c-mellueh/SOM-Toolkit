from __future__ import annotations

from typing import TYPE_CHECKING, Type

from PySide6.QtWidgets import QApplication

import som_gui

if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Project, Popups
    from som_gui import tool
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QCloseEvent


def init(main_window: Type[tool.MainWindow], class_tree: Type[tool.ClassTree]):
    """
    Create the actions used in the MainMenuBar. using add_action and set_action. Afterwards the Actions can be called by get_action. This is mostly used in retranslate_ui
    :param main_window:
    :return:
    """
    from som_gui.module.main_window import trigger

    open_window_action = main_window.add_action(
        "menuEdit", "ToggleConsole", trigger.toggle_console
    )
    main_window.set_action(trigger.TOOGLE_CONSOLE_ACTION, open_window_action)
    class_tree.trigger_tree_init(main_window.get_class_tree_widget())
    main_window.get_ui().button_search.pressed.connect(
        lambda: class_tree.trigger_search(main_window.get_class_tree_widget())
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

    tree = main_window.get_class_tree_widget()
    header = tree.headerItem()
    for column, name in enumerate(class_tree.get_header_names(tree)):
        header.setText(column, name)


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


def toggle_console_clicked(main_window: Type[tool.MainWindow]):
    """
    TOggles if Console is Shown
    :param main_window:
    :return:
    """
    main_window.toggle_console()
    retranslate_ui(main_window)  # Changes Text from Show to Hide / from Hide to Show


def add_class_tree_shortcuts(
    class_tree: Type[tool.ClassTree],
    util: Type[tool.Util],
    main_window: Type[tool.MainWindow],
    class_info: Type[tool.ClassInfo],
):
    tree = main_window.get_class_tree_widget()
    util.add_shortcut(
        "Ctrl+X", main_window.get(), lambda: class_tree.delete_selection(tree)
    )
    util.add_shortcut(
        "Ctrl+G", main_window.get(), lambda: class_tree.group_selection(tree)
    )
    util.add_shortcut(
        "Ctrl+F",
        main_window.get(),
        lambda: class_tree.trigger_search(tree),
    )
    util.add_shortcut(
        "Ctrl+C",
        main_window.get(),
        lambda: class_info.trigger_class_info_widget(2, main_window.get_active_class()),
    )


def connect_class_tree(
    main_window: Type[tool.MainWindow],
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
):
    tree = main_window.get_class_tree_widget()
    tree.expanded.connect(lambda: class_tree.resize_tree(tree))
    tree.itemChanged.connect(lambda item: class_tree.update_check_state(tree, item))
    tree.itemSelectionChanged.connect(main_window.trigger_class_changed)

    tree.itemDoubleClicked.connect(
        lambda item: class_info.trigger_class_info_widget(
            1, class_tree.get_class_from_item(item)
        )
    )
    main_window.get_ui().button_classes_add.clicked.connect(
        lambda: class_info.trigger_class_info_widget(0, main_window.get_active_class())
    )


def class_selection_changed(
    main_window: Type[tool.MainWindow],
    class_tree: Type[tool.ClassTree],
    property_set_tool: Type[tool.PropertySet],
):
    tree = main_window.get_class_tree_widget()
    selected_items = class_tree.get_selected(tree)
    if len(selected_items) == 1:
        selected_pset = property_set_tool.get_active_property_set()
        som_class = class_tree.get_class_from_item(selected_items[0])
        main_window.set_active_class(som_class)
        property_set_tool.update_completer(som_class)
        property_set_tool.set_enabled(True)
        property_set_tool.trigger_table_repaint()

        # reselect the same pset that is allready selected
        if not selected_pset:
            return
        pset = {p.name: p for p in property_set_tool.get_property_sets()}.get(
            selected_pset.name
        )
        if pset:
            property_set_tool.select_property_set(pset)
    else:
        property_set_tool.clear_table()
        property_set_tool.set_enabled(False)


def define_class_tree_context_menu(
    main_window: Type[tool.MainWindow],
    class_tree: Type[tool.ClassTree],
    class_info: Type[tool.ClassInfo],
):
    tree = main_window.get_class_tree_widget()
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
    class_tree.reset_tree(main_window.get_class_tree_widget())
