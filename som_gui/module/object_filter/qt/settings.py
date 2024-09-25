# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
                               QSizePolicy, QWidget)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 68)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.label_usecase = QLabel(Form)
        self.label_usecase.setObjectName(u"label_usecase")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_usecase)

        self.cb_usecase = QComboBox(Form)
        self.cb_usecase.setObjectName(u"cb_usecase")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cb_usecase)

        self.label_phase = QLabel(Form)
        self.label_phase.setObjectName(u"label_phase")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_phase)

        self.cb_phase = QComboBox(Form)
        self.cb_phase.setObjectName(u"cb_phase")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cb_phase)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_usecase.setText(QCoreApplication.translate("Form", u"Anwendungsfall", None))
        self.label_phase.setText(QCoreApplication.translate("Form", u"Leistungsphase", None))
    # retranslateUi
