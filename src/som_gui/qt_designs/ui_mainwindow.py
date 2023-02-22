# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1261, 495)
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
        self.action_mapping_Script = QAction(MainWindow)
        self.action_mapping_Script.setObjectName(u"action_mapping_Script")
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
        self.verticalLayout_objects.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_objects = QGridLayout()
        self.gridLayout_objects.setObjectName(u"gridLayout_objects")
        self.label_Ident = QLabel(self.layoutWidget)
        self.label_Ident.setObjectName(u"label_Ident")

        self.gridLayout_objects.addWidget(self.label_Ident, 1, 0, 1, 1)

        self.lineEdit_ident_attribute = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_attribute.setObjectName(u"lineEdit_ident_attribute")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ident_attribute.sizePolicy().hasHeightForWidth())
        self.lineEdit_ident_attribute.setSizePolicy(sizePolicy)
        self.lineEdit_ident_attribute.setFrame(True)
        self.lineEdit_ident_attribute.setEchoMode(QLineEdit.Normal)
        self.lineEdit_ident_attribute.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_attribute, 1, 2, 1, 1)

        self.lineEdit_ident_pSet = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_pSet.setObjectName(u"lineEdit_ident_pSet")
        sizePolicy.setHeightForWidth(self.lineEdit_ident_pSet.sizePolicy().hasHeightForWidth())
        self.lineEdit_ident_pSet.setSizePolicy(sizePolicy)
        self.lineEdit_ident_pSet.setFrame(True)
        self.lineEdit_ident_pSet.setEchoMode(QLineEdit.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_pSet, 1, 1, 1, 1)

        self.label_object_name = QLabel(self.layoutWidget)
        self.label_object_name.setObjectName(u"label_object_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_object_name.sizePolicy().hasHeightForWidth())
        self.label_object_name.setSizePolicy(sizePolicy1)
        self.label_object_name.setMinimumSize(QSize(30, 0))
        self.label_object_name.setLineWidth(1)

        self.gridLayout_objects.addWidget(self.label_object_name, 0, 0, 1, 1)

        self.lineEdit_ident_value = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_value.setObjectName(u"lineEdit_ident_value")
        self.lineEdit_ident_value.setFrame(True)
        self.lineEdit_ident_value.setEchoMode(QLineEdit.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_value, 1, 3, 1, 1)

        self.horizontalLayout_object_button = QHBoxLayout()
        self.horizontalLayout_object_button.setObjectName(u"horizontalLayout_object_button")
        self.lineEdit_object_name = QLineEdit(self.layoutWidget)
        self.lineEdit_object_name.setObjectName(u"lineEdit_object_name")
        sizePolicy.setHeightForWidth(self.lineEdit_object_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_object_name.setSizePolicy(sizePolicy)
        self.lineEdit_object_name.setFrame(True)
        self.lineEdit_object_name.setEchoMode(QLineEdit.Normal)

        self.horizontalLayout_object_button.addWidget(self.lineEdit_object_name)

        self.button_objects_add = QPushButton(self.layoutWidget)
        self.button_objects_add.setObjectName(u"button_objects_add")
        self.button_objects_add.setAutoDefault(True)

        self.horizontalLayout_object_button.addWidget(self.button_objects_add)


        self.gridLayout_objects.addLayout(self.horizontalLayout_object_button, 0, 1, 1, 3)


        self.verticalLayout_objects.addLayout(self.gridLayout_objects)

        self.tree_object = QTreeWidget(self.layoutWidget)
        self.tree_object.setObjectName(u"tree_object")
        self.tree_object.setEnabled(True)
        self.tree_object.setDragDropMode(QAbstractItemView.InternalMove)
        self.tree_object.setDefaultDropAction(Qt.MoveAction)
        self.tree_object.setAlternatingRowColors(False)
        self.tree_object.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree_object.setSortingEnabled(True)
        self.tree_object.setExpandsOnDoubleClick(False)
        self.tree_object.header().setProperty("showSortIndicator", True)

        self.verticalLayout_objects.addWidget(self.tree_object)

        self.splitter.addWidget(self.layoutWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_property_set = QWidget()
        self.tab_property_set.setObjectName(u"tab_property_set")
        self.tab_property_set.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.tab_property_set)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter_2 = QSplitter(self.tab_property_set)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy2)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.table_pset = QTableWidget(self.splitter_2)
        if (self.table_pset.columnCount() < 2):
            self.table_pset.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.table_pset.rowCount() < 1):
            self.table_pset.setRowCount(1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_pset.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_pset.setItem(0, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_pset.setItem(0, 1, __qtablewidgetitem4)
        self.table_pset.setObjectName(u"table_pset")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.table_pset.sizePolicy().hasHeightForWidth())
        self.table_pset.setSizePolicy(sizePolicy3)
        self.table_pset.setFocusPolicy(Qt.StrongFocus)
        self.table_pset.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_pset.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_pset.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_pset.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_pset.setSortingEnabled(True)
        self.splitter_2.addWidget(self.table_pset)
        self.table_pset.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_pset.verticalHeader().setVisible(False)
        self.table_pset.verticalHeader().setCascadingSectionResizes(False)
        self.table_attribute = QTableWidget(self.splitter_2)
        if (self.table_attribute.columnCount() < 4):
            self.table_attribute.setColumnCount(4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_attribute.setHorizontalHeaderItem(3, __qtablewidgetitem8)
        self.table_attribute.setObjectName(u"table_attribute")
        self.table_attribute.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.splitter_2.addWidget(self.table_attribute)

        self.gridLayout.addWidget(self.splitter_2, 3, 0, 1, 2)

        self.horizontalLayout_pSet_button = QHBoxLayout()
        self.horizontalLayout_pSet_button.setObjectName(u"horizontalLayout_pSet_button")
        self.label_pSet_name = QLabel(self.tab_property_set)
        self.label_pSet_name.setObjectName(u"label_pSet_name")
        self.label_pSet_name.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_pSet_button.addWidget(self.label_pSet_name)

        self.lineEdit_pSet_name = QLineEdit(self.tab_property_set)
        self.lineEdit_pSet_name.setObjectName(u"lineEdit_pSet_name")
        self.lineEdit_pSet_name.setFrame(True)

        self.horizontalLayout_pSet_button.addWidget(self.lineEdit_pSet_name)

        self.button_Pset_add = QPushButton(self.tab_property_set)
        self.button_Pset_add.setObjectName(u"button_Pset_add")
        sizePolicy1.setHeightForWidth(self.button_Pset_add.sizePolicy().hasHeightForWidth())
        self.button_Pset_add.setSizePolicy(sizePolicy1)
        self.button_Pset_add.setAutoDefault(True)

        self.horizontalLayout_pSet_button.addWidget(self.button_Pset_add)


        self.gridLayout.addLayout(self.horizontalLayout_pSet_button, 2, 0, 1, 2)

        self.tabWidget.addTab(self.tab_property_set, "")
        self.tab_code = QWidget()
        self.tab_code.setObjectName(u"tab_code")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_code)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widget_vertical_stack = QWidget(self.tab_code)
        self.widget_vertical_stack.setObjectName(u"widget_vertical_stack")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_vertical_stack.sizePolicy().hasHeightForWidth())
        self.widget_vertical_stack.setSizePolicy(sizePolicy4)
        self.verticalLayout_4 = QVBoxLayout(self.widget_vertical_stack)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_script_title = QLabel(self.widget_vertical_stack)
        self.label_script_title.setObjectName(u"label_script_title")

        self.verticalLayout_4.addWidget(self.label_script_title)

        self.listWidget_scripts = QListWidget(self.widget_vertical_stack)
        QListWidgetItem(self.listWidget_scripts)
        QListWidgetItem(self.listWidget_scripts)
        QListWidgetItem(self.listWidget_scripts)
        QListWidgetItem(self.listWidget_scripts)
        QListWidgetItem(self.listWidget_scripts)
        self.listWidget_scripts.setObjectName(u"listWidget_scripts")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.listWidget_scripts.sizePolicy().hasHeightForWidth())
        self.listWidget_scripts.setSizePolicy(sizePolicy5)
        self.listWidget_scripts.setMaximumSize(QSize(161, 16777215))
        self.listWidget_scripts.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)

        self.verticalLayout_4.addWidget(self.listWidget_scripts)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_add_script = QPushButton(self.widget_vertical_stack)
        self.pushButton_add_script.setObjectName(u"pushButton_add_script")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pushButton_add_script.sizePolicy().hasHeightForWidth())
        self.pushButton_add_script.setSizePolicy(sizePolicy6)
        self.pushButton_add_script.setMinimumSize(QSize(25, 25))
        self.pushButton_add_script.setMaximumSize(QSize(21, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButton_add_script)

        self.pushButton_delete_script = QPushButton(self.widget_vertical_stack)
        self.pushButton_delete_script.setObjectName(u"pushButton_delete_script")
        sizePolicy6.setHeightForWidth(self.pushButton_delete_script.sizePolicy().hasHeightForWidth())
        self.pushButton_delete_script.setSizePolicy(sizePolicy6)
        self.pushButton_delete_script.setMinimumSize(QSize(25, 25))
        self.pushButton_delete_script.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.pushButton_delete_script)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_import_script = QPushButton(self.widget_vertical_stack)
        self.pushButton_import_script.setObjectName(u"pushButton_import_script")
        sizePolicy6.setHeightForWidth(self.pushButton_import_script.sizePolicy().hasHeightForWidth())
        self.pushButton_import_script.setSizePolicy(sizePolicy6)
        self.pushButton_import_script.setMinimumSize(QSize(25, 25))
        self.pushButton_import_script.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.pushButton_import_script)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addWidget(self.widget_vertical_stack)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_burger = QPushButton(self.tab_code)
        self.pushButton_burger.setObjectName(u"pushButton_burger")
        sizePolicy.setHeightForWidth(self.pushButton_burger.sizePolicy().hasHeightForWidth())
        self.pushButton_burger.setSizePolicy(sizePolicy)
        self.pushButton_burger.setMinimumSize(QSize(25, 25))
        self.pushButton_burger.setMaximumSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButton_burger)

        self.pushButton_left = QPushButton(self.tab_code)
        self.pushButton_left.setObjectName(u"pushButton_left")
        sizePolicy.setHeightForWidth(self.pushButton_left.sizePolicy().hasHeightForWidth())
        self.pushButton_left.setSizePolicy(sizePolicy)
        self.pushButton_left.setMinimumSize(QSize(25, 25))
        self.pushButton_left.setMaximumSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButton_left)

        self.pushButton_right = QPushButton(self.tab_code)
        self.pushButton_right.setObjectName(u"pushButton_right")
        sizePolicy.setHeightForWidth(self.pushButton_right.sizePolicy().hasHeightForWidth())
        self.pushButton_right.setSizePolicy(sizePolicy)
        self.pushButton_right.setMinimumSize(QSize(25, 25))
        self.pushButton_right.setMaximumSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.pushButton_right)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_script_name = QLabel(self.tab_code)
        self.label_script_name.setObjectName(u"label_script_name")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(2)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_script_name.sizePolicy().hasHeightForWidth())
        self.label_script_name.setSizePolicy(sizePolicy7)

        self.horizontalLayout.addWidget(self.label_script_name)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.code_edit = QTextEdit(self.tab_code)
        self.code_edit.setObjectName(u"code_edit")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy8.setHorizontalStretch(2)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.code_edit.sizePolicy().hasHeightForWidth())
        self.code_edit.setSizePolicy(sizePolicy8)

        self.verticalLayout_2.addWidget(self.code_edit)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.tab_code, "")
        self.splitter.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.verticalLayout_main)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1261, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuExport = QMenu(self.menuFile)
        self.menuExport.setObjectName(u"menuExport")
        self.menuDesite = QMenu(self.menubar)
        self.menuDesite.setObjectName(u"menuDesite")
        self.menuPredefined_Psets = QMenu(self.menubar)
        self.menuPredefined_Psets.setObjectName(u"menuPredefined_Psets")
        self.menuShow_Graphs = QMenu(self.menubar)
        self.menuShow_Graphs.setObjectName(u"menuShow_Graphs")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.lineEdit_ident_pSet, self.lineEdit_ident_attribute)
        QWidget.setTabOrder(self.lineEdit_ident_attribute, self.lineEdit_ident_value)
        QWidget.setTabOrder(self.lineEdit_ident_value, self.button_objects_add)
        QWidget.setTabOrder(self.button_objects_add, self.tree_object)
        QWidget.setTabOrder(self.tree_object, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.pushButton_delete_script)
        QWidget.setTabOrder(self.pushButton_delete_script, self.pushButton_import_script)
        QWidget.setTabOrder(self.pushButton_import_script, self.pushButton_burger)
        QWidget.setTabOrder(self.pushButton_burger, self.pushButton_left)
        QWidget.setTabOrder(self.pushButton_left, self.listWidget_scripts)
        QWidget.setTabOrder(self.listWidget_scripts, self.pushButton_add_script)
        QWidget.setTabOrder(self.pushButton_add_script, self.pushButton_right)
        QWidget.setTabOrder(self.pushButton_right, self.code_edit)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDesite.menuAction())
        self.menubar.addAction(self.menuPredefined_Psets.menuAction())
        self.menubar.addAction(self.menuShow_Graphs.menuAction())
        self.menuFile.addAction(self.action_file_new)
        self.menuFile.addAction(self.action_file_Open)
        self.menuFile.addAction(self.action_file_Save)
        self.menuFile.addAction(self.action_file_Save_As)
        self.menuFile.addAction(self.action_settings)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuFile.addAction(self.action_mapping)
        self.menuExport.addAction(self.action_abbreviation_json)
        self.menuExport.addAction(self.action_allplan)
        self.menuExport.addAction(self.action_card1)
        self.menuExport.addAction(self.action_vestra)
        self.menuExport.addAction(self.action_excel)
        self.menuDesite.addAction(self.action_desite_export)
        self.menuDesite.addAction(self.action_export_bs)
        self.menuDesite.addAction(self.action_export_bookmarks)
        self.menuDesite.addAction(self.action_export_boq)
        self.menuDesite.addAction(self.action_mapping_Script)
        self.menuPredefined_Psets.addAction(self.action_show_list)
        self.menuShow_Graphs.addAction(self.action_show_graphs)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_file_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.action_file_Save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.action_file_Save_As.setText(QCoreApplication.translate("MainWindow", u"Save As ...", None))
        self.action_file_Open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.action_desite_Settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.action_desite_export.setText(QCoreApplication.translate("MainWindow", u"Export Modelcheck", None))
        self.action_show_list.setText(QCoreApplication.translate("MainWindow", u"Show List", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.action_export_bs.setText(QCoreApplication.translate("MainWindow", u"Export BS", None))
        self.action_export_bookmarks.setText(QCoreApplication.translate("MainWindow", u"Export Bookmarks", None))
        self.action_show_graphs.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.action_export_boq.setText(QCoreApplication.translate("MainWindow", u"Export  for BoQ", None))
        self.action_mapping_options.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.action_mapping.setText(QCoreApplication.translate("MainWindow", u"Mapping", None))
        self.action_shared_parameter.setText(QCoreApplication.translate("MainWindow", u"Shared Parameters", None))
        self.action_ifc_mapping.setText(QCoreApplication.translate("MainWindow", u"IFC Mapping", None))
        self.action_mapping_Script.setText(QCoreApplication.translate("MainWindow", u"Mapping Script", None))
        self.action_abbreviation_json.setText(QCoreApplication.translate("MainWindow", u"Abbreviation JSON", None))
        self.action_allplan.setText(QCoreApplication.translate("MainWindow", u"Allplan", None))
        self.action_card1.setText(QCoreApplication.translate("MainWindow", u"CARD1", None))
        self.action_vestra.setText(QCoreApplication.translate("MainWindow", u"Verstra", None))
        self.action_excel.setText(QCoreApplication.translate("MainWindow", u"Excel", None))
        self.label_Ident.setText(QCoreApplication.translate("MainWindow", u"Ident", None))
        self.lineEdit_ident_attribute.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Attribute", None))
        self.lineEdit_ident_pSet.setPlaceholderText(QCoreApplication.translate("MainWindow", u"PropertySet", None))
        self.label_object_name.setText(QCoreApplication.translate("MainWindow", u"Object", None))
        self.lineEdit_ident_value.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Value", None))
        self.lineEdit_object_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.button_objects_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        ___qtreewidgetitem = self.tree_object.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Identifier", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Objects", None));
        ___qtablewidgetitem = self.table_pset.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"PropertySet", None));
        ___qtablewidgetitem1 = self.table_pset.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"InheritedBy", None));
        ___qtablewidgetitem2 = self.table_pset.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Test", None));

        __sortingEnabled = self.table_pset.isSortingEnabled()
        self.table_pset.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.table_pset.item(0, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"BestandsdatenqVerkehrsanlagen", None));
        ___qtablewidgetitem4 = self.table_pset.item(0, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Verkehrsanlagen", None));
        self.table_pset.setSortingEnabled(__sortingEnabled)

        ___qtablewidgetitem5 = self.table_attribute.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem6 = self.table_attribute.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Data Format", None));
        ___qtablewidgetitem7 = self.table_attribute.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Format", None));
        ___qtablewidgetitem8 = self.table_attribute.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.label_pSet_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.button_Pset_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_property_set), QCoreApplication.translate("MainWindow", u"PropertySet", None))
        self.label_script_title.setText(QCoreApplication.translate("MainWindow", u"Scripts", None))

        __sortingEnabled1 = self.listWidget_scripts.isSortingEnabled()
        self.listWidget_scripts.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget_scripts.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem1 = self.listWidget_scripts.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem2 = self.listWidget_scripts.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem3 = self.listWidget_scripts.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        ___qlistwidgetitem4 = self.listWidget_scripts.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Item", None));
        self.listWidget_scripts.setSortingEnabled(__sortingEnabled1)

        self.pushButton_add_script.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_delete_script.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_import_script.setText(QCoreApplication.translate("MainWindow", u"DL", None))
        self.pushButton_burger.setText(QCoreApplication.translate("MainWindow", u"B", None))
        self.pushButton_left.setText(QCoreApplication.translate("MainWindow", u"<-", None))
        self.pushButton_right.setText(QCoreApplication.translate("MainWindow", u"->", None))
        self.label_script_name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_code), QCoreApplication.translate("MainWindow", u"Code", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuDesite.setTitle(QCoreApplication.translate("MainWindow", u"Desite", None))
        self.menuPredefined_Psets.setTitle(QCoreApplication.translate("MainWindow", u"Predefined Psets", None))
        self.menuShow_Graphs.setTitle(QCoreApplication.translate("MainWindow", u"Aggregation", None))
    # retranslateUi

