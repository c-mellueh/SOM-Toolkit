# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
                               QMenuBar, QPushButton, QSizePolicy, QSplitter,
                               QStatusBar, QTableWidgetItem, QTreeWidgetItem, QVBoxLayout,
                               QWidget)

from som_gui.module.attribute_table.ui import AttributeTable
from som_gui.module.object.ui import ObjectTreeWidget
from som_gui.module.property_set.ui import PsetTableWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1254, 710)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.action_file_new = QAction(MainWindow)
        self.action_file_new.setObjectName(u"action_file_new")
        self.action_file_Save = QAction(MainWindow)
        self.action_file_Save.setObjectName(u"action_file_Save")
        self.action_file_Save_As = QAction(MainWindow)
        self.action_file_Save_As.setObjectName(u"action_file_Save_As")
        self.action_file_Open = QAction(MainWindow)
        self.action_file_Open.setObjectName(u"action_file_Open")
        self.action_desite_Settings = QAction(MainWindow)
        self.action_desite_Settings.setObjectName(u"action_desite_Settings")
        self.action_desite_export = QAction(MainWindow)
        self.action_desite_export.setObjectName(u"action_desite_export")
        self.action_show_list = QAction(MainWindow)
        self.action_show_list.setObjectName(u"action_show_list")
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.action_export_bs = QAction(MainWindow)
        self.action_export_bs.setObjectName(u"action_export_bs")
        self.action_export_bookmarks = QAction(MainWindow)
        self.action_export_bookmarks.setObjectName(u"action_export_bookmarks")
        self.action_show_graphs = QAction(MainWindow)
        self.action_show_graphs.setObjectName(u"action_show_graphs")
        self.action_export_boq = QAction(MainWindow)
        self.action_export_boq.setObjectName(u"action_export_boq")
        self.action_mapping_options = QAction(MainWindow)
        self.action_mapping_options.setObjectName(u"action_mapping_options")
        self.action_mapping = QAction(MainWindow)
        self.action_mapping.setObjectName(u"action_mapping")
        self.action_shared_parameter = QAction(MainWindow)
        self.action_shared_parameter.setObjectName(u"action_shared_parameter")
        self.action_ifc_mapping = QAction(MainWindow)
        self.action_ifc_mapping.setObjectName(u"action_ifc_mapping")
        self.action_mapping_script = QAction(MainWindow)
        self.action_mapping_script.setObjectName(u"action_mapping_script")
        self.action_abbreviation_json = QAction(MainWindow)
        self.action_abbreviation_json.setObjectName(u"action_abbreviation_json")
        self.action_allplan = QAction(MainWindow)
        self.action_allplan.setObjectName(u"action_allplan")
        self.action_card1 = QAction(MainWindow)
        self.action_card1.setObjectName(u"action_card1")
        self.action_vestra = QAction(MainWindow)
        self.action_vestra.setObjectName(u"action_vestra")
        self.action_excel = QAction(MainWindow)
        self.action_excel.setObjectName(u"action_excel")
        self.action_import_excel = QAction(MainWindow)
        self.action_import_excel.setObjectName(u"action_import_excel")
        self.action_modelcheck = QAction(MainWindow)
        self.action_modelcheck.setObjectName(u"action_modelcheck")
        self.action_create_groups = QAction(MainWindow)
        self.action_create_groups.setObjectName(u"action_create_groups")
        self.action_model_control = QAction(MainWindow)
        self.action_model_control.setObjectName(u"action_model_control")
        self.action_project_phase = QAction(MainWindow)
        self.action_project_phase.setObjectName(u"action_project_phase")
        self.actionModellpr_fung_CSV = QAction(MainWindow)
        self.actionModellpr_fung_CSV.setObjectName(u"actionModellpr_fung_CSV")
        self.action_desite_js = QAction(MainWindow)
        self.action_desite_js.setObjectName(u"action_desite_js")
        self.action_desite_csv = QAction(MainWindow)
        self.action_desite_csv.setObjectName(u"action_desite_csv")
        self.action_bim_collab = QAction(MainWindow)
        self.action_bim_collab.setObjectName(u"action_bim_collab")
        self.action_model_control_v2 = QAction(MainWindow)
        self.action_model_control_v2.setObjectName(u"action_model_control_v2")
        self.action_use_cases = QAction(MainWindow)
        self.action_use_cases.setObjectName(u"action_use_cases")
        self.verticalLayout_main = QWidget(MainWindow)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout = QVBoxLayout(self.verticalLayout_main)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.verticalLayout_main)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_objects = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_objects.setObjectName(u"verticalLayout_objects")
        self.verticalLayout_objects.setContentsMargins(0, 0, 5, 0)
        self.gridLayout_objects = QGridLayout()
        self.gridLayout_objects.setObjectName(u"gridLayout_objects")
        self.button_objects_add = QPushButton(self.layoutWidget)
        self.button_objects_add.setObjectName(u"button_objects_add")
        self.button_objects_add.setAutoDefault(True)

        self.gridLayout_objects.addWidget(self.button_objects_add, 0, 5, 1, 1)

        self.horizontalLayout_object_button = QHBoxLayout()
        self.horizontalLayout_object_button.setObjectName(u"horizontalLayout_object_button")
        self.line_edit_object_name = QLineEdit(self.layoutWidget)
        self.line_edit_object_name.setObjectName(u"line_edit_object_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_object_name.sizePolicy().hasHeightForWidth())
        self.line_edit_object_name.setSizePolicy(sizePolicy)
        self.line_edit_object_name.setFrame(True)
        self.line_edit_object_name.setEchoMode(QLineEdit.Normal)
        self.line_edit_object_name.setClearButtonEnabled(False)

        self.horizontalLayout_object_button.addWidget(self.line_edit_object_name)


        self.gridLayout_objects.addLayout(self.horizontalLayout_object_button, 0, 2, 1, 3)

        self.lineEdit_ident_pSet = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_pSet.setObjectName(u"lineEdit_ident_pSet")
        sizePolicy.setHeightForWidth(self.lineEdit_ident_pSet.sizePolicy().hasHeightForWidth())
        self.lineEdit_ident_pSet.setSizePolicy(sizePolicy)
        self.lineEdit_ident_pSet.setFrame(True)
        self.lineEdit_ident_pSet.setEchoMode(QLineEdit.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_pSet, 1, 2, 1, 1)

        self.label_object_name = QLabel(self.layoutWidget)
        self.label_object_name.setObjectName(u"label_object_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_object_name.sizePolicy().hasHeightForWidth())
        self.label_object_name.setSizePolicy(sizePolicy1)
        self.label_object_name.setMinimumSize(QSize(30, 0))
        self.label_object_name.setLineWidth(1)

        self.gridLayout_objects.addWidget(self.label_object_name, 0, 1, 1, 1)

        self.lineEdit_ident_attribute = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_attribute.setObjectName(u"lineEdit_ident_attribute")
        sizePolicy.setHeightForWidth(self.lineEdit_ident_attribute.sizePolicy().hasHeightForWidth())
        self.lineEdit_ident_attribute.setSizePolicy(sizePolicy)
        self.lineEdit_ident_attribute.setFrame(True)
        self.lineEdit_ident_attribute.setEchoMode(QLineEdit.Normal)
        self.lineEdit_ident_attribute.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_attribute, 1, 3, 1, 1)

        self.button_search = QPushButton(self.layoutWidget)
        self.button_search.setObjectName(u"button_search")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy2)
        self.button_search.setMinimumSize(QSize(24, 0))
        self.button_search.setMaximumSize(QSize(24, 24))
        self.button_search.setIconSize(QSize(16, 16))

        self.gridLayout_objects.addWidget(self.button_search, 0, 0, 1, 1)

        self.lineEdit_ident_value = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_value.setObjectName(u"lineEdit_ident_value")
        self.lineEdit_ident_value.setFrame(True)
        self.lineEdit_ident_value.setEchoMode(QLineEdit.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_value, 1, 4, 1, 2)

        self.label_Ident = QLabel(self.layoutWidget)
        self.label_Ident.setObjectName(u"label_Ident")

        self.gridLayout_objects.addWidget(self.label_Ident, 1, 1, 1, 1)


        self.verticalLayout_objects.addLayout(self.gridLayout_objects)

        self.tree_object = ObjectTreeWidget(self.layoutWidget)
        self.tree_object.setObjectName(u"tree_object")
        self.tree_object.setEnabled(True)
        self.tree_object.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_object.setDragEnabled(True)
        self.tree_object.setDragDropOverwriteMode(False)
        self.tree_object.setDragDropMode(QAbstractItemView.InternalMove)
        self.tree_object.setDefaultDropAction(Qt.MoveAction)
        self.tree_object.setAlternatingRowColors(False)
        self.tree_object.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree_object.setSortingEnabled(True)
        self.tree_object.setExpandsOnDoubleClick(False)
        self.tree_object.header().setProperty("showSortIndicator", True)

        self.verticalLayout_objects.addWidget(self.tree_object)

        self.splitter.addWidget(self.layoutWidget)
        self.box_layout_pset = QWidget(self.splitter)
        self.box_layout_pset.setObjectName(u"box_layout_pset")
        self.gridLayout = QGridLayout(self.box_layout_pset)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_pSet_button = QHBoxLayout()
        self.horizontalLayout_pSet_button.setObjectName(u"horizontalLayout_pSet_button")
        self.label_pSet_name = QLabel(self.box_layout_pset)
        self.label_pSet_name.setObjectName(u"label_pSet_name")
        self.label_pSet_name.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_pSet_button.addWidget(self.label_pSet_name)

        self.lineEdit_pSet_name = QLineEdit(self.box_layout_pset)
        self.lineEdit_pSet_name.setObjectName(u"lineEdit_pSet_name")
        self.lineEdit_pSet_name.setFrame(True)

        self.horizontalLayout_pSet_button.addWidget(self.lineEdit_pSet_name)

        self.button_Pset_add = QPushButton(self.box_layout_pset)
        self.button_Pset_add.setObjectName(u"button_Pset_add")
        sizePolicy1.setHeightForWidth(self.button_Pset_add.sizePolicy().hasHeightForWidth())
        self.button_Pset_add.setSizePolicy(sizePolicy1)
        self.button_Pset_add.setAutoDefault(True)

        self.horizontalLayout_pSet_button.addWidget(self.button_Pset_add)


        self.gridLayout.addLayout(self.horizontalLayout_pSet_button, 2, 0, 1, 2)

        self.splitter_2 = QSplitter(self.box_layout_pset)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy3)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.table_pset = PsetTableWidget(self.splitter_2)
        if (self.table_pset.columnCount() < 3):
            self.table_pset.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_pset.setObjectName(u"table_pset")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.table_pset.sizePolicy().hasHeightForWidth())
        self.table_pset.setSizePolicy(sizePolicy4)
        self.table_pset.setFocusPolicy(Qt.StrongFocus)
        self.table_pset.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_pset.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_pset.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_pset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_pset.setSortingEnabled(True)
        self.splitter_2.addWidget(self.table_pset)
        self.table_pset.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_pset.horizontalHeader().setStretchLastSection(True)
        self.table_pset.verticalHeader().setVisible(False)
        self.table_pset.verticalHeader().setCascadingSectionResizes(False)
        self.table_attribute = AttributeTable(self.splitter_2)
        if (self.table_attribute.columnCount() < 4):
            self.table_attribute.setColumnCount(4)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        self.table_attribute.setObjectName(u"table_attribute")
        self.table_attribute.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_attribute.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_attribute.setSortingEnabled(True)
        self.splitter_2.addWidget(self.table_attribute)
        self.table_attribute.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.splitter_2, 3, 0, 1, 2)

        self.splitter.addWidget(self.box_layout_pset)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.verticalLayout_main)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1254, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.line_edit_object_name, self.lineEdit_ident_pSet)
        QWidget.setTabOrder(self.lineEdit_ident_pSet, self.lineEdit_ident_attribute)
        QWidget.setTabOrder(self.lineEdit_ident_attribute, self.lineEdit_ident_value)
        QWidget.setTabOrder(self.lineEdit_ident_value, self.button_objects_add)
        QWidget.setTabOrder(self.button_objects_add, self.tree_object)
        QWidget.setTabOrder(self.tree_object, self.button_search)
        QWidget.setTabOrder(self.button_search, self.lineEdit_pSet_name)
        QWidget.setTabOrder(self.lineEdit_pSet_name, self.button_Pset_add)
        QWidget.setTabOrder(self.button_Pset_add, self.table_pset)
        QWidget.setTabOrder(self.table_pset, self.table_attribute)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_file_new.setText(QCoreApplication.translate("MainWindow", u"Neu", None))
        self.action_file_Save.setText(QCoreApplication.translate("MainWindow", u"Speichern", None))
        self.action_file_Save_As.setText(QCoreApplication.translate("MainWindow", u"Speichern unter ...", None))
        self.action_file_Open.setText(QCoreApplication.translate("MainWindow", u"\u00d6ffnen", None))
#if QT_CONFIG(tooltip)
        self.action_file_Open.setToolTip(QCoreApplication.translate("MainWindow", u"\u00d6ffnet eine SOMjson Datei", None))
#endif // QT_CONFIG(tooltip)
        self.action_desite_Settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.action_desite_export.setText(QCoreApplication.translate("MainWindow", u"Modellpr\u00fcfung", None))
#if QT_CONFIG(tooltip)
        self.action_desite_export.setToolTip(QCoreApplication.translate("MainWindow", u"Erstellt eine qa.xml-Datei die in Desite als Pr\u00fcfdurchlauf eingelesen werden kann. Es wird dabei die Attribuierung von Entit\u00e4ten gepr\u00fcft", None))
#endif // QT_CONFIG(tooltip)
        self.action_show_list.setText(QCoreApplication.translate("MainWindow", u"Anzeigen", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"Einstellungen", None))
        self.action_export_bs.setText(QCoreApplication.translate("MainWindow", u"Export BS", None))
        self.action_export_bookmarks.setText(QCoreApplication.translate("MainWindow", u"Lesezeichen", None))
#if QT_CONFIG(tooltip)
        self.action_export_bookmarks.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Erstellt ein Script und eine bk.xml-Datei.</p><p>Es muss zuerst das Script ausgef\u00fchrt  werden bevor die bk.xml-Datei importiert wird!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.action_show_graphs.setText(QCoreApplication.translate("MainWindow", u"Anzeigen", None))
#if QT_CONFIG(tooltip)
        self.action_show_graphs.setToolTip(QCoreApplication.translate("MainWindow", u"die Aggregationsstruktur in welcher die einzelnen Objekte gespeichert werden k\u00f6nnen", None))
#endif // QT_CONFIG(tooltip)
        self.action_export_boq.setText(QCoreApplication.translate("MainWindow", u"Export  for BoQ", None))
        self.action_mapping_options.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.action_mapping.setText(QCoreApplication.translate("MainWindow", u"Mapping", None))
#if QT_CONFIG(tooltip)
        self.action_mapping.setToolTip(QCoreApplication.translate("MainWindow", u"Revit- & IFC-Mapping", None))
#endif // QT_CONFIG(tooltip)
        self.action_shared_parameter.setText(QCoreApplication.translate("MainWindow", u"Shared Parameters", None))
        self.action_ifc_mapping.setText(QCoreApplication.translate("MainWindow", u"IFC Mapping", None))
        self.action_mapping_script.setText(QCoreApplication.translate("MainWindow", u"Mapping Script", None))
#if QT_CONFIG(tooltip)
        self.action_mapping_script.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Das Mappingscript verschiebt Attribute aus einem ausgew\u00e4hlten PropertySet in die nach SOM richtigen PropertySets</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.action_abbreviation_json.setText(QCoreApplication.translate("MainWindow", u"Abbreviation JSON", None))
        self.action_allplan.setText(QCoreApplication.translate("MainWindow", u"Allplan", None))
        self.action_card1.setText(QCoreApplication.translate("MainWindow", u"CARD1", None))
        self.action_vestra.setText(QCoreApplication.translate("MainWindow", u"Verstra", None))
        self.action_excel.setText(QCoreApplication.translate("MainWindow", u"Excel", None))
        self.action_import_excel.setText(QCoreApplication.translate("MainWindow", u"Excel Importieren", None))
#if QT_CONFIG(tooltip)
        self.action_import_excel.setToolTip(QCoreApplication.translate("MainWindow", u"Importiert eine SOM-MaKa Excel", None))
#endif // QT_CONFIG(tooltip)
        self.action_modelcheck.setText(QCoreApplication.translate("MainWindow", u"Modellpr\u00fcfung", None))
        self.action_create_groups.setText(QCoreApplication.translate("MainWindow", u"Gruppen Generieren", None))
        self.action_model_control.setText(QCoreApplication.translate("MainWindow", u"Modellinformationen einlesen", None))
        self.action_project_phase.setText(QCoreApplication.translate("MainWindow", u"Leistungsphase", None))
        self.actionModellpr_fung_CSV.setText(QCoreApplication.translate("MainWindow", u"Modellpr\u00fcfung CSV", None))
        self.action_desite_js.setText(QCoreApplication.translate("MainWindow", u"Desite JavaScript", None))
        self.action_desite_csv.setText(QCoreApplication.translate("MainWindow", u"Desite CSV", None))
        self.action_bim_collab.setText(QCoreApplication.translate("MainWindow", u"BimCollabZoom", None))
        self.action_model_control_v2.setText(QCoreApplication.translate("MainWindow", u"Modellinformationen V2", None))
        self.action_use_cases.setText(QCoreApplication.translate("MainWindow", u"Anwendungsf\u00e4lle", None))
        self.button_objects_add.setText(QCoreApplication.translate("MainWindow", u"Erstellen", None))
#if QT_CONFIG(tooltip)
        self.line_edit_object_name.setToolTip(QCoreApplication.translate("MainWindow", u"Name der Objektvorgabe", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit_object_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Name", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_ident_pSet.setToolTip(QCoreApplication.translate("MainWindow", u"Name des PropertySets in dem das Identifier Attribut sich befindet", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_ident_pSet.setPlaceholderText(QCoreApplication.translate("MainWindow", u"PropertySet", None))
        self.label_object_name.setText(QCoreApplication.translate("MainWindow", u"Objektvorgabe", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_ident_attribute.setToolTip(QCoreApplication.translate("MainWindow", u"Name des Identifier Attributes", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_ident_attribute.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Attribut", None))
        self.button_search.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_ident_value.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Wert des Identifier Attributes</p><p>Dieser Wert darf nur einmal vorkommen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_ident_value.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Wert", None))
#if QT_CONFIG(tooltip)
        self.label_Ident.setToolTip(QCoreApplication.translate("MainWindow", u"Anhand des Identifiers wird bestimmt, welche Objektvorgabe auf eine Entit\u00e4t angewendet werden muss", None))
#endif // QT_CONFIG(tooltip)
        self.label_Ident.setText(QCoreApplication.translate("MainWindow", u"Identifier", None))
        self.label_pSet_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.button_Pset_add.setText(QCoreApplication.translate("MainWindow", u"Erstellen", None))
        ___qtablewidgetitem = self.table_pset.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"PropertySet", None));
        ___qtablewidgetitem1 = self.table_pset.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Geerbt von", None));
        ___qtablewidgetitem2 = self.table_pset.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Optional", None));
        ___qtablewidgetitem3 = self.table_attribute.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem4 = self.table_attribute.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Datentyp", None));
        ___qtablewidgetitem5 = self.table_attribute.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Format", None));
        ___qtablewidgetitem6 = self.table_attribute.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Wert", None));
    # retranslateUi

