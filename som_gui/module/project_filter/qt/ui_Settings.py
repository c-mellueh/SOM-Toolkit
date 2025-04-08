# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
                               QVBoxLayout, QWidget)

class Ui_FilterWindow(object):
    def setupUi(self, FilterWindow):
        if not FilterWindow.objectName():
            FilterWindow.setObjectName(u"FilterWindow")
        FilterWindow.resize(708, 194)
        self.horizontalLayout = QHBoxLayout(FilterWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_phase = QLabel(FilterWindow)
        self.label_phase.setObjectName(u"label_phase")

        self.verticalLayout_2.addWidget(self.label_phase)

        self.widget_phase = QWidget(FilterWindow)
        self.widget_phase.setObjectName(u"widget_phase")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_phase.sizePolicy().hasHeightForWidth())
        self.widget_phase.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.widget_phase)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_usecase = QLabel(FilterWindow)
        self.label_usecase.setObjectName(u"label_usecase")

        self.verticalLayout.addWidget(self.label_usecase)

        self.widget_usecase = QWidget(FilterWindow)
        self.widget_usecase.setObjectName(u"widget_usecase")
        sizePolicy.setHeightForWidth(self.widget_usecase.sizePolicy().hasHeightForWidth())
        self.widget_usecase.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.widget_usecase)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(FilterWindow)

        QMetaObject.connectSlotsByName(FilterWindow)
    # setupUi

    def retranslateUi(self, FilterWindow):
        FilterWindow.setWindowTitle(QCoreApplication.translate("FilterWindow", u"Form", None))
        self.label_phase.setText(QCoreApplication.translate("FilterWindow", u"Phase", None))
        self.label_usecase.setText(QCoreApplication.translate("FilterWindow", u"Usecase", None))
    # retranslateUi

