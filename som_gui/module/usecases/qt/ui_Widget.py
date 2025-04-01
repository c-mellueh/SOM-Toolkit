# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

from som_gui.module.usecases.ui import (ClassView, ProjectView, PropertyView)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(830, 583)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.vertical_splitter = QSplitter(Form)
        self.vertical_splitter.setObjectName(u"vertical_splitter")
        self.vertical_splitter.setOrientation(Qt.Orientation.Vertical)
        self.project_tableView = ProjectView(self.vertical_splitter)
        self.project_tableView.setObjectName(u"project_tableView")
        self.vertical_splitter.addWidget(self.project_tableView)
        self.horizontal_splitter = QSplitter(self.vertical_splitter)
        self.horizontal_splitter.setObjectName(u"horizontal_splitter")
        self.horizontal_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.class_splitter = QSplitter(self.horizontal_splitter)
        self.class_splitter.setObjectName(u"class_splitter")
        self.class_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.class_treeView_fixed = ClassView(self.class_splitter)
        self.class_treeView_fixed.setObjectName(u"class_treeView_fixed")
        self.class_splitter.addWidget(self.class_treeView_fixed)
        self.class_treeView_extendable = ClassView(self.class_splitter)
        self.class_treeView_extendable.setObjectName(u"class_treeView_extendable")
        self.class_splitter.addWidget(self.class_treeView_extendable)
        self.horizontal_splitter.addWidget(self.class_splitter)
        self.property_splitter = QSplitter(self.horizontal_splitter)
        self.property_splitter.setObjectName(u"property_splitter")
        self.property_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.property_table_view_fixed = PropertyView(self.property_splitter)
        self.property_table_view_fixed.setObjectName(u"property_table_view_fixed")
        self.property_splitter.addWidget(self.property_table_view_fixed)
        self.property_table_view_extendable = PropertyView(self.property_splitter)
        self.property_table_view_extendable.setObjectName(u"property_table_view_extendable")
        self.property_splitter.addWidget(self.property_table_view_extendable)
        self.horizontal_splitter.addWidget(self.property_splitter)
        self.vertical_splitter.addWidget(self.horizontal_splitter)

        self.verticalLayout.addWidget(self.vertical_splitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

