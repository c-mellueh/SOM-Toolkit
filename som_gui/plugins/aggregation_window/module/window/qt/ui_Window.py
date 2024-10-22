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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
                               QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

from ...view.ui import AggregationView
from ..ui import ComboBox


class Ui_Aggregation(object):
    def setupUi(self, Aggregation):
        if not Aggregation.objectName():
            Aggregation.setObjectName(u"Aggregation")
        Aggregation.resize(1027, 724)
        self.actionAdd_View = QAction(Aggregation)
        self.actionAdd_View.setObjectName(u"actionAdd_View")
        self.actionRename_View = QAction(Aggregation)
        self.actionRename_View.setObjectName(u"actionRename_View")
        self.actionDelete_current_View = QAction(Aggregation)
        self.actionDelete_current_View.setObjectName(u"actionDelete_current_View")
        self.actionFilter_View = QAction(Aggregation)
        self.actionFilter_View.setObjectName(u"actionFilter_View")
        self.actionReset_Filter = QAction(Aggregation)
        self.actionReset_Filter.setObjectName(u"actionReset_Filter")
        self.actionSearch_for_Node = QAction(Aggregation)
        self.actionSearch_for_Node.setObjectName(u"actionSearch_for_Node")
        self.actionCopy_selected_Nodes = QAction(Aggregation)
        self.actionCopy_selected_Nodes.setObjectName(u"actionCopy_selected_Nodes")
        self.actionPaste_Nodes = QAction(Aggregation)
        self.actionPaste_Nodes.setObjectName(u"actionPaste_Nodes")
        self.centralwidget = QWidget(Aggregation)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBox = ComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.graphicsView = AggregationView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)

        Aggregation.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Aggregation)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1027, 33))
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuAggregation = QMenu(self.menubar)
        self.menuAggregation.setObjectName(u"menuAggregation")
        Aggregation.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Aggregation)
        self.statusbar.setObjectName(u"statusbar")
        Aggregation.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuAggregation.menuAction())
        self.menuView.addAction(self.actionAdd_View)
        self.menuView.addAction(self.actionRename_View)
        self.menuView.addAction(self.actionDelete_current_View)
        self.menuView.addAction(self.actionFilter_View)
        self.menuView.addAction(self.actionReset_Filter)
        self.menuAggregation.addAction(self.actionSearch_for_Node)
        self.menuAggregation.addAction(self.actionCopy_selected_Nodes)
        self.menuAggregation.addAction(self.actionPaste_Nodes)

        self.retranslateUi(Aggregation)

        QMetaObject.connectSlotsByName(Aggregation)

    # setupUi

    def retranslateUi(self, Aggregation):
        Aggregation.setWindowTitle(QCoreApplication.translate("Aggregation", u"MainWindow", None))
        self.actionAdd_View.setText(QCoreApplication.translate("Aggregation", u"Add View", None))
        self.actionRename_View.setText(QCoreApplication.translate("Aggregation", u"Rename View", None))
        self.actionDelete_current_View.setText(QCoreApplication.translate("Aggregation", u"Delete current View", None))
        self.actionFilter_View.setText(QCoreApplication.translate("Aggregation", u"Filter View", None))
        self.actionReset_Filter.setText(QCoreApplication.translate("Aggregation", u"Reset Filter", None))
        self.actionSearch_for_Node.setText(QCoreApplication.translate("Aggregation", u"Search for Node", None))
        # if QT_CONFIG(shortcut)
        self.actionSearch_for_Node.setShortcut(QCoreApplication.translate("Aggregation", u"Ctrl+F", None))
        # endif // QT_CONFIG(shortcut)
        self.actionCopy_selected_Nodes.setText(QCoreApplication.translate("Aggregation", u"Copy selected Nodes", None))
        # if QT_CONFIG(shortcut)
        self.actionCopy_selected_Nodes.setShortcut(QCoreApplication.translate("Aggregation", u"Ctrl+C", None))
        # endif // QT_CONFIG(shortcut)
        self.actionPaste_Nodes.setText(QCoreApplication.translate("Aggregation", u"Paste Nodes", None))
        # if QT_CONFIG(shortcut)
        self.actionPaste_Nodes.setShortcut(QCoreApplication.translate("Aggregation", u"Ctrl+V", None))
        # endif // QT_CONFIG(shortcut)
        self.menuView.setTitle(QCoreApplication.translate("Aggregation", u"View", None))
        self.menuAggregation.setTitle(QCoreApplication.translate("Aggregation", u"Aggregation", None))
    # retranslateUi
