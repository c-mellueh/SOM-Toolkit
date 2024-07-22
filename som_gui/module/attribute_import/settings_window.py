# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AttributeImportSettings.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
                               QDialogButtonBox, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(275, 172)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.check_box_boolean_values = QCheckBox(Dialog)
        self.check_box_boolean_values.setObjectName(u"check_box_boolean_values")
        self.check_box_boolean_values.setLayoutDirection(Qt.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_boolean_values)

        self.check_box_regex = QCheckBox(Dialog)
        self.check_box_regex.setObjectName(u"check_box_regex")
        self.check_box_regex.setLayoutDirection(Qt.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_regex)

        self.check_box_range = QCheckBox(Dialog)
        self.check_box_range.setObjectName(u"check_box_range")
        self.check_box_range.setLayoutDirection(Qt.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_range)

        self.check_box_existing_attributes = QCheckBox(Dialog)
        self.check_box_existing_attributes.setObjectName(u"check_box_existing_attributes")
        self.check_box_existing_attributes.setLayoutDirection(Qt.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_existing_attributes)

        self.check_box_color = QCheckBox(Dialog)
        self.check_box_color.setObjectName(u"check_box_color")
        self.check_box_color.setLayoutDirection(Qt.RightToLeft)
        self.check_box_color.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.check_box_color)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.check_box_boolean_values.setText(QCoreApplication.translate("Dialog", u"IfcBoolean importieren", None))
        self.check_box_regex.setText(QCoreApplication.translate("Dialog", u"RegEx-Vorgaben importieren", None))
        self.check_box_range.setText(QCoreApplication.translate("Dialog", u"Range-Vorgaben importieren", None))
        self.check_box_existing_attributes.setText(
            QCoreApplication.translate("Dialog", u"Bereits existierende Vorgaben anzeigen", None))
        self.check_box_color.setText(QCoreApplication.translate("Dialog", u"Daten einf\u00e4rben", None))
    # retranslateUi

