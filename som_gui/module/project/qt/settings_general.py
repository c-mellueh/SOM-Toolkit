# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsGeneral.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
                               QSizePolicy, QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(578, 173)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.le_name = QLineEdit(Form)
        self.le_name.setObjectName(u"le_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_name)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.le_version = QLineEdit(Form)
        self.le_version.setObjectName(u"le_version")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_version)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.le_author_mail = QLineEdit(Form)
        self.le_author_mail.setObjectName(u"le_author_mail")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.le_author_mail)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label)

        self.le_description = QTextEdit(Form)
        self.le_description.setObjectName(u"le_description")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.le_description)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Projekt Name:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Version:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Author Email:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Beschreibung:", None))
    # retranslateUi

