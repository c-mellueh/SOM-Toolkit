# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PropertySetMapping.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(640, 118)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_name = QLabel(Dialog)
        self.label_name.setObjectName(u"label_name")

        self.verticalLayout.addWidget(self.label_name)

        self.widget_input_lines = QWidget(Dialog)
        self.widget_input_lines.setObjectName(u"widget_input_lines")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_input_lines.sizePolicy().hasHeightForWidth())
        self.widget_input_lines.setSizePolicy(sizePolicy)
        self.widget_input_lines.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.widget_input_lines)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_edit = QLineEdit(self.widget_input_lines)
        self.line_edit.setObjectName(u"line_edit")

        self.gridLayout.addWidget(self.line_edit, 0, 0, 1, 1)

        self.button_add = QPushButton(self.widget_input_lines)
        self.button_add.setObjectName(u"button_add")

        self.gridLayout.addWidget(self.button_add, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget_input_lines)

        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_name.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.button_add.setText(QCoreApplication.translate("Dialog", u"+", None))
    # retranslateUi

