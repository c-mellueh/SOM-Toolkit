from PySide6.QtWidgets import QTreeWidget

from som_gui import tool
from som_gui.core import object as core


def connect():
    widget: QTreeWidget = tool.Object.get_object_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, tool.Object))
    widget.itemSelectionChanged.connect(
        lambda: core.item_selection_changed(tool.Object, tool.PropertySet)
    )
    widget.itemDoubleClicked.connect(item_double_clicked)
    widget.customContextMenuRequested.connect(
        lambda p: core.create_context_menu(p, tool.Object)
    )
    widget.expanded.connect(lambda: core.resize_columns(tool.Object))

    # Connect MainWindow
    main_ui = tool.MainWindow.get_ui()
    main_ui.button_search.pressed.connect(
        lambda: core.search_object(tool.Search, tool.Object, tool.Project)
    )
    main_ui.button_objects_add.clicked.connect(
        lambda: core.add_object_clicked(
            tool.Object,
            tool.Project,
            tool.PropertySet,
            tool.PredefinedPropertySet,
            tool.Popups,
        )
    )
    main_ui.lineEdit_ident_pSet.textChanged.connect(
        lambda: core.ident_pset_changed(
            tool.Object, tool.MainWindow, tool.PredefinedPropertySet
        )
    )
    main_ui.lineEdit_ident_property.textChanged.connect(
        lambda: core.ident_property_changed(
            tool.Object, tool.MainWindow, tool.PredefinedPropertySet
        )
    )

    core.load_context_menus(tool.Object, tool.Util)
    core.add_shortcuts(
        tool.Object, tool.Util, tool.Search, tool.MainWindow, tool.Project
    )
    core.connect_object_input_widget(
        tool.Object, tool.MainWindow, tool.PredefinedPropertySet
    )
    core.init_main_window(tool.Object, tool.MainWindow)


def item_double_clicked():
    core.create_object_info_widget(mode=1, object_tool=tool.Object, util=tool.Util)


def object_info_paint_event():
    core.object_info_refresh(tool.Object)
    pass


def repaint_event():
    core.refresh_object_tree(tool.Object, tool.Project)


def drop_event(event):
    core.item_dropped_on(event.pos(), tool.Object)


def on_new_project():
    core.reset_tree(tool.Object)


def retranslate_ui():
    core.retranslate_ui(tool.Object)
