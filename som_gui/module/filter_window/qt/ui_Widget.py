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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QSizePolicy,
    QSplitter, QVBoxLayout, QWidget)

from som_gui.module.filter_window.ui import ProjectView

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1456, 892)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.vertical_splitter = QSplitter(Form)
        self.vertical_splitter.setObjectName(u"vertical_splitter")
        self.vertical_splitter.setOrientation(Qt.Orientation.Vertical)
        self.project_table = ProjectView(self.vertical_splitter)
        self.project_table.setObjectName(u"project_table")
        self.project_table.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.project_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.vertical_splitter.addWidget(self.project_table)
        self.splitter_3 = QSplitter(self.vertical_splitter)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.class_splitter = QSplitter(self.splitter_3)
        self.class_splitter.setObjectName(u"class_splitter")
        self.class_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter_3.addWidget(self.class_splitter)
        self.property_splitter = QSplitter(self.splitter_3)
        self.property_splitter.setObjectName(u"property_splitter")
        self.property_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter_3.addWidget(self.property_splitter)
        self.vertical_splitter.addWidget(self.splitter_3)

        self.verticalLayout.addWidget(self.vertical_splitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

