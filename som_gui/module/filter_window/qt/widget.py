# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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

from som_gui.module.filter_window.ui import (ObjectTreeView, ProjectView, PsetTreeView)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(854, 581)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter_2 = QSplitter(Form)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.project_table = ProjectView(self.splitter_2)
        self.project_table.setObjectName(u"project_table")
        self.project_table.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.splitter_2.addWidget(self.project_table)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.object_tree = ObjectTreeView(self.splitter)
        self.object_tree.setObjectName(u"object_tree")
        self.splitter.addWidget(self.object_tree)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.pset_tree = PsetTreeView(self.verticalLayoutWidget)
        self.pset_tree.setObjectName(u"pset_tree")

        self.verticalLayout.addWidget(self.pset_tree)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.splitter_2.addWidget(self.splitter)

        self.verticalLayout_2.addWidget(self.splitter_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

