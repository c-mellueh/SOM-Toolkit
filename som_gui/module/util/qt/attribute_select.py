# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AttributeSelect.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QSizePolicy,
                               QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(726, 40)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.le_pset_name = QLineEdit(Form)
        self.le_pset_name.setObjectName(u"le_pset_name")

        self.horizontalLayout.addWidget(self.le_pset_name)

        self.le_attribute_name = QLineEdit(Form)
        self.le_attribute_name.setObjectName(u"le_attribute_name")

        self.horizontalLayout.addWidget(self.le_attribute_name)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.le_pset_name.setPlaceholderText(QCoreApplication.translate("Form", u"Ident PropertySet", None))
        self.le_attribute_name.setPlaceholderText(QCoreApplication.translate("Form", u"Ident Attribute", None))
    # retranslateUi

