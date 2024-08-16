# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CompareWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
                               QSplitter, QTableWidget, QTableWidgetItem, QTreeWidgetItem,
                               QVBoxLayout, QWidget)

from som_gui.module.compare.ui import EntityTreeWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(713, 298)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.tree_widget_propertysets = EntityTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_widget_propertysets.setHeaderItem(__qtreewidgetitem)
        self.tree_widget_propertysets.setObjectName(u"tree_widget_propertysets")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tree_widget_propertysets.sizePolicy().hasHeightForWidth())
        self.tree_widget_propertysets.setSizePolicy(sizePolicy1)
        self.splitter.addWidget(self.tree_widget_propertysets)
        self.table_widget_values = QTableWidget(self.splitter)
        self.table_widget_values.setObjectName(u"table_widget_values")
        sizePolicy1.setHeightForWidth(self.table_widget_values.sizePolicy().hasHeightForWidth())
        self.table_widget_values.setSizePolicy(sizePolicy1)
        self.table_widget_values.setSelectionMode(QAbstractItemView.NoSelection)
        self.splitter.addWidget(self.table_widget_values)
        self.table_widget_values.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi
