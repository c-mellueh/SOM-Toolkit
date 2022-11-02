from __future__ import annotations

import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog, QMessageBox
from SOMcreator import constants, filehandling
from lxml import etree

from ..Windows import popups, graphs_window

if TYPE_CHECKING:
    from ..main_window import MainWindow


def add_node_pos(tree: etree.ElementTree):
    xml_group_nodes = tree.find(constants.NODES)
    node_dict = {node.aggregation.uuid: node for node in graphs_window.Node.registry}
    for xml_node in xml_group_nodes:
        uuid = xml_node.attrib.get(constants.IDENTIFIER)
        node = node_dict[uuid]
        xml_node.set(constants.X_POS, str(node.x()))
        xml_node.set(constants.Y_POS, str(node.y()))


def save_clicked(main_window: MainWindow) -> str:
    if main_window.save_path is None or not main_window.save_path.endswith("xml"):
        path = save_as_clicked(main_window)
    else:
        xml_tree = filehandling.build_xml(main_window.project)
        path = main_window.save_path
        add_node_pos(xml_tree)
        with open(path, "wb") as f:
            xml_tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)
    return path


def save_as_clicked(main_window: MainWindow) -> str:
    if main_window.save_path is not None:
        base_path = os.path.dirname(main_window.save_path)
        path = \
            QFileDialog.getSaveFileName(main_window, "Save XML", base_path, "xml Files (*.DRCxml *.xml )")[0]
    else:
        path = QFileDialog.getSaveFileName(main_window, "Save XML", "", "xml Files ( *.DRCxml *.xml)")[0]

    if path:
        xml_tree = filehandling.build_xml(main_window.project, )
        add_node_pos(xml_tree)
        with open(path, "wb") as f:
            xml_tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)
        main_window.save_path = path
    return path


def close_event(main_window: MainWindow):
    status = main_window.project.changed
    if status:
        reply = popups.msg_close()
        if reply == QMessageBox.Save:
            path = src.desiteRuleCreator.Filehandling.save_file.save_clicked(main_window)
            if not path or path is None:
                return False
            else:
                return True
        elif reply == QMessageBox.No:
            return True
        else:
            return False
    else:
        return True
