from __future__ import annotations

from typing import TYPE_CHECKING

import SOMcreator
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtWidgets import QMainWindow, QSplitter
from SOMcreator.external_software.IDS import main
from SOMcreator.external_software.bim_collab_zoom import modelcheck as bc_modelcheck
from SOMcreator.external_software.desite import modelcheck
from anytree import AnyNode

from ... import icons
from ...filehandling import export
from ...qt_designs import ui_modelcheck
from ...widgets import object_check_widget, ifc_modelcheck_widget

if TYPE_CHECKING:
    from ...main_window import MainWindow


class ModelcheckWindow(QMainWindow):

    def __init__(self, main_window: MainWindow) -> None:
        def connect() -> None:
            self.widget.action_desite_js.triggered.connect(self.export_desite_js)
            self.widget.action_desite_attributes.triggered.connect(self.export_desite_attribute_table)
            self.widget.action_desite_csv.triggered.connect(self.export_desite_csv)
            self.widget.action_desite_fast.triggered.connect(self.export_desite_fast)
            self.widget.action_bimcollab_zoom.triggered.connect(self.export_bimcollab)
            self.widget.action_ids.triggered.connect(self.export_ids)

        super(ModelcheckWindow, self).__init__(main_window)
        self.widget = ui_modelcheck.Ui_Modelcheck()
        self.widget.setupUi(self)
        self.setWindowIcon(icons.get_icon())
        self.main_window = main_window
        connect()
        self.ifc_modelcheck = ifc_modelcheck_widget.ModelcheckWidget(main_window)
        self.data_model_widget = object_check_widget.ObjectCheckWidget(main_window)
        layout = self.widget.centralwidget.layout()
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)
        splitter.addWidget(self.data_model_widget)
        splitter.addWidget(self.ifc_modelcheck)
        self.show()

    def build_data_dict(self) -> dict[SOMcreator.Object, dict[SOMcreator.PropertySet, list[SOMcreator.Attribute]]]:
        def handle_item(model_index: QModelIndex):
            check_state = model_index.data(Qt.ItemDataRole.CheckStateRole)
            if not check_state == 2:
                return

            obj: SOMcreator.Object = model_index.data(object_check_widget.OBJECT_DATA_INDEX)

            if not self.data_model_widget.data_model[obj]:
                return

            data_dict[obj] = dict()
            for property_set in obj.property_sets:
                if not self.data_model_widget.data_model[property_set]:
                    continue
                data_dict[obj][property_set] = list()

                for attribute in property_set.attributes:
                    if self.data_model_widget.data_model[attribute]:
                        data_dict[obj][property_set].append(attribute)

            for r in range(model.rowCount(model_index)):
                child_index = model.index(r, 0, model_index)
                handle_item(child_index)

        tree = self.data_model_widget.widget.object_tree
        model = tree.model()
        root_index = tree.rootIndex()
        data_dict = dict()

        for row in range(model.rowCount(root_index)):
            handle_item(model.index(row, 0, root_index))
        return data_dict

    def export_ids(self):
        path = export.get_path(self.main_window, "ids")
        if not path:
            return
        data_dict = self.build_data_dict()
        main.export(self.main_window.project, data_dict, path)

    def export_bimcollab(self):
        path = export.get_path(self.main_window, "bcsv")
        if not path:
            return
        data_dict = self.build_data_dict()
        bc_modelcheck.export(data_dict, path, self.main_window.project.author)

    def export_desite_fast(self):
        path = export.get_path(self.main_window, "qa.xml")
        if not path:
            return
        pset = self.ifc_modelcheck.ident_pset
        attrib = self.ifc_modelcheck.ident_attribute
        data_dict = self.build_data_dict()
        modelcheck.fast_check(self.main_window.project, pset, attrib, data_dict, path)

    def export_desite_csv(self):
        path = export.get_path(self.main_window, "csv")
        if not path:
            return
        data_dict = self.build_data_dict()
        modelcheck._csv_export(self.main_window.project, data_dict, path)

    def export_desite_js(self):
        path = export.get_path(self.main_window, "qa.xml")
        if not path:
            return
        data_dict = self.build_data_dict()
        modelcheck.export(self.main_window.project, data_dict, path, project_tree=self.tree())

    def export_desite_attribute_table(self):
        path = export.get_path(self.main_window, "qa.xml")
        if not path:
            return
        data_dict = self.build_data_dict()
        modelcheck.export(self.main_window.project, data_dict, path, project_tree=self.tree(),
                          export_type=modelcheck.TABLE_EXPORT)

    def tree(self) -> AnyNode:
        def handle_item(model_index: QModelIndex, parent_node: AnyNode):
            check_state = model_index.data(Qt.ItemDataRole.CheckStateRole)
            if not check_state == 2:
                return

            obj = model_index.data(object_check_widget.OBJECT_DATA_INDEX)
            model_node = AnyNode(name=obj.name, id=obj.ident_value, obj=obj, parent=parent_node)
            for r in range(model.rowCount(model_index)):
                child_index = model.index(r, 0, model_index)
                handle_item(child_index, model_node)

        tree = self.data_model_widget.widget.object_tree
        model = tree.model()
        root_index = tree.rootIndex()

        base = AnyNode(id=self.main_window.project.name, name=self.main_window.project.name,
                       obj=self.main_window.project)

        for row in range(model.rowCount(root_index)):
            handle_item(model.index(row, 0, root_index), base)
        return base
