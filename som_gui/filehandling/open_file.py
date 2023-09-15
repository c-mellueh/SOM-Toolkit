from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QInputDialog, QLineEdit, QFileDialog
from SOMcreator import classes
from SOMcreator import json_constants

from .. import settings
from ..data import constants
from . import FILETYPE
from ..widgets import object_widget
from ..windows import popups
from ..windows.aggregation_view import aggregation_window

if TYPE_CHECKING:
    from ..main_window import MainWindow


def check_for_objects_without_aggregation(proj: classes.Project):
    for obj in proj.objects:
        if not obj.aggregations:
            logging.info(f"Objekt {obj.name} ({obj.ident_value} kommt in keiner Aggregation vor)")


def import_node_pos(main_dict: dict, graph_window: aggregation_window.AggregationWindow) -> None:
    json_aggregation_dict: dict = main_dict[json_constants.AGGREGATIONS]
    aggregation_ref = {aggregation.uuid: aggregation for aggregation in classes.Aggregation}
    for uuid, aggregation_dict in json_aggregation_dict.items():
        aggregation = aggregation_ref[uuid]
        x_pos = aggregation_dict.get(json_constants.X_POS) or 0.0
        y_pos = aggregation_dict.get(json_constants.Y_POS) or 0.0
        graph_window.create_node(aggregation, QPointF(x_pos, y_pos))

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


def fill_ui(main_window: MainWindow) -> None:
    object_widget.clear_object_input(main_window)
    object_widget.fill_tree(main_window)
    main_window.graph_window.is_initial_opening = True
    main_window.graph_window.hide()


def get_path(main_window: MainWindow, title: str, file_text: str) -> str:
    cur_path = settings.get_open_path()
    if not os.path.exists(cur_path):
        cur_path = os.getcwd() + "/"
    return QFileDialog.getOpenFileName(main_window, title, str(cur_path), file_text)[0]


def import_data(main_window: MainWindow, path: str):
    settings.set_open_path(path)
    settings.set_save_path(path)
    main_dict = main_window.project.open(path)
    import_node_pos(main_dict, main_window.graph_window)
    fill_ui(main_window)
    check_for_objects_without_aggregation(main_window.project)
    logging.info(f"Import Done!")
    main_window.generate_window_title()
    main_window.graph_window.create_missing_scenes()


def open_file_clicked(main_window: MainWindow) -> None:
    path = get_path(main_window, "Open Project", FILETYPE)
    if not path:
        return

    import_data(main_window, path)
