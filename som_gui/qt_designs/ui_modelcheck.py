# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Modelcheck.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QHeaderView,
    QListWidget, QListWidgetItem, QSizePolicy, QSplitter,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(836, 429)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tree_widget_objects = QTreeWidget(self.splitter)
        self.tree_widget_objects.setObjectName(u"tree_widget_objects")
        self.splitter.addWidget(self.tree_widget_objects)
        self.list_widget_checkrules = QListWidget(self.splitter)
        self.list_widget_checkrules.setObjectName(u"list_widget_checkrules")
        self.splitter.addWidget(self.list_widget_checkrules)

        self.verticalLayout.addWidget(self.splitter)

        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtreewidgetitem = self.tree_widget_objects.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Identifier", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Name", None));
    # retranslateUi

