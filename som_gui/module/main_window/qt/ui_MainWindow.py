# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QHeaderView, QLabel, QMainWindow, QMenu,
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
        MainWindow.resize(1512, 740)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.actiondqwd = QAction(MainWindow)
        self.actiondqwd.setObjectName(u"actiondqwd")
        self.verticalLayout_main = QWidget(MainWindow)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout = QVBoxLayout(self.verticalLayout_main)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.verticalLayout_main)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_objects = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_objects.setObjectName(u"verticalLayout_objects")
        self.verticalLayout_objects.setContentsMargins(0, 0, 5, 0)
        self.gridLayout_objects = QGridLayout()
        self.gridLayout_objects.setObjectName(u"gridLayout_objects")
        self.label_object = QLabel(self.layoutWidget)
        self.label_object.setObjectName(u"label_object")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_object.sizePolicy().hasHeightForWidth())
        self.label_object.setSizePolicy(sizePolicy)
        self.label_object.setMinimumSize(QSize(30, 0))
        self.label_object.setLineWidth(1)

        self.gridLayout_objects.addWidget(self.label_object, 0, 1, 1, 1)

        self.button_objects_add = QPushButton(self.layoutWidget)
        self.button_objects_add.setObjectName(u"button_objects_add")
        self.button_objects_add.setAutoDefault(True)

        self.gridLayout_objects.addWidget(self.button_objects_add, 0, 3, 1, 1)

        self.button_search = QPushButton(self.layoutWidget)
        self.button_search.setObjectName(u"button_search")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy1)
        self.button_search.setMinimumSize(QSize(24, 0))
        self.button_search.setMaximumSize(QSize(24, 24))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.button_search.setIcon(icon)
        self.button_search.setIconSize(QSize(16, 16))

        self.gridLayout_objects.addWidget(self.button_search, 0, 0, 1, 1)

        self.label_object_name = QLabel(self.layoutWidget)
        self.label_object_name.setObjectName(u"label_object_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_object_name.sizePolicy().hasHeightForWidth())
        self.label_object_name.setSizePolicy(sizePolicy2)

        self.gridLayout_objects.addWidget(self.label_object_name, 0, 2, 1, 1)


        self.verticalLayout_objects.addLayout(self.gridLayout_objects)

        self.tree_object = ObjectTreeWidget(self.layoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_object.setHeaderItem(__qtreewidgetitem)
        self.tree_object.setObjectName(u"tree_object")
        self.tree_object.setEnabled(True)
        self.tree_object.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_object.setDragEnabled(True)
        self.tree_object.setDragDropOverwriteMode(False)
        self.tree_object.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.tree_object.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.tree_object.setAlternatingRowColors(False)
        self.tree_object.setSortingEnabled(True)
        self.tree_object.setExpandsOnDoubleClick(False)
        self.tree_object.header().setProperty(u"showSortIndicator", True)

        self.verticalLayout_objects.addWidget(self.tree_object)

        self.splitter.addWidget(self.layoutWidget)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vertical_layout_pset = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_pset.setObjectName(u"vertical_layout_pset")
        self.vertical_layout_pset.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_pSet_button = QHBoxLayout()
        self.horizontalLayout_pSet_button.setObjectName(u"horizontalLayout_pSet_button")
        self.label_pset = QLabel(self.verticalLayoutWidget)
        self.label_pset.setObjectName(u"label_pset")
        self.label_pset.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_pSet_button.addWidget(self.label_pset)

        self.label_pset_name = QLabel(self.verticalLayoutWidget)
        self.label_pset_name.setObjectName(u"label_pset_name")
        sizePolicy2.setHeightForWidth(self.label_pset_name.sizePolicy().hasHeightForWidth())
        self.label_pset_name.setSizePolicy(sizePolicy2)

        self.horizontalLayout_pSet_button.addWidget(self.label_pset_name)

        self.button_Pset_add = QPushButton(self.verticalLayoutWidget)
        self.button_Pset_add.setObjectName(u"button_Pset_add")
        sizePolicy.setHeightForWidth(self.button_Pset_add.sizePolicy().hasHeightForWidth())
        self.button_Pset_add.setSizePolicy(sizePolicy)
        self.button_Pset_add.setAutoDefault(True)

        self.horizontalLayout_pSet_button.addWidget(self.button_Pset_add)


        self.vertical_layout_pset.addLayout(self.horizontalLayout_pSet_button)

        self.table_pset = PsetTableWidget(self.verticalLayoutWidget)
        if (self.table_pset.columnCount() < 3):
            self.table_pset.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_pset.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_pset.setObjectName(u"table_pset")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.table_pset.sizePolicy().hasHeightForWidth())
        self.table_pset.setSizePolicy(sizePolicy3)
        self.table_pset.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table_pset.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_pset.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_pset.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_pset.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_pset.horizontalHeader().setStretchLastSection(True)
        self.table_pset.verticalHeader().setVisible(False)
        self.table_pset.verticalHeader().setCascadingSectionResizes(False)

        self.vertical_layout_pset.addWidget(self.table_pset)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.table_attribute = AttributeTable(self.splitter)
        self.table_attribute.setObjectName(u"table_attribute")
        self.table_attribute.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_attribute.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_attribute.setSortingEnabled(True)
        self.splitter.addWidget(self.table_attribute)
        self.table_attribute.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.verticalLayout_main)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1512, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuExport = QMenu(self.menuFile)
        self.menuExport.setObjectName(u"menuExport")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuDesite = QMenu(self.menubar)
        self.menuDesite.setObjectName(u"menuDesite")
        self.menuModels = QMenu(self.menubar)
        self.menuModels.setObjectName(u"menuModels")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.button_objects_add, self.tree_object)
        QWidget.setTabOrder(self.tree_object, self.button_search)
        QWidget.setTabOrder(self.button_search, self.button_Pset_add)
        QWidget.setTabOrder(self.button_Pset_add, self.table_attribute)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuModels.menuAction())
        self.menubar.addAction(self.menuDesite.menuAction())
        self.menuFile.addAction(self.menuExport.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SOMToolkit", None))
        self.actiondqwd.setText(QCoreApplication.translate("MainWindow", u"dqwd", None))
        self.label_object.setText(QCoreApplication.translate("MainWindow", u"Class:", None))
        self.button_objects_add.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.button_search.setText("")
        self.label_object_name.setText("")
        self.label_pset.setText(QCoreApplication.translate("MainWindow", u"PropertySet:", None))
        self.label_pset_name.setText("")
        self.button_Pset_add.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        ___qtablewidgetitem = self.table_pset.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"PropertySet", None));
        ___qtablewidgetitem1 = self.table_pset.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Inherited By", None));
        ___qtablewidgetitem2 = self.table_pset.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Optional", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuDesite.setTitle(QCoreApplication.translate("MainWindow", u"Desite", None))
        self.menuModels.setTitle(QCoreApplication.translate("MainWindow", u"Models", None))
    # retranslateUi

