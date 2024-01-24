# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PredefinedPropertySetWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
                               QDialogButtonBox, QGridLayout, QLabel, QListWidget,
                               QListWidgetItem, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(640, 480)
        Dialog.setContextMenuPolicy(Qt.CustomContextMenu)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.list_view_existance = QListWidget(Dialog)
        self.list_view_existance.setObjectName(u"list_view_existance")
        self.list_view_existance.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_view_existance.setSortingEnabled(True)

        self.gridLayout.addWidget(self.list_view_existance, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.list_view_pset = QListWidget(Dialog)
        self.list_view_pset.setObjectName(u"list_view_pset")
        self.list_view_pset.setFocusPolicy(Qt.StrongFocus)
        self.list_view_pset.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view_pset.setEditTriggers(QAbstractItemView.EditKeyPressed)
        self.list_view_pset.setSortingEnabled(True)

        self.gridLayout.addWidget(self.list_view_pset, 1, 0, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"PropertySet", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Erbt an:", None))
    # retranslateUi
