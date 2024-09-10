# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
                               QSizePolicy, QToolBox, QVBoxLayout, QWidget)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 480)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.toolBox = QToolBox(Form)
        self.toolBox.setObjectName(u"toolBox")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 622, 400))
        self.toolBox.addItem(self.page_2, u"Page 2")

        self.verticalLayout.addWidget(self.toolBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.le_export_path = QLineEdit(Form)
        self.le_export_path.setObjectName(u"le_export_path")

        self.horizontalLayout.addWidget(self.le_export_path)

        self.bu_select_path = QPushButton(Form)
        self.bu_select_path.setObjectName(u"bu_select_path")
        self.bu_select_path.setMaximumSize(QSize(24, 16777215))

        self.horizontalLayout.addWidget(self.bu_select_path)

        self.bu_run = QPushButton(Form)
        self.bu_run.setObjectName(u"bu_run")

        self.horizontalLayout.addWidget(self.bu_run)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)

        self.toolBox.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("Form", u"Page 2", None))
        self.le_export_path.setPlaceholderText(QCoreApplication.translate("Form", u"export path", None))
        self.bu_select_path.setText(QCoreApplication.translate("Form", u"...", None))
        self.bu_run.setText(QCoreApplication.translate("Form", u"Run", None))
    # retranslateUi
