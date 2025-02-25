# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UnitSettings.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QListWidget,
    QListWidgetItem, QSizePolicy, QVBoxLayout, QWidget)

class Ui_UnitSettings(object):
    def setupUi(self, UnitSettings):
        if not UnitSettings.objectName():
            UnitSettings.setObjectName(u"UnitSettings")
        UnitSettings.resize(557, 227)
        self.verticalLayout = QVBoxLayout(UnitSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(UnitSettings)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.list_units = QListWidget(UnitSettings)
        self.list_units.setObjectName(u"list_units")

        self.verticalLayout.addWidget(self.list_units)

        self.line_2 = QFrame(UnitSettings)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Shadow.Raised)
        self.line_2.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout.addWidget(self.line_2)

        self.label_2 = QLabel(UnitSettings)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.list_prefixes = QListWidget(UnitSettings)
        self.list_prefixes.setObjectName(u"list_prefixes")

        self.verticalLayout.addWidget(self.list_prefixes)


        self.retranslateUi(UnitSettings)

        QMetaObject.connectSlotsByName(UnitSettings)
    # setupUi

    def retranslateUi(self, UnitSettings):
        UnitSettings.setWindowTitle(QCoreApplication.translate("UnitSettings", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("UnitSettings", u"Active Units", None))
        self.label_2.setText(QCoreApplication.translate("UnitSettings", u"Active Unit Prefixes", None))
    # retranslateUi

