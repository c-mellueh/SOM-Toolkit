from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog, QMessageBox
from SOMcreator import json_constants

from . import FILETYPE
from .. import settings
from ..data import constants
from ..windows import popups

if TYPE_CHECKING:
    from ..main_window import MainWindow


def add_node_pos(main_window: MainWindow, main_dict: dict, path: str):
    def filter_scene_dict(scene_dict: dict) -> dict:
        new_dict = dict()
        for name, node_dict in scene_dict.items():
            node_list = node_dict[json_constants.NODES]
            if node_list:
                new_dict[name] = {json_constants.NODES: node_list}
        return new_dict

    aggregation_dict = main_dict[json_constants.AGGREGATIONS]
    for node in main_window.graph_window.nodes:
        uuid = node.aggregation.uuid
        try:
            aggregation_entry = aggregation_dict[uuid]
            aggregation_entry[json_constants.X_POS] = node.x()
            aggregation_entry[json_constants.Y_POS] = node.y()
        except KeyError:
            logging.warning(f"KeyError: {node}")

    main_dict[constants.AGGREGATION_SCENES] = filter_scene_dict(main_window.graph_window.scene_dict)

    with open(path, "w") as file:
        json.dump(main_dict, file, indent=2)
