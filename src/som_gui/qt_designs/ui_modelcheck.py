# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Modelcheck.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
    QGridLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(684, 220)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setHorizontalSpacing(5)
        self.label_ifc = QLabel(Dialog)
        self.label_ifc.setObjectName(u"label_ifc")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ifc.sizePolicy().hasHeightForWidth())
        self.label_ifc.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_ifc, 1, 0, 1, 1)

        self.button_ifc = QPushButton(Dialog)
        self.button_ifc.setObjectName(u"button_ifc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_ifc.sizePolicy().hasHeightForWidth())
        self.button_ifc.setSizePolicy(sizePolicy1)
        self.button_ifc.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.button_ifc, 2, 2, 1, 1)

        self.label_export = QLabel(Dialog)
        self.label_export.setObjectName(u"label_export")
        sizePolicy.setHeightForWidth(self.label_export.sizePolicy().hasHeightForWidth())
        self.label_export.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_export, 4, 0, 1, 1)

        self.line_edit_ifc = QLineEdit(Dialog)
        self.line_edit_ifc.setObjectName(u"line_edit_ifc")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_edit_ifc.sizePolicy().hasHeightForWidth())
        self.line_edit_ifc.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.line_edit_ifc, 2, 0, 1, 2)

        self.line_edit_ident_pset = QLineEdit(Dialog)
        self.line_edit_ident_pset.setObjectName(u"line_edit_ident_pset")

        self.gridLayout.addWidget(self.line_edit_ident_pset, 0, 0, 1, 1)

        self.label_ifc_missing = QLabel(Dialog)
        self.label_ifc_missing.setObjectName(u"label_ifc_missing")
        self.label_ifc_missing.setEnabled(True)
        self.label_ifc_missing.setTextFormat(Qt.PlainText)

        self.gridLayout.addWidget(self.label_ifc_missing, 3, 0, 1, 1)

        self.line_edit_ident_attribute = QLineEdit(Dialog)
        self.line_edit_ident_attribute.setObjectName(u"line_edit_ident_attribute")

        self.gridLayout.addWidget(self.line_edit_ident_attribute, 0, 1, 1, 1)

        self.label_export_missing = QLabel(Dialog)
        self.label_export_missing.setObjectName(u"label_export_missing")

        self.gridLayout.addWidget(self.label_export_missing, 6, 0, 1, 1)

        self.line_edit_export = QLineEdit(Dialog)
        self.line_edit_export.setObjectName(u"line_edit_export")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line_edit_export.sizePolicy().hasHeightForWidth())
        self.line_edit_export.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.line_edit_export, 5, 0, 1, 2)

        self.button_export = QPushButton(Dialog)
        self.button_export.setObjectName(u"button_export")
        sizePolicy1.setHeightForWidth(self.button_export.sizePolicy().hasHeightForWidth())
        self.button_export.setSizePolicy(sizePolicy1)
        self.button_export.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.button_export, 5, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

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
        self.label_ifc.setText(QCoreApplication.translate("Dialog", u"IFC Pfad", None))
        self.button_ifc.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_export.setText(QCoreApplication.translate("Dialog", u"Excel Export Pfad", None))
        self.line_edit_ident_pset.setText("")
        self.line_edit_ident_pset.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ident PropertySet", None))
        self.label_ifc_missing.setText(QCoreApplication.translate("Dialog", u"IFC Pfad fehlt!", None))
        self.line_edit_ident_attribute.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ident Attribut", None))
        self.label_export_missing.setText(QCoreApplication.translate("Dialog", u"Export Pfad fehlt!", None))
        self.button_export.setText(QCoreApplication.translate("Dialog", u"...", None))
    # retranslateUi

