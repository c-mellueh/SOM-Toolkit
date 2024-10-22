# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsWidget.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
                               QDialogButtonBox, QSizePolicy, QVBoxLayout, QWidget)

class Ui_AttributeImport(object):
    def setupUi(self, AttributeImport):
        if not AttributeImport.objectName():
            AttributeImport.setObjectName(u"AttributeImport")
        AttributeImport.resize(281, 203)
        self.verticalLayout = QVBoxLayout(AttributeImport)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.check_box_boolean_values = QCheckBox(AttributeImport)
        self.check_box_boolean_values.setObjectName(u"check_box_boolean_values")
        self.check_box_boolean_values.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_boolean_values)

        self.check_box_regex = QCheckBox(AttributeImport)
        self.check_box_regex.setObjectName(u"check_box_regex")
        self.check_box_regex.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_regex)

        self.check_box_range = QCheckBox(AttributeImport)
        self.check_box_range.setObjectName(u"check_box_range")
        self.check_box_range.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_range)

        self.check_box_existing_attributes = QCheckBox(AttributeImport)
        self.check_box_existing_attributes.setObjectName(u"check_box_existing_attributes")
        self.check_box_existing_attributes.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_existing_attributes)

        self.check_box_color = QCheckBox(AttributeImport)
        self.check_box_color.setObjectName(u"check_box_color")
        self.check_box_color.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.check_box_color.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.check_box_color)

        self.check_box_object_filter = QCheckBox(AttributeImport)
        self.check_box_object_filter.setObjectName(u"check_box_object_filter")
        self.check_box_object_filter.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_object_filter)

        self.buttonBox = QDialogButtonBox(AttributeImport)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AttributeImport)
        self.buttonBox.accepted.connect(AttributeImport.accept)
        self.buttonBox.rejected.connect(AttributeImport.reject)

        QMetaObject.connectSlotsByName(AttributeImport)
    # setupUi

    def retranslateUi(self, AttributeImport):
        AttributeImport.setWindowTitle(QCoreApplication.translate("AttributeImport", u"Dialog", None))
        self.check_box_boolean_values.setText(QCoreApplication.translate("AttributeImport", u"show IfcBoolean", None))
        self.check_box_regex.setText(QCoreApplication.translate("AttributeImport", u"show RegEx", None))
        self.check_box_range.setText(QCoreApplication.translate("AttributeImport", u"show Range", None))
        self.check_box_existing_attributes.setText(
            QCoreApplication.translate("AttributeImport", u"show allready Existing", None))
        self.check_box_color.setText(QCoreApplication.translate("AttributeImport", u"color Data", None))
        self.check_box_object_filter.setText(
            QCoreApplication.translate("AttributeImport", u"filter by Usecase/Phase", None))
    # retranslateUi

