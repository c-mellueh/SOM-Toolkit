# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ModelControl.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1104, 678)
        Form.setMinimumSize(QSize(30, 100))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.splitter_attribute = QSplitter(Form)
        self.splitter_attribute.setObjectName(u"splitter_attribute")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_attribute.sizePolicy().hasHeightForWidth())
        self.splitter_attribute.setSizePolicy(sizePolicy)
        self.splitter_attribute.setOrientation(Qt.Horizontal)
        self.line_edit_ident_pset = QLineEdit(self.splitter_attribute)
        self.line_edit_ident_pset.setObjectName(u"line_edit_ident_pset")
        self.splitter_attribute.addWidget(self.line_edit_ident_pset)
        self.line_edit_ident_attribute = QLineEdit(self.splitter_attribute)
        self.line_edit_ident_attribute.setObjectName(u"line_edit_ident_attribute")
        self.splitter_attribute.addWidget(self.line_edit_ident_attribute)

        self.verticalLayout.addWidget(self.splitter_attribute)

        self.label_ifc = QLabel(Form)
        self.label_ifc.setObjectName(u"label_ifc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_ifc.sizePolicy().hasHeightForWidth())
        self.label_ifc.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.label_ifc)

        self.horizontal_layout_ifc = QHBoxLayout()
        self.horizontal_layout_ifc.setObjectName(u"horizontal_layout_ifc")
        self.line_edit_ifc = QLineEdit(Form)
        self.line_edit_ifc.setObjectName(u"line_edit_ifc")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_edit_ifc.sizePolicy().hasHeightForWidth())
        self.line_edit_ifc.setSizePolicy(sizePolicy2)

        self.horizontal_layout_ifc.addWidget(self.line_edit_ifc)

        self.button_ifc = QPushButton(Form)
        self.button_ifc.setObjectName(u"button_ifc")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_ifc.sizePolicy().hasHeightForWidth())
        self.button_ifc.setSizePolicy(sizePolicy3)
        self.button_ifc.setMaximumSize(QSize(25, 16777215))

        self.horizontal_layout_ifc.addWidget(self.button_ifc)

        self.button_run = QPushButton(Form)
        self.button_run.setObjectName(u"button_run")

        self.horizontal_layout_ifc.addWidget(self.button_run)


        self.verticalLayout.addLayout(self.horizontal_layout_ifc)

        self.label_ifc_missing = QLabel(Form)
        self.label_ifc_missing.setObjectName(u"label_ifc_missing")
        self.label_ifc_missing.setEnabled(True)
        self.label_ifc_missing.setTextFormat(Qt.PlainText)

        self.verticalLayout.addWidget(self.label_ifc_missing)

        self.progress_bar = QProgressBar(Form)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setEnabled(True)
        self.progress_bar.setValue(24)

        self.verticalLayout.addWidget(self.progress_bar)

        self.horizontal_layout_buttons = QHBoxLayout()
        self.horizontal_layout_buttons.setObjectName(u"horizontal_layout_buttons")
        self.button_last = QPushButton(Form)
        self.button_last.setObjectName(u"button_last")
        self.button_last.setEnabled(True)

        self.horizontal_layout_buttons.addWidget(self.button_last)

        self.button_next = QPushButton(Form)
        self.button_next.setObjectName(u"button_next")
        self.button_next.setEnabled(True)

        self.horizontal_layout_buttons.addWidget(self.button_next)


        self.verticalLayout.addLayout(self.horizontal_layout_buttons)

        self.splitter_lists = QSplitter(Form)
        self.splitter_lists.setObjectName(u"splitter_lists")
        self.splitter_lists.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.splitter_lists.sizePolicy().hasHeightForWidth())
        self.splitter_lists.setSizePolicy(sizePolicy4)
        self.splitter_lists.setOrientation(Qt.Horizontal)
        self.list_widget_property_set = QListWidget(self.splitter_lists)
        self.list_widget_property_set.setObjectName(u"list_widget_property_set")
        self.splitter_lists.addWidget(self.list_widget_property_set)
        self.list_widget_attribute = QListWidget(self.splitter_lists)
        self.list_widget_attribute.setObjectName(u"list_widget_attribute")
        self.splitter_lists.addWidget(self.list_widget_attribute)
        self.list_widget_value = QTableWidget(self.splitter_lists)
        if (self.list_widget_value.columnCount() < 2):
            self.list_widget_value.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.list_widget_value.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.list_widget_value.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.list_widget_value.setObjectName(u"list_widget_value")
        self.splitter_lists.addWidget(self.list_widget_value)

        self.verticalLayout.addWidget(self.splitter_lists)

        self.horzontal_layout_action_buttons = QHBoxLayout()
        self.horzontal_layout_action_buttons.setObjectName(u"horzontal_layout_action_buttons")
        self.horizontal_spacer_action_buttons = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horzontal_layout_action_buttons.addItem(self.horizontal_spacer_action_buttons)

        self.button_abbort = QPushButton(Form)
        self.button_abbort.setObjectName(u"button_abbort")

        self.horzontal_layout_action_buttons.addWidget(self.button_abbort)

        self.button_import_values = QPushButton(Form)
        self.button_import_values.setObjectName(u"button_import_values")

        self.horzontal_layout_action_buttons.addWidget(self.button_import_values)


        self.verticalLayout.addLayout(self.horzontal_layout_action_buttons)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.line_edit_ident_pset.setText("")
        self.line_edit_ident_pset.setPlaceholderText(QCoreApplication.translate("Form", u"Ident PropertySet", None))
        self.line_edit_ident_attribute.setPlaceholderText(QCoreApplication.translate("Form", u"Ident Attribut", None))
        self.label_ifc.setText(QCoreApplication.translate("Form", u"IFC Pfad", None))
        self.button_ifc.setText(QCoreApplication.translate("Form", u"...", None))
        self.button_run.setText(QCoreApplication.translate("Form", u"IFC Einlesen", None))
        self.label_ifc_missing.setText(QCoreApplication.translate("Form", u"IFC Pfad fehlt!", None))
        self.button_last.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.button_next.setText(QCoreApplication.translate("Form", u"PushButton", None))
        ___qtablewidgetitem = self.list_widget_value.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Wert", None));
        ___qtablewidgetitem1 = self.list_widget_value.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Akzeptiert", None));
        self.button_abbort.setText(QCoreApplication.translate("Form", u"Abbrechen", None))
        self.button_import_values.setText(QCoreApplication.translate("Form", u"Werte Importieren", None))
    # retranslateUi

