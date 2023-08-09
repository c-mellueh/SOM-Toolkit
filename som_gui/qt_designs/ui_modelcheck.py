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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(667, 472)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setHorizontalSpacing(5)
        self.label_export_missing = QLabel(Form)
        self.label_export_missing.setObjectName(u"label_export_missing")

        self.gridLayout.addWidget(self.label_export_missing, 6, 0, 1, 1)

        self.button_ifc = QPushButton(Form)
        self.button_ifc.setObjectName(u"button_ifc")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_ifc.sizePolicy().hasHeightForWidth())
        self.button_ifc.setSizePolicy(sizePolicy)
        self.button_ifc.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.button_ifc, 2, 2, 1, 1)

        self.label_ifc = QLabel(Form)
        self.label_ifc.setObjectName(u"label_ifc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_ifc.sizePolicy().hasHeightForWidth())
        self.label_ifc.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_ifc, 1, 0, 1, 1)

        self.line_edit_export = QLineEdit(Form)
        self.line_edit_export.setObjectName(u"line_edit_export")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_edit_export.sizePolicy().hasHeightForWidth())
        self.line_edit_export.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.line_edit_export, 5, 0, 1, 2)

        self.label_ifc_missing = QLabel(Form)
        self.label_ifc_missing.setObjectName(u"label_ifc_missing")
        self.label_ifc_missing.setEnabled(True)
        self.label_ifc_missing.setTextFormat(Qt.PlainText)

        self.gridLayout.addWidget(self.label_ifc_missing, 3, 0, 1, 1)

        self.line_edit_ident_pset = QLineEdit(Form)
        self.line_edit_ident_pset.setObjectName(u"line_edit_ident_pset")

        self.gridLayout.addWidget(self.line_edit_ident_pset, 0, 0, 1, 1)

        self.label_export = QLabel(Form)
        self.label_export.setObjectName(u"label_export")
        sizePolicy1.setHeightForWidth(self.label_export.sizePolicy().hasHeightForWidth())
        self.label_export.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_export, 4, 0, 1, 1)

        self.button_export = QPushButton(Form)
        self.button_export.setObjectName(u"button_export")
        sizePolicy.setHeightForWidth(self.button_export.sizePolicy().hasHeightForWidth())
        self.button_export.setSizePolicy(sizePolicy)
        self.button_export.setMaximumSize(QSize(25, 16777215))

        self.gridLayout.addWidget(self.button_export, 5, 2, 1, 1)

        self.line_edit_ident_attribute = QLineEdit(Form)
        self.line_edit_ident_attribute.setObjectName(u"line_edit_ident_attribute")

        self.gridLayout.addWidget(self.line_edit_ident_attribute, 0, 1, 1, 1)

        self.line_edit_ifc = QLineEdit(Form)
        self.line_edit_ifc.setObjectName(u"line_edit_ifc")
        sizePolicy2.setHeightForWidth(self.line_edit_ifc.sizePolicy().hasHeightForWidth())
        self.line_edit_ifc.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.line_edit_ifc, 2, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.table_widget = QTableWidget(Form)
        if (self.table_widget.columnCount() < 2):
            self.table_widget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table_widget.setObjectName(u"table_widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.table_widget.sizePolicy().hasHeightForWidth())
        self.table_widget.setSizePolicy(sizePolicy3)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.table_widget)

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
        self.label_export_missing.setText(QCoreApplication.translate("Form", u"Export Pfad fehlt!", None))
        self.button_ifc.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_ifc.setText(QCoreApplication.translate("Form", u"IFC Pfad", None))
        self.label_ifc_missing.setText(QCoreApplication.translate("Form", u"IFC Pfad fehlt!", None))
        self.line_edit_ident_pset.setText("")
        self.line_edit_ident_pset.setPlaceholderText(QCoreApplication.translate("Form", u"Ident PropertySet", None))
        self.label_export.setText(QCoreApplication.translate("Form", u"Excel Export Pfad", None))
        self.button_export.setText(QCoreApplication.translate("Form", u"...", None))
        self.line_edit_ident_attribute.setPlaceholderText(QCoreApplication.translate("Form", u"Ident Attribut", None))
        ___qtablewidgetitem = self.table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Fehlertyp", None));
        ___qtablewidgetitem1 = self.table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Beschreibung", None));
        self.label_status.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.button_run.setText(QCoreApplication.translate("Form", u"Run", None))
        self.button_close.setText(QCoreApplication.translate("Form", u"Close", None))
    # retranslateUi

