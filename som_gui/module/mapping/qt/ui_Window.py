# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Window.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QSplitter, QStatusBar,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from som_gui.module.mapping.ui import (ObjectTreeWidget, PropertySetTreeWidget)

class Ui_Mapping(object):
    def setupUi(self, Mapping):
        if not Mapping.objectName():
            Mapping.setObjectName(u"Mapping")
        Mapping.resize(1194, 549)
        self.action_ifc = QAction(Mapping)
        self.action_ifc.setObjectName(u"action_ifc")
        self.action_shared_parameters = QAction(Mapping)
        self.action_shared_parameters.setObjectName(u"action_shared_parameters")
        self.centralwidget = QWidget(Mapping)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setFrameShape(QFrame.Shape.Box)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.object_tree = ObjectTreeWidget(self.splitter)
        self.object_tree.setObjectName(u"object_tree")
        self.object_tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.object_tree.setSortingEnabled(True)
        self.splitter.addWidget(self.object_tree)
        self.gridLayoutWidget = QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.right_layout = QGridLayout(self.gridLayoutWidget)
        self.right_layout.setObjectName(u"right_layout")
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_object_name = QLabel(self.gridLayoutWidget)
        self.label_object_name.setObjectName(u"label_object_name")
        self.label_object_name.setEnabled(True)

        self.verticalLayout.addWidget(self.label_object_name)

        self.pset_tree = PropertySetTreeWidget(self.gridLayoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"PropertySet/Attribute");
        self.pset_tree.setHeaderItem(__qtreewidgetitem)
        self.pset_tree.setObjectName(u"pset_tree")
        self.pset_tree.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.pset_tree)


        self.right_layout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.splitter.addWidget(self.gridLayoutWidget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        Mapping.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Mapping)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1194, 33))
        self.menu_revit = QMenu(self.menubar)
        self.menu_revit.setObjectName(u"menu_revit")
        Mapping.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Mapping)
        self.statusbar.setObjectName(u"statusbar")
        Mapping.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_revit.menuAction())
        self.menu_revit.addAction(self.action_ifc)
        self.menu_revit.addAction(self.action_shared_parameters)

        self.retranslateUi(Mapping)

        QMetaObject.connectSlotsByName(Mapping)
    # setupUi

    def retranslateUi(self, Mapping):
        Mapping.setWindowTitle(QCoreApplication.translate("Mapping", u"MainWindow", None))
        self.action_ifc.setText(QCoreApplication.translate("Mapping", u"Export IFC-Mapping", None))
        self.action_shared_parameters.setText(QCoreApplication.translate("Mapping", u"Export Shared Parameters", None))
        ___qtreewidgetitem = self.object_tree.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Mapping", u"Ifc Mapping", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Mapping", u"Object", None));
        self.label_object_name.setText("")
        ___qtreewidgetitem1 = self.pset_tree.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Mapping", u"Revit Mapping", None));
        self.menu_revit.setTitle(QCoreApplication.translate("Mapping", u"Revit", None))
    # retranslateUi

