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
    QLayout, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1104, 680)
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


        self.verticalLayout.addLayout(self.horizontal_layout_ifc)

        self.label_status = QLabel(Form)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setEnabled(True)
        self.label_status.setTextFormat(Qt.PlainText)

        self.verticalLayout.addWidget(self.label_status)

        self.progress_bar = QProgressBar(Form)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setEnabled(True)
        self.progress_bar.setValue(0)

        self.verticalLayout.addWidget(self.progress_bar)

        self.horizontal_layout_buttons = QHBoxLayout()
        self.horizontal_layout_buttons.setObjectName(u"horizontal_layout_buttons")
        self.button_last = QPushButton(Form)
        self.button_last.setObjectName(u"button_last")
        self.button_last.setEnabled(True)
        self.button_last.setMaximumSize(QSize(200, 24))

        self.horizontal_layout_buttons.addWidget(self.button_last)

        self.label_object_name = QLabel(Form)
        self.label_object_name.setObjectName(u"label_object_name")
        self.label_object_name.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_buttons.addWidget(self.label_object_name)

        self.button_next = QPushButton(Form)
        self.button_next.setObjectName(u"button_next")
        self.button_next.setEnabled(True)
        self.button_next.setMaximumSize(QSize(200, 24))

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
        self.table_widget_property_set = QTableWidget(self.splitter_lists)
        if (self.table_widget_property_set.columnCount() < 2):
            self.table_widget_property_set.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget_property_set.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget_property_set.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table_widget_property_set.setObjectName(u"table_widget_property_set")
        self.splitter_lists.addWidget(self.table_widget_property_set)
        self.table_widget_property_set.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_property_set.horizontalHeader().setStretchLastSection(True)
        self.table_widget_property_set.verticalHeader().setVisible(False)
        self.table_widget_property_set.verticalHeader().setProperty("showSortIndicator", False)
        self.table_widget_property_set.verticalHeader().setStretchLastSection(False)
        self.table_widget_attribute = QTableWidget(self.splitter_lists)
        if (self.table_widget_attribute.columnCount() < 3):
            self.table_widget_attribute.setColumnCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget_attribute.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget_attribute.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget_attribute.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        self.table_widget_attribute.setObjectName(u"table_widget_attribute")
        self.splitter_lists.addWidget(self.table_widget_attribute)
        self.table_widget_attribute.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_attribute.horizontalHeader().setStretchLastSection(True)
        self.table_widget_attribute.verticalHeader().setVisible(False)
        self.table_widget_attribute.verticalHeader().setProperty("showSortIndicator", False)
        self.table_widget_attribute.verticalHeader().setStretchLastSection(False)
        self.table_widget_value = QTableWidget(self.splitter_lists)
        if (self.table_widget_value.columnCount() < 2):
            self.table_widget_value.setColumnCount(2)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget_value.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_widget_value.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        self.table_widget_value.setObjectName(u"table_widget_value")
        self.splitter_lists.addWidget(self.table_widget_value)
        self.table_widget_value.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_value.horizontalHeader().setStretchLastSection(True)
        self.table_widget_value.verticalHeader().setVisible(False)
        self.table_widget_value.verticalHeader().setProperty("showSortIndicator", False)
        self.table_widget_value.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.splitter_lists)

        self.horzontal_layout_action_buttons = QHBoxLayout()
        self.horzontal_layout_action_buttons.setObjectName(u"horzontal_layout_action_buttons")
        self.horizontal_spacer_action_buttons = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horzontal_layout_action_buttons.addItem(self.horizontal_spacer_action_buttons)

        self.button_abort = QPushButton(Form)
        self.button_abort.setObjectName(u"button_abort")

        self.horzontal_layout_action_buttons.addWidget(self.button_abort)

        self.button_run = QPushButton(Form)
        self.button_run.setObjectName(u"button_run")

        self.horzontal_layout_action_buttons.addWidget(self.button_run)


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
        self.label_status.setText(QCoreApplication.translate("Form", u"IFC Pfad fehlt!", None))
        self.button_last.setText(QCoreApplication.translate("Form", u"Zur\u00fcck", None))
        self.label_object_name.setText(QCoreApplication.translate("Form", u"ObjectName", None))
        self.button_next.setText(QCoreApplication.translate("Form", u"N\u00e4chstes Objekt", None))
        ___qtablewidgetitem = self.table_widget_property_set.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"PropertySet", None));
        ___qtablewidgetitem1 = self.table_widget_property_set.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Anzahl", None));
        ___qtablewidgetitem2 = self.table_widget_attribute.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Attribut", None));
        ___qtablewidgetitem3 = self.table_widget_attribute.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Anzahl", None));
        ___qtablewidgetitem4 = self.table_widget_attribute.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Eindeutig", None));
        ___qtablewidgetitem5 = self.table_widget_value.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Wert", None));
        ___qtablewidgetitem6 = self.table_widget_value.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Anzahl", None));
        self.button_abort.setText(QCoreApplication.translate("Form", u"Abbrechen", None))
        self.button_run.setText(QCoreApplication.translate("Form", u"IFC Einlesen", None))
    # retranslateUi

