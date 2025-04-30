# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MappingWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QWidget)

class Ui_MappingWidget(object):
    def setupUi(self, MappingWidget):
        if not MappingWidget.objectName():
            MappingWidget.setObjectName(u"MappingWidget")
        MappingWidget.resize(660, 156)
        self.gridLayout = QGridLayout(MappingWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_ifc_mapping = QLabel(MappingWidget)
        self.label_ifc_mapping.setObjectName(u"label_ifc_mapping")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ifc_mapping.sizePolicy().hasHeightForWidth())
        self.label_ifc_mapping.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_ifc_mapping, 1, 0, 1, 1)

        self.button_add_ifc = QPushButton(MappingWidget)
        self.button_add_ifc.setObjectName(u"button_add_ifc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_add_ifc.sizePolicy().hasHeightForWidth())
        self.button_add_ifc.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.button_add_ifc, 1, 2, 1, 1)

        self.table_view = QTableView(MappingWidget)
        self.table_view.setObjectName(u"table_view")
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setCascadingSectionResizes(True)

        self.gridLayout.addWidget(self.table_view, 3, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 1)


        self.retranslateUi(MappingWidget)

        QMetaObject.connectSlotsByName(MappingWidget)
    # setupUi

    def retranslateUi(self, MappingWidget):
        MappingWidget.setWindowTitle(QCoreApplication.translate("MappingWidget", u"Form", None))
        self.label_ifc_mapping.setText(QCoreApplication.translate("MappingWidget", u"IFC Mapping", None))
        self.button_add_ifc.setText(QCoreApplication.translate("MappingWidget", u"+", None))
    # retranslateUi

