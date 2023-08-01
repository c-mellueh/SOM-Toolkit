from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import SOMcreator.constants
from ..data.constants import FILETYPE
from PySide6.QtWidgets import QFileDialog, QMessageBox
from SOMcreator import constants as som_constants
from ..data import constants

import json

from ..windows import popups
from ..windows.aggregation_view import aggregation_window
from .. import settings

if TYPE_CHECKING:
    from ..main_window import MainWindow


def add_node_pos(main_window:MainWindow,main_dict:dict,path:str):
    aggregation_dict = main_dict[SOMcreator.constants.AGGREGATIONS]
    for node in main_window.graph_window.nodes:

        uuid = node.aggregation.uuid
        try:
            aggregation_entry = aggregation_dict[uuid]
            aggregation_entry[som_constants.X_POS] = node.x()
            aggregation_entry[som_constants.Y_POS] = node.y()
        except KeyError:
            print(node)


    main_dict[constants.AGGREGATION_SCENES] = main_window.graph_window.scene_dict

    with open(path,"w") as file:
        json.dump(main_dict,file,indent=2)

def save_clicked(main_window: MainWindow) -> str:
    path = settings.get_save_path()
    if not os.path.exists(path) or not path.endswith("json"):
        path = save_as_clicked(main_window)
    else:
        logging.info(f"Saved project to {path}")
        main_dict = main_window.project.save(path)
        add_node_pos(main_window,main_dict,path)
    return path


def save_as_clicked(main_window: MainWindow) -> str:
    path = settings.get_save_path()
    if not os.path.exists(path):
        path = \
            QFileDialog.getSaveFileName(main_window, "Save Project", "",FILETYPE)[0]
    else:
        path = os.path.splitext(path)[0]
        path = QFileDialog.getSaveFileName(main_window, "Save Project", path, FILETYPE)[0]

    if path:
        _save(main_window,path)
    return path

def _save(main_window:MainWindow,path):
    main_dict = main_window.project.save(path)
    add_node_pos(main_window,main_dict, path)
    settings.set_open_path(path)
    settings.set_save_path(path)
    print(f"Speichern abgeschlossen")

def close_event(main_window: MainWindow):
    status = main_window.project.changed
    if status:
        reply = popups.msg_close()
        if reply == QMessageBox.StandardButton.Save:
            path = save_clicked(main_window)
            if not path or path is None:
                return False
            else:
                return True
        elif reply == QMessageBox.StandardButton.No:
            return True
        else:
            return False
    else:
        return True
