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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(667, 276)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setHorizontalSpacing(5)
        self.button_ifc = QPushButton(Form)
        self.button_ifc.setObjectName(u"button_ifc")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_ifc.sizePolicy().hasHeightForWidth())
        self.button_ifc.setSizePolicy(sizePolicy)
        self.button_ifc.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.button_ifc, 3, 2, 1, 1)

        self.line_edit_export = QLineEdit(Form)
        self.line_edit_export.setObjectName(u"line_edit_export")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_export.sizePolicy().hasHeightForWidth())
        self.line_edit_export.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.line_edit_export, 6, 0, 1, 2)

        self.button_export = QPushButton(Form)
        self.button_export.setObjectName(u"button_export")
        sizePolicy.setHeightForWidth(self.button_export.sizePolicy().hasHeightForWidth())
        self.button_export.setSizePolicy(sizePolicy)
        self.button_export.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.button_export, 6, 2, 1, 1)

        self.line_edit_ifc = QLineEdit(Form)
        self.line_edit_ifc.setObjectName(u"line_edit_ifc")
        sizePolicy1.setHeightForWidth(self.line_edit_ifc.sizePolicy().hasHeightForWidth())
        self.line_edit_ifc.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.line_edit_ifc, 3, 0, 1, 2)

        self.layout_attribute = QGridLayout()
        self.layout_attribute.setObjectName(u"layout_attribute")
        self.line_edit_ident_attribute = QLineEdit(Form)
        self.line_edit_ident_attribute.setObjectName(u"line_edit_ident_attribute")

        self.layout_attribute.addWidget(self.line_edit_ident_attribute, 0, 1, 1, 1)

        self.line_edit_ident_pset = QLineEdit(Form)
        self.line_edit_ident_pset.setObjectName(u"line_edit_ident_pset")

        self.layout_attribute.addWidget(self.line_edit_ident_pset, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.layout_attribute, 0, 0, 1, 3)

        self.label_ifc = QLabel(Form)
        self.label_ifc.setObjectName(u"label_ifc")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_ifc.sizePolicy().hasHeightForWidth())
        self.label_ifc.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_ifc, 2, 0, 1, 3)

        self.label_ifc_missing = QLabel(Form)
        self.label_ifc_missing.setObjectName(u"label_ifc_missing")
        self.label_ifc_missing.setEnabled(True)
        self.label_ifc_missing.setTextFormat(Qt.PlainText)

        self.gridLayout.addWidget(self.label_ifc_missing, 4, 0, 1, 3)

        self.label_export = QLabel(Form)
        self.label_export.setObjectName(u"label_export")
        sizePolicy2.setHeightForWidth(self.label_export.sizePolicy().hasHeightForWidth())
        self.label_export.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_export, 5, 0, 1, 3)

        self.label_export_missing = QLabel(Form)
        self.label_export_missing.setObjectName(u"label_export_missing")

        self.gridLayout.addWidget(self.label_export_missing, 7, 0, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout)

        self.label_status = QLabel(Form)
        self.label_status.setObjectName(u"label_status")

        self.verticalLayout.addWidget(self.label_status)

        self.progress_bar = QProgressBar(Form)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)
        self.progress_bar.setTextVisible(True)

        self.verticalLayout.addWidget(self.progress_bar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_run = QPushButton(Form)
        self.button_run.setObjectName(u"button_run")

        self.horizontalLayout.addWidget(self.button_run)

        self.button_close = QPushButton(Form)
        self.button_close.setObjectName(u"button_close")

        self.horizontalLayout.addWidget(self.button_close)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button_ifc.setText(QCoreApplication.translate("Form", u"...", None))
        self.button_export.setText(QCoreApplication.translate("Form", u"...", None))
        self.line_edit_ident_attribute.setPlaceholderText(QCoreApplication.translate("Form", u"Ident Attribut", None))
        self.line_edit_ident_pset.setText("")
        self.line_edit_ident_pset.setPlaceholderText(QCoreApplication.translate("Form", u"Ident PropertySet", None))
        self.label_ifc.setText(QCoreApplication.translate("Form", u"IFC Pfad", None))
        self.label_ifc_missing.setText(QCoreApplication.translate("Form", u"IFC Pfad fehlt!", None))
        self.label_export.setText(QCoreApplication.translate("Form", u"Fehler Export Pfad", None))
        self.label_export_missing.setText(QCoreApplication.translate("Form", u"Export Pfad fehlt!", None))
        self.label_status.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.button_run.setText(QCoreApplication.translate("Form", u"Run", None))
        self.button_close.setText(QCoreApplication.translate("Form", u"Close", None))
    # retranslateUi

