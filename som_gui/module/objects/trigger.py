import som_gui
from som_gui.tool import Project, Objects
from som_gui.core import objects as core
from PySide6.QtWidgets import QTreeWidget
from som_gui.module.objects.prop import ObjectProperties, ObjectInfoWidgetProperties
from som_gui.module.objects.ui import ObjectInfoWidget

def connect():
    widget: QTreeWidget = Objects.get_object_tree()
    widget.itemChanged.connect(lambda item: core.item_changed(item, Objects))
    widget.itemSelectionChanged.connect(lambda: core.item_selection_changed(Objects))
    widget.itemDoubleClicked.connect(item_double_clicked)


def item_double_clicked():
    create_object_info_widget(mode=1)


def create_object_info_widget(mode: int):
    prop: ObjectProperties = som_gui.ObjectProperties
    prop.object_info_widget_properties = ObjectInfoWidgetProperties()
    prop.object_info_widget = ObjectInfoWidget()
    prop.object_info_widget_properties.mode = mode
    widget = prop.object_info_widget.widget
    widget.button_add_ifc.pressed.connect(lambda: core.object_info_add_ifc(Objects))
    widget.combo_box_pset.currentIndexChanged.connect(lambda: core.object_info_pset_changed(Objects))
    core.item_double_clicked(Objects)
    if prop.object_info_widget.exec():
        core.object_info_accept(Objects)


def item_copy_event():
    create_object_info_widget(mode=2)

def object_info_paint_event():
    core.object_info_refresh(Objects)
    pass

def repaint_event():
    core.refresh_object_tree(Objects, Project)


def change_event():
    core.item_changed(Objects)


def drop_event(event):
    print(F"DROP EVENT")
    core.item_dropped_on(event.pos(), Objects)
