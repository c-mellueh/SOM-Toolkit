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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QSizePolicy,
    QSplitter, QVBoxLayout, QWidget)

from som_gui.module.usecases.ui import (ClassView, ProjectView, PropertyView)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1147, 697)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter_3 = QSplitter(Form)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Vertical)
        self.project_tableView = ProjectView(self.splitter_3)
        self.project_tableView.setObjectName(u"project_tableView")
        self.splitter_3.addWidget(self.project_tableView)
        self.project_tableView.horizontalHeader().setStretchLastSection(True)
        self.project_tableView.verticalHeader().setStretchLastSection(True)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.class_splitter = QSplitter(self.splitter_2)
        self.class_splitter.setObjectName(u"class_splitter")
        self.class_splitter.setLineWidth(0)
        self.class_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.class_splitter.setHandleWidth(0)
        self.class_treeView_fixed = ClassView(self.class_splitter)
        self.class_treeView_fixed.setObjectName(u"class_treeView_fixed")
        self.class_treeView_fixed.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.class_splitter.addWidget(self.class_treeView_fixed)
        self.class_treeView_extendable = ClassView(self.class_splitter)
        self.class_treeView_extendable.setObjectName(u"class_treeView_extendable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.class_treeView_extendable.sizePolicy().hasHeightForWidth())
        self.class_treeView_extendable.setSizePolicy(sizePolicy)
        self.class_splitter.addWidget(self.class_treeView_extendable)
        self.splitter_2.addWidget(self.class_splitter)
        self.verticalLayoutWidget = QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.property_label = QLabel(self.verticalLayoutWidget)
        self.property_label.setObjectName(u"property_label")

        self.verticalLayout.addWidget(self.property_label)

        self.splitter = QSplitter(self.verticalLayoutWidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.property_TableView_fixed = PropertyView(self.splitter)
        self.property_TableView_fixed.setObjectName(u"property_TableView_fixed")
        self.splitter.addWidget(self.property_TableView_fixed)
        self.property_TableView_extendable = PropertyView(self.splitter)
        self.property_TableView_extendable.setObjectName(u"property_TableView_extendable")
        sizePolicy.setHeightForWidth(self.property_TableView_extendable.sizePolicy().hasHeightForWidth())
        self.property_TableView_extendable.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.property_TableView_extendable)

        self.verticalLayout.addWidget(self.splitter)

        self.splitter_2.addWidget(self.verticalLayoutWidget)
        self.splitter_3.addWidget(self.splitter_2)

        self.verticalLayout_2.addWidget(self.splitter_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.property_label.setText("")
    # retranslateUi

