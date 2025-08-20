# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from som_gui.module.mapping.ui import ClassTreeWidget, PropertySetTreeWidget


class Ui_Mapping(object):
    def setupUi(self, Mapping):
        if not Mapping.objectName():
            Mapping.setObjectName("Mapping")
        Mapping.resize(1194, 549)
        self.action_ifc = QAction(Mapping)
        self.action_ifc.setObjectName("action_ifc")
        self.action_shared_parameters = QAction(Mapping)
        self.action_shared_parameters.setObjectName("action_shared_parameters")
        self.centralwidget = QWidget(Mapping)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setFrameShape(QFrame.Shape.Box)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.class_tree = ClassTreeWidget(self.splitter)
        self.class_tree.setObjectName("class_tree")
        self.class_tree.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.class_tree.setSortingEnabled(True)
        self.splitter.addWidget(self.class_tree)
        self.gridLayoutWidget = QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.right_layout = QGridLayout(self.gridLayoutWidget)
        self.right_layout.setObjectName("right_layout")
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_class_name = QLabel(self.gridLayoutWidget)
        self.label_class_name.setObjectName("label_class_name")
        self.label_class_name.setEnabled(True)

        self.verticalLayout.addWidget(self.label_class_name)

        self.pset_tree = PropertySetTreeWidget(self.gridLayoutWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, "PropertySet/Property")
        self.pset_tree.setHeaderItem(__qtreewidgetitem)
        self.pset_tree.setObjectName("pset_tree")
        self.pset_tree.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.pset_tree)

        self.right_layout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.splitter.addWidget(self.gridLayoutWidget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        Mapping.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Mapping)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1194, 33))
        self.menu_revit = QMenu(self.menubar)
        self.menu_revit.setObjectName("menu_revit")
        Mapping.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Mapping)
        self.statusbar.setObjectName("statusbar")
        Mapping.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_revit.menuAction())
        self.menu_revit.addAction(self.action_ifc)
        self.menu_revit.addAction(self.action_shared_parameters)

        self.retranslateUi(Mapping)

        QMetaObject.connectSlotsByName(Mapping)

    # setupUi

    def retranslateUi(self, Mapping):
        Mapping.setWindowTitle(
            QCoreApplication.translate("Mapping", "MainWindow", None)
        )
        self.action_ifc.setText(
            QCoreApplication.translate("Mapping", "Export IFC-Mapping", None)
        )
        self.action_shared_parameters.setText(
            QCoreApplication.translate("Mapping", "Export Shared Parameters", None)
        )
        ___qtreewidgetitem = self.class_tree.headerItem()
        ___qtreewidgetitem.setText(
            1, QCoreApplication.translate("Mapping", "Ifc Mapping", None)
        )
        ___qtreewidgetitem.setText(
            0, QCoreApplication.translate("Mapping", "Class", None)
        )
        self.label_class_name.setText("")
        ___qtreewidgetitem1 = self.pset_tree.headerItem()
        ___qtreewidgetitem1.setText(
            1, QCoreApplication.translate("Mapping", "Revit Mapping", None)
        )
        self.menu_revit.setTitle(QCoreApplication.translate("Mapping", "Revit", None))

    # retranslateUi
