# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
        MainWindow.resize(1315, 503)
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
        self.button_objects_add = QPushButton(self.layoutWidget)
        self.button_objects_add.setObjectName(u"button_objects_add")
        self.button_objects_add.setAutoDefault(True)

        self.gridLayout_objects.addWidget(self.button_objects_add, 0, 5, 1, 1)

        self.horizontalLayout_object_button = QHBoxLayout()
        self.horizontalLayout_object_button.setObjectName(u"horizontalLayout_object_button")
        self.line_edit_object_name = QLineEdit(self.layoutWidget)
        self.line_edit_object_name.setObjectName(u"line_edit_object_name")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_object_name.sizePolicy().hasHeightForWidth())
        self.line_edit_object_name.setSizePolicy(sizePolicy)
        self.line_edit_object_name.setFrame(True)
        self.line_edit_object_name.setEchoMode(QLineEdit.Normal)
        self.line_edit_object_name.setClearButtonEnabled(False)

        self.horizontalLayout_object_button.addWidget(self.line_edit_object_name)

        self.line_edit_abbreviation = QLineEdit(self.layoutWidget)
        self.line_edit_abbreviation.setObjectName(u"line_edit_abbreviation")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_abbreviation.sizePolicy().hasHeightForWidth())
        self.line_edit_abbreviation.setSizePolicy(sizePolicy1)

        self.horizontalLayout_object_button.addWidget(self.line_edit_abbreviation)


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
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_object_name.sizePolicy().hasHeightForWidth())
        self.label_object_name.setSizePolicy(sizePolicy2)
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
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy3)
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
        sizePolicy2.setHeightForWidth(self.button_Pset_add.sizePolicy().hasHeightForWidth())
        self.button_Pset_add.setSizePolicy(sizePolicy2)
        self.button_Pset_add.setAutoDefault(True)

        self.horizontalLayout_pSet_button.addWidget(self.button_Pset_add)


        self.gridLayout.addLayout(self.horizontalLayout_pSet_button, 2, 0, 1, 2)

        self.splitter_2 = QSplitter(self.tab_property_set)
        self.splitter_2.setObjectName(u"splitter_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy4)
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.table_pset = QTableWidget(self.splitter_2)
        if (self.table_pset.columnCount() < 3):
            self.table_pset.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_pset.setObjectName(u"table_pset")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.table_pset.sizePolicy().hasHeightForWidth())
        self.table_pset.setSizePolicy(sizePolicy5)
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
        self.table_attribute = QTableWidget(self.splitter_2)
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
        self.table_attribute.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.splitter_2.addWidget(self.table_attribute)
        self.table_attribute.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.splitter_2, 3, 0, 1, 2)

        self.tabWidget.addTab(self.tab_property_set, "")
        self.tab_code = QWidget()
        self.tab_code.setObjectName(u"tab_code")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_code)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widget_vertical_stack = QWidget(self.tab_code)
        self.widget_vertical_stack.setObjectName(u"widget_vertical_stack")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.widget_vertical_stack.sizePolicy().hasHeightForWidth())
        self.widget_vertical_stack.setSizePolicy(sizePolicy6)
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
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.listWidget_scripts.sizePolicy().hasHeightForWidth())
        self.listWidget_scripts.setSizePolicy(sizePolicy7)
        self.listWidget_scripts.setMaximumSize(QSize(161, 16777215))
        self.listWidget_scripts.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)

        self.verticalLayout_4.addWidget(self.listWidget_scripts)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_add_script = QPushButton(self.widget_vertical_stack)
        self.pushButton_add_script.setObjectName(u"pushButton_add_script")
        sizePolicy1.setHeightForWidth(self.pushButton_add_script.sizePolicy().hasHeightForWidth())
        self.pushButton_add_script.setSizePolicy(sizePolicy1)
        self.pushButton_add_script.setMinimumSize(QSize(25, 25))
        self.pushButton_add_script.setMaximumSize(QSize(21, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButton_add_script)

        self.pushButton_delete_script = QPushButton(self.widget_vertical_stack)
        self.pushButton_delete_script.setObjectName(u"pushButton_delete_script")
        sizePolicy1.setHeightForWidth(self.pushButton_delete_script.sizePolicy().hasHeightForWidth())
        self.pushButton_delete_script.setSizePolicy(sizePolicy1)
        self.pushButton_delete_script.setMinimumSize(QSize(25, 25))
        self.pushButton_delete_script.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.pushButton_delete_script)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_import_script = QPushButton(self.widget_vertical_stack)
        self.pushButton_import_script.setObjectName(u"pushButton_import_script")
        sizePolicy1.setHeightForWidth(self.pushButton_import_script.sizePolicy().hasHeightForWidth())
        self.pushButton_import_script.setSizePolicy(sizePolicy1)
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
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(2)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.label_script_name.sizePolicy().hasHeightForWidth())
        self.label_script_name.setSizePolicy(sizePolicy8)

        self.horizontalLayout.addWidget(self.label_script_name)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.code_edit = QTextEdit(self.tab_code)
        self.code_edit.setObjectName(u"code_edit")
        sizePolicy9 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy9.setHorizontalStretch(2)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.code_edit.sizePolicy().hasHeightForWidth())
        self.code_edit.setSizePolicy(sizePolicy9)

        self.verticalLayout_2.addWidget(self.code_edit)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.tab_code, "")
        self.splitter.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.verticalLayout_main)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1315, 22))
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
        self.menu_ifc = QMenu(self.menubar)
        self.menu_ifc.setObjectName(u"menu_ifc")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.lineEdit_ident_pSet, self.lineEdit_ident_attribute)
        QWidget.setTabOrder(self.lineEdit_ident_attribute, self.lineEdit_ident_value)
        QWidget.setTabOrder(self.lineEdit_ident_value, self.tree_object)
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
        self.menubar.addAction(self.menu_ifc.menuAction())
        self.menuFile.addAction(self.action_file_new)
        self.menuFile.addAction(self.action_file_Open)
        self.menuFile.addAction(self.action_import_excel)
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
        self.menuDesite.addAction(self.action_export_bookmarks)
        self.menuDesite.addAction(self.action_mapping_script)
        self.menuPredefined_Psets.addAction(self.action_show_list)
        self.menuShow_Graphs.addAction(self.action_show_graphs)
        self.menu_ifc.addAction(self.action_modelcheck)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


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
        self.button_objects_add.setText(QCoreApplication.translate("MainWindow", u"Erstellen", None))
#if QT_CONFIG(tooltip)
        self.line_edit_object_name.setToolTip(QCoreApplication.translate("MainWindow", u"Name der Objektvorgabe", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit_object_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Name", None))
#if QT_CONFIG(tooltip)
        self.line_edit_abbreviation.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>die Abk\u00fcrzung ist relevant f\u00fcr die Bauwerksstruktur.<br/>Sie sollte zwischen 1-10 Zeichen Lang sein und darf nur einmal vorkommen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit_abbreviation.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Abk\u00fcrzung", None))
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
        ___qtreewidgetitem = self.tree_object.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Optional", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Abk\u00fcrzung", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Identifier", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Objektvorgaben", None));
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_property_set), QCoreApplication.translate("MainWindow", u"PropertySet", None))
        self.label_script_title.setText(QCoreApplication.translate("MainWindow", u"Scripts", None))

        __sortingEnabled = self.listWidget_scripts.isSortingEnabled()
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
        self.listWidget_scripts.setSortingEnabled(__sortingEnabled)

        self.pushButton_add_script.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_delete_script.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_import_script.setText(QCoreApplication.translate("MainWindow", u"DL", None))
        self.pushButton_burger.setText(QCoreApplication.translate("MainWindow", u"B", None))
        self.pushButton_left.setText(QCoreApplication.translate("MainWindow", u"<-", None))
        self.pushButton_right.setText(QCoreApplication.translate("MainWindow", u"->", None))
        self.label_script_name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_code), QCoreApplication.translate("MainWindow", u"Code", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
#if QT_CONFIG(tooltip)
        self.menuDesite.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.menuDesite.setTitle(QCoreApplication.translate("MainWindow", u"Desite", None))
        self.menuPredefined_Psets.setTitle(QCoreApplication.translate("MainWindow", u"Vordefinierte Psets", None))
        self.menuShow_Graphs.setTitle(QCoreApplication.translate("MainWindow", u"Bauwerksstruktur", None))
        self.menu_ifc.setTitle(QCoreApplication.translate("MainWindow", u"IFC", None))
    # retranslateUi

