# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MappingWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1159, 517)
        self.action_ifc = QAction(Form)
        self.action_ifc.setObjectName(u"action_ifc")
        self.action_shared_parameters = QAction(Form)
        self.action_shared_parameters.setObjectName(u"action_shared_parameters")
        self.action_export_attribute_excel = QAction(Form)
        self.action_export_attribute_excel.setObjectName(u"action_export_attribute_excel")
        self.action_desite_mapping = QAction(Form)
        self.action_desite_mapping.setObjectName(u"action_desite_mapping")
        self.action_create_vestra_mapping = QAction(Form)
        self.action_create_vestra_mapping.setObjectName(u"action_create_vestra_mapping")
        self.action_desite_abbreviation = QAction(Form)
        self.action_desite_abbreviation.setObjectName(u"action_desite_abbreviation")
        self.action_allplan = QAction(Form)
        self.action_allplan.setObjectName(u"action_allplan")
        self.action_vestra = QAction(Form)
        self.action_vestra.setObjectName(u"action_vestra")
        self.action_card1 = QAction(Form)
        self.action_card1.setObjectName(u"action_card1")
        self.action_excel = QAction(Form)
        self.action_excel.setObjectName(u"action_excel")
        self.centralwidget = QWidget(Form)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setFrameShape(QFrame.Box)
        self.splitter.setOrientation(Qt.Horizontal)
        self.object_tree = ObjectTreeWidget(self.splitter)
        self.object_tree.setObjectName(u"object_tree")
        self.object_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
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
        self.pset_tree.setObjectName(u"pset_tree")
        self.pset_tree.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.pset_tree)

        self.right_layout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.splitter.addWidget(self.gridLayoutWidget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        Form.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Form)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1159, 22))
        self.menu_revit = QMenu(self.menubar)
        self.menu_revit.setObjectName(u"menu_revit")
        Form.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Form)
        self.statusbar.setObjectName(u"statusbar")
        Form.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_revit.menuAction())
        self.menu_revit.addAction(self.action_ifc)
        self.menu_revit.addAction(self.action_shared_parameters)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"MainWindow", None))
        self.action_ifc.setText(QCoreApplication.translate("Form", u"Export IFC-Mapping", None))
        self.action_shared_parameters.setText(QCoreApplication.translate("Form", u"Export Shared Parameters", None))
        self.action_export_attribute_excel.setText(QCoreApplication.translate("Form", u"Export Attribute Excel", None))
        self.action_desite_mapping.setText(QCoreApplication.translate("Form", u"create mapping Script", None))
        self.action_create_vestra_mapping.setText(QCoreApplication.translate("Form", u"create .amrx", None))
        self.action_desite_abbreviation.setText(QCoreApplication.translate("Form", u"create abbreviation JSON", None))
        self.action_allplan.setText(QCoreApplication.translate("Form", u"Allplan", None))
        self.action_vestra.setText(QCoreApplication.translate("Form", u"Vestra", None))
        self.action_card1.setText(QCoreApplication.translate("Form", u"CARD1", None))
        self.action_excel.setText(QCoreApplication.translate("Form", u"Excel", None))
        self.label_object_name.setText("")
        self.menu_revit.setTitle(QCoreApplication.translate("Form", u"Revit", None))
    # retranslateUi
