# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSplitter, QStatusBar, QTableWidgetItem, QTreeWidgetItem,
    QVBoxLayout, QWidget)

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
        self.line_edit_object_name.setEchoMode(QLineEdit.EchoMode.Normal)
        self.line_edit_object_name.setClearButtonEnabled(False)

        self.horizontalLayout_object_button.addWidget(self.line_edit_object_name)


        self.gridLayout_objects.addLayout(self.horizontalLayout_object_button, 0, 2, 1, 3)

        self.lineEdit_ident_pSet = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_pSet.setObjectName(u"lineEdit_ident_pSet")
        sizePolicy.setHeightForWidth(self.lineEdit_ident_pSet.sizePolicy().hasHeightForWidth())
        self.lineEdit_ident_pSet.setSizePolicy(sizePolicy)
        self.lineEdit_ident_pSet.setFrame(True)
        self.lineEdit_ident_pSet.setEchoMode(QLineEdit.EchoMode.Normal)

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
        self.lineEdit_ident_attribute.setEchoMode(QLineEdit.EchoMode.Normal)
        self.lineEdit_ident_attribute.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)

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
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.button_search.setIcon(icon)
        self.button_search.setIconSize(QSize(16, 16))

        self.gridLayout_objects.addWidget(self.button_search, 0, 0, 1, 1)

        self.lineEdit_ident_value = QLineEdit(self.layoutWidget)
        self.lineEdit_ident_value.setObjectName(u"lineEdit_ident_value")
        self.lineEdit_ident_value.setFrame(True)
        self.lineEdit_ident_value.setEchoMode(QLineEdit.EchoMode.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_value, 1, 4, 1, 2)

        self.label_Ident = QLabel(self.layoutWidget)
        self.label_Ident.setObjectName(u"label_Ident")

        self.gridLayout_objects.addWidget(self.label_Ident, 1, 1, 1, 1)


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
        self.tree_object.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree_object.setSortingEnabled(True)
        self.tree_object.setExpandsOnDoubleClick(False)
        self.tree_object.header().setProperty(u"showSortIndicator", True)

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
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
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
        self.table_pset.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table_pset.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_pset.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_pset.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_pset.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_pset.setSortingEnabled(True)
        self.splitter_2.addWidget(self.table_pset)
        self.table_pset.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.table_pset.horizontalHeader().setStretchLastSection(True)
        self.table_pset.verticalHeader().setVisible(False)
        self.table_pset.verticalHeader().setCascadingSectionResizes(False)
        self.table_attribute = AttributeTable(self.splitter_2)
        self.table_attribute.setObjectName(u"table_attribute")
        self.table_attribute.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_attribute.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_attribute.setSortingEnabled(True)
        self.splitter_2.addWidget(self.table_attribute)
        self.table_attribute.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.splitter_2, 3, 0, 1, 2)

        self.splitter.addWidget(self.box_layout_pset)

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
        self.button_objects_add.setText(QCoreApplication.translate("MainWindow", u"Create", None))
#if QT_CONFIG(tooltip)
        self.line_edit_object_name.setToolTip(QCoreApplication.translate("MainWindow", u"Name of Object", None))
#endif // QT_CONFIG(tooltip)
        self.line_edit_object_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Name", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_ident_pSet.setToolTip(QCoreApplication.translate("MainWindow", u"Name of PropertySet which owns Identifier Attribute", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_ident_pSet.setPlaceholderText(QCoreApplication.translate("MainWindow", u"PropertySet", None))
        self.label_object_name.setText(QCoreApplication.translate("MainWindow", u"Object", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_ident_attribute.setToolTip(QCoreApplication.translate("MainWindow", u"Name of Attribute which owns the identifier value", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_ident_attribute.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Attribute", None))
        self.button_search.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_ident_value.setToolTip(QCoreApplication.translate("MainWindow", u"Needs to be unique!", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_ident_value.setText("")
        self.lineEdit_ident_value.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Value", None))
#if QT_CONFIG(tooltip)
        self.label_Ident.setToolTip(QCoreApplication.translate("MainWindow", u"The Identifier defines which Object is selected it needs to be unique!", None))
#endif // QT_CONFIG(tooltip)
        self.label_Ident.setText(QCoreApplication.translate("MainWindow", u"Identifier", None))
        self.label_pSet_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_pSet_name.setToolTip("")
#endif // QT_CONFIG(tooltip)
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

