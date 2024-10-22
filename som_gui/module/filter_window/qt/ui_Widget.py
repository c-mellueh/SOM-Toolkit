# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QLabel,
                               QSizePolicy, QSplitter, QVBoxLayout, QWidget)

from som_gui.module.filter_window.ui import (ObjectTreeView, ProjectView, PsetTreeView)


class Ui_FilterWindow(object):
    def setupUi(self, FilterWindow):
        if not FilterWindow.objectName():
            FilterWindow.setObjectName(u"FilterWindow")
        FilterWindow.resize(1263, 853)
        self.verticalLayout_2 = QVBoxLayout(FilterWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter_2 = QSplitter(FilterWindow)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.project_table = ProjectView(self.splitter_2)
        self.project_table.setObjectName(u"project_table")
        self.project_table.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.project_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.splitter_2.addWidget(self.project_table)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
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

        self.retranslateUi(FilterWindow)

        QMetaObject.connectSlotsByName(FilterWindow)
    # setupUi

    def retranslateUi(self, FilterWindow):
        FilterWindow.setWindowTitle(QCoreApplication.translate("FilterWindow", u"Form", None))
        self.label.setText("")
    # retranslateUi

