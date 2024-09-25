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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
                               QPlainTextEdit, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(578, 173)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.le_version = QLineEdit(Form)
        self.le_version.setObjectName(u"le_version")

        self.gridLayout.addWidget(self.le_version, 1, 1, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.le_author_mail = QLineEdit(Form)
        self.le_author_mail.setObjectName(u"le_author_mail")

        self.gridLayout.addWidget(self.le_author_mail, 2, 1, 1, 1)

        self.le_name = QLineEdit(Form)
        self.le_name.setObjectName(u"le_name")

        self.gridLayout.addWidget(self.le_name, 0, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.le_description = QPlainTextEdit(Form)
        self.le_description.setObjectName(u"le_description")

        self.gridLayout.addWidget(self.le_description, 3, 1, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Author Email:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Version:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Projekt Name:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Beschreibung:", None))
    # retranslateUi

