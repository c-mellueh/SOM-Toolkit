# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
                               QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(708, 194)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_phase = QLabel(Form)
        self.label_phase.setObjectName(u"label_phase")

        self.verticalLayout_2.addWidget(self.label_phase)

        self.widget_phase = QWidget(Form)
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
        self.label_usecase = QLabel(Form)
        self.label_usecase.setObjectName(u"label_usecase")

        self.verticalLayout.addWidget(self.label_usecase)

        self.widget_usecase = QWidget(Form)
        self.widget_usecase.setObjectName(u"widget_usecase")
        sizePolicy.setHeightForWidth(self.widget_usecase.sizePolicy().hasHeightForWidth())
        self.widget_usecase.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.widget_usecase)

        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_phase.setText(QCoreApplication.translate("Form", u"Leistungsphase", None))
        self.label_usecase.setText(QCoreApplication.translate("Form", u"Anwendungsfall", None))
    # retranslateUi

