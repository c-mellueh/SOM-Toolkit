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
        Form.resize(1445, 1004)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter_2 = QSplitter(Form)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.project_tableView = ProjectView(self.splitter_2)
        self.project_tableView.setObjectName(u"project_tableView")
        self.splitter_2.addWidget(self.project_tableView)
        self.project_tableView.horizontalHeader().setStretchLastSection(True)
        self.project_tableView.verticalHeader().setStretchLastSection(True)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.class_splitter = QSplitter(self.splitter)
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
        self.class_splitter.addWidget(self.class_treeView_extendable)
        self.splitter.addWidget(self.class_splitter)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.property_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.property_layout.setObjectName(u"property_layout")
        self.property_layout.setContentsMargins(0, 0, 0, 0)
        self.property_label = QLabel(self.verticalLayoutWidget)
        self.property_label.setObjectName(u"property_label")

        self.property_layout.addWidget(self.property_label)

        self.property_table_view = PropertyView(self.verticalLayoutWidget)
        self.property_table_view.setObjectName(u"property_table_view")

        self.property_layout.addWidget(self.property_table_view)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.splitter_2.addWidget(self.splitter)

        self.verticalLayout.addWidget(self.splitter_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.property_label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

