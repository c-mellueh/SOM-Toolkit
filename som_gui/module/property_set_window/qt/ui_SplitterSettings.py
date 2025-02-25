# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SplitterSettings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(478, 53)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.line_edit_seperator = QLineEdit(Form)
        self.line_edit_seperator.setObjectName(u"line_edit_seperator")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_seperator.sizePolicy().hasHeightForWidth())
        self.line_edit_seperator.setSizePolicy(sizePolicy)
        self.line_edit_seperator.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.line_edit_seperator, 3, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Shadow.Raised)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line, 0, 0, 1, 2)

        self.check_box_seperator = QCheckBox(Form)
        self.check_box_seperator.setObjectName(u"check_box_seperator")
        self.check_box_seperator.setChecked(True)

        self.gridLayout.addWidget(self.check_box_seperator, 3, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.line_edit_seperator.setPlaceholderText(QCoreApplication.translate("Form", u"Splitter text", None))
        self.label.setText(QCoreApplication.translate("Form", u"Splitter", None))
        self.check_box_seperator.setText(QCoreApplication.translate("Form", u"Use Splitter", None))
    # retranslateUi

