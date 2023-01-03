from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QInputDialog, QLineEdit, QFileDialog
from SOMcreator import classes, constants
from lxml import etree
from configparser import ConfigParser

from ..windows import graphs_window, popups
from .. import settings

if TYPE_CHECKING:
    from ..main_window import MainWindow


def string_to_bool(text: str) -> bool | None:
    if text == str(True):
        return True
    elif text == str(False):
        return False
    else:
        return None


def iter_child(parent_node: graphs_window.Node):
    child: classes.Aggregation
    for child in parent_node.aggregation.children:
        child_node = graphs_window.aggregation_to_node(child)
        con_type = parent_node.aggregation.connection_dict[child_node.aggregation]
        parent_node.add_child(child_node, con_type)
        iter_child(child_node)


def import_node_pos(graph_window: graphs_window.GraphWindow, path: str):
    tree = etree.parse(path)
    projekt_xml = tree.getroot()
    xml_group_nodes = projekt_xml.find(constants.NODES)
    aggregation_dict = {aggregation.uuid: aggregation for aggregation in classes.Aggregation}
    node_dict:dict[str,(graphs_window.Node,float,float,bool)] = {}
    for xml_node in xml_group_nodes:
        uuid = xml_node.attrib.get(constants.IDENTIFIER)
        x_pos = float(xml_node.attrib.get(constants.X_POS))
        y_pos = float(xml_node.attrib.get(constants.Y_POS))
        aggregation: classes.Aggregation = aggregation_dict.get(uuid)
        node = graphs_window.Node(aggregation, graph_window)
        root = xml_node.attrib.get("root")
        if root == "True":
            root = True
        else:
            root = False
        node_dict[uuid] = (node, x_pos, y_pos, root)

    for node, x_pos, y_pos, root in node_dict.values():
        if root:
            graph_window.create_scene_by_node(node)
            graph_window.draw_tree(node)
            iter_child(node)
            graph_window.drawn_scenes.append(node.scene())

    for node, x_pos, y_pos, root in node_dict.values():
        node.setY(float(y_pos))
        node.setX(float(x_pos))

    graph_window.combo_box.setCurrentIndex(0)
    graph_window.combo_change()


def new_file(main_window: MainWindow) -> None:
    ok = popups.msg_unsaved()
    if ok:
        project_name = QInputDialog.getText(main_window, "New Project", "new Project Name:", QLineEdit.EchoMode.Normal, "")

        if project_name[1]:
            main_window.project = classes.Project(main_window.project, project_name[0])
            main_window.setWindowTitle(main_window.project.name)
            main_window.project.name = project_name[0]
            main_window.clear_all()


def merge_new_file(main_window):
    print(main_window)
    print("MERGE NEEDS TO BE PROGRAMMED")  # TODO: Write Merge


def open_file_clicked(main_window: MainWindow):
    def handle_old_data():
        if classes.Object:
            result = popups.msg_delete_or_merge()
            if result is None:
                return
            if result:
                main_window.clear_all()

    def get_path():
        file_text = "DRC Files (*.xml *.DRCxml *.xlsx);;" \
                    " xml Files (*.xml *.DRCxml);;" \
                    " Excel Files (*xlsx);;all (*.*)"

        cur_path = settings.get_file_path()
        if not os.path.exists(cur_path):
            cur_path = os.getcwd() + "/"
        return QFileDialog.getOpenFileName(main_window, "Open File", str(cur_path), file_text)[0]



    handle_old_data()
    path = get_path()
    print(path)
    _open_file_by_path(main_window,path)


def _open_file_by_path(main_window:MainWindow,path):
    def build_aggregations():
        gw = main_window.graph_window
        root_nodes = list()
        for aggreg in sorted(classes.Aggregation, key=lambda x: x.name):
            node = graphs_window.Node(aggreg, gw)
            if aggreg.is_root:
                root_nodes.append(node)

        for node in root_nodes:
            gw.create_scene_by_node(node)
            iter_child(node)
            gw.draw_tree(node)

        gw.combo_box.setCurrentIndex(0)
        gw.combo_change()

    if not path:
        return

    settings.set_file_path(path)
    project = main_window.project
    if path.endswith("xlsx"):
        project.import_excel(path)
        build_aggregations()
    else:
        project.open(path)
        import_node_pos(main_window.graph_window, path)

    main_window.ui.tree_object.resizeColumnToContents(0)
    main_window.load_graph(show=False)
    main_window.clear_object_input()
    main_window.fill_tree()