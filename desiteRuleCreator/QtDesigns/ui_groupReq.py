# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'group_name_request.ui'
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
    QGridLayout, QLineEdit, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(456, 105)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pset_name = QLineEdit(Dialog)
        self.pset_name.setObjectName(u"pset_name")

        self.gridLayout.addWidget(self.pset_name, 1, 0, 1, 1)

        self.attribute_name = QLineEdit(Dialog)
        self.attribute_name.setObjectName(u"attribute_name")

        self.gridLayout.addWidget(self.attribute_name, 1, 1, 1, 1)

        self.attribute_value = QLineEdit(Dialog)
        self.attribute_value.setObjectName(u"attribute_value")

        self.gridLayout.addWidget(self.attribute_value, 1, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 2)

        self.group_name = QLineEdit(Dialog)
        self.group_name.setObjectName(u"group_name")

        self.gridLayout.addWidget(self.group_name, 0, 0, 1, 3)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pset_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"PropertySet", None))
        self.attribute_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"Attribute", None))
        self.attribute_value.setPlaceholderText(QCoreApplication.translate("Dialog", u"Value", None))
        self.group_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"Name of object", None))
    # retranslateUi

