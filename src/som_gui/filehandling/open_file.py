from __future__ import annotations

import os
import shutil
import tempfile

import openpyxl
from PySide6.QtWidgets import QInputDialog, QLineEdit, QFileDialog
from PySide6.QtCore import QPointF
from SOMcreator import classes
from SOMcreator import constants as som_constants
from .. import settings
from ..data.constants import FILETYPE
from ..data import constants
from ..windows import popups
from ..windows.aggregation_view import aggregation_window
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..main_window import MainWindow


def iter_child(parent_node: aggregation_window.Node) -> None:
    child: classes.Aggregation
    for child in parent_node.aggregation.children:
        child_node = aggregation_window.aggregation_to_node(child)
        con_type = parent_node.aggregation.connection_dict[child_node.aggregation]
        parent_node.add_child(child_node, con_type)
        iter_child(child_node)


def import_node_pos(main_dict: dict, graph_window: aggregation_window.AggregationWindow) -> None:
    json_aggregation_dict: dict = main_dict[som_constants.AGGREGATIONS]
    aggregation_ref = {aggregation.uuid: aggregation for aggregation in classes.Aggregation}
    for uuid, aggregation_dict in json_aggregation_dict.items():
        aggregation = aggregation_ref[uuid]
        x_pos = aggregation_dict.get(som_constants.X_POS) or 0.0
        y_pos = aggregation_dict.get(som_constants.Y_POS) or 0.0
        graph_window.create_node(aggregation,QPointF(x_pos,y_pos))

    scene_dict = main_dict.get(constants.AGGREGATION_SCENES) or dict()
    graph_window.scene_dict.update(scene_dict)


def new_file(main_window: MainWindow) -> None:
    ok = popups.msg_unsaved()
    if ok:
        proj_name = QInputDialog.getText(main_window, "New Project", "new Project Name:", QLineEdit.EchoMode.Normal, "")

        if proj_name[1]:
            main_window.project = classes.Project(main_window.project, proj_name[0])
            main_window.setWindowTitle(main_window.project.name)
            main_window.project.name = proj_name[0]
            main_window.clear_all()


def merge_new_file(main_window: MainWindow) -> None:
    print(main_window)
    print("MERGE NEEDS TO BE PROGRAMMED")  # TODO: Write Merge


def request_delete_or_merge(main_window: MainWindow) -> None:
    if classes.Object:
        result = popups.msg_delete_or_merge()
        if result is None:
            return
        if result:
            main_window.clear_all()


def fill_ui(main_window: MainWindow) -> None:
    main_window.clear_object_input()
    main_window.fill_tree()


def get_path(main_window: MainWindow, title: str, file_text: str) -> str:
    cur_path = settings.get_open_path()
    if not os.path.exists(cur_path):
        cur_path = os.getcwd() + "/"
    return QFileDialog.getOpenFileName(main_window, title, str(cur_path), file_text)[0]


def import_excel_clicked(main_window: MainWindow) -> None:
    def build_aggregations():
        return #TODO: fix
        gw = main_window.graph_window
        root_nodes = list()
        for aggreg in sorted(classes.Aggregation, key=lambda x: x.name):
            node = aggregation_window.Node(aggreg, gw)
            if aggreg.is_root:
                root_nodes.append(node)

        for node in root_nodes:
            gw.create_scene_by_node(node)
            iter_child(node)
            gw.draw_tree(node)

        gw.combo_box.setCurrentIndex(0)
        gw.combo_change()

    request_delete_or_merge(main_window)
    path = get_path(main_window, "Import File", "Excel Files (*xlsx);;all (*.*)")
    if not path:
        return

    with tempfile.TemporaryDirectory() as tmpdirname:
        new_path = os.path.join(tmpdirname, "som_excel.xlsx")
        shutil.copy2(path, new_path)
        book = openpyxl.load_workbook(new_path)
        sheet_name, ok = popups.req_worksheet_name(main_window, book.sheetnames)
    if not ok:
        return
    main_window.project.import_excel(path, sheet_name)
    build_aggregations()
    fill_ui(main_window)


def open_file_clicked(main_window: MainWindow) -> None:
    path = get_path(main_window, "Open Project", FILETYPE)
    if not path:
        return

    settings.set_open_path(path)
    settings.set_save_path(path)
    main_dict = main_window.project.open(path)
    import_node_pos(main_dict, main_window.graph_window)
    fill_ui(main_window)
