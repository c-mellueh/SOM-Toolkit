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
        Form.resize(868, 462)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter_2 = QSplitter(Form)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.tree_widget_propertysets = EntityTreeWidget(self.splitter_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_widget_propertysets.setHeaderItem(__qtreewidgetitem)
        self.tree_widget_propertysets.setObjectName(u"tree_widget_propertysets")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_widget_propertysets.sizePolicy().hasHeightForWidth())
        self.tree_widget_propertysets.setSizePolicy(sizePolicy)
        self.splitter_2.addWidget(self.tree_widget_propertysets)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.table_widget_values = QTableWidget(self.splitter)
        self.table_widget_values.setObjectName(u"table_widget_values")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.table_widget_values.sizePolicy().hasHeightForWidth())
        self.table_widget_values.setSizePolicy(sizePolicy1)
        self.table_widget_values.setSelectionMode(QAbstractItemView.NoSelection)
        self.splitter.addWidget(self.table_widget_values)
        self.table_widget_values.horizontalHeader().setStretchLastSection(True)
        self.table_infos = QTableWidget(self.splitter)
        self.table_infos.setObjectName(u"table_infos")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.table_infos.sizePolicy().hasHeightForWidth())
        self.table_infos.setSizePolicy(sizePolicy2)
        self.splitter.addWidget(self.table_infos)
        self.table_infos.horizontalHeader().setStretchLastSection(True)
        self.splitter_2.addWidget(self.splitter)

        self.verticalLayout.addWidget(self.splitter_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

