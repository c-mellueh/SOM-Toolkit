# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AttributeImport.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1104, 568)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(30, 100))
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.splitter_attribute = QSplitter(Form)
        self.splitter_attribute.setObjectName(u"splitter_attribute")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter_attribute.sizePolicy().hasHeightForWidth())
        self.splitter_attribute.setSizePolicy(sizePolicy1)
        self.splitter_attribute.setOrientation(Qt.Horizontal)
        self.line_edit_ident_pset = QLineEdit(self.splitter_attribute)
        self.line_edit_ident_pset.setObjectName(u"line_edit_ident_pset")
        self.splitter_attribute.addWidget(self.line_edit_ident_pset)
        self.line_edit_ident_attribute = QLineEdit(self.splitter_attribute)
        self.line_edit_ident_attribute.setObjectName(u"line_edit_ident_attribute")
        self.splitter_attribute.addWidget(self.line_edit_ident_attribute)

        self.verticalLayout_3.addWidget(self.splitter_attribute)

        self.label_ifc = QLabel(Form)
        self.label_ifc.setObjectName(u"label_ifc")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_ifc.sizePolicy().hasHeightForWidth())
        self.label_ifc.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.label_ifc)

        self.horizontal_layout_ifc = QHBoxLayout()
        self.horizontal_layout_ifc.setObjectName(u"horizontal_layout_ifc")
        self.line_edit_ifc = QLineEdit(Form)
        self.line_edit_ifc.setObjectName(u"line_edit_ifc")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line_edit_ifc.sizePolicy().hasHeightForWidth())
        self.line_edit_ifc.setSizePolicy(sizePolicy3)

        self.horizontal_layout_ifc.addWidget(self.line_edit_ifc)

        self.button_ifc = QPushButton(Form)
        self.button_ifc.setObjectName(u"button_ifc")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.button_ifc.sizePolicy().hasHeightForWidth())
        self.button_ifc.setSizePolicy(sizePolicy4)
        self.button_ifc.setMaximumSize(QSize(25, 16777215))

        self.horizontal_layout_ifc.addWidget(self.button_ifc)


        self.verticalLayout_3.addLayout(self.horizontal_layout_ifc)

        self.label_status = QLabel(Form)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy5)
        self.label_status.setTextFormat(Qt.PlainText)

        self.verticalLayout_3.addWidget(self.label_status)

        self.progress_bar = QProgressBar(Form)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setEnabled(True)
        self.progress_bar.setValue(0)

        self.verticalLayout_3.addWidget(self.progress_bar)

        self.horizontal_layout_buttons = QHBoxLayout()
        self.horizontal_layout_buttons.setObjectName(u"horizontal_layout_buttons")
        self.horizontal_layout_buttons.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.combo_box_group = QComboBox(Form)
        self.combo_box_group.setObjectName(u"combo_box_group")

        self.horizontal_layout_buttons.addWidget(self.combo_box_group)

        self.combo_box_name = QComboBox(Form)
        self.combo_box_name.setObjectName(u"combo_box_name")

        self.horizontal_layout_buttons.addWidget(self.combo_box_name)

        self.label_object_count = QLabel(Form)
        self.label_object_count.setObjectName(u"label_object_count")
        sizePolicy5.setHeightForWidth(self.label_object_count.sizePolicy().hasHeightForWidth())
        self.label_object_count.setSizePolicy(sizePolicy5)
        self.label_object_count.setMinimumSize(QSize(0, 24))
        self.label_object_count.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_buttons.addWidget(self.label_object_count)


        self.verticalLayout_3.addLayout(self.horizontal_layout_buttons)

        self.splitter_tables = QSplitter(Form)
        self.splitter_tables.setObjectName(u"splitter_tables")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.splitter_tables.sizePolicy().hasHeightForWidth())
        self.splitter_tables.setSizePolicy(sizePolicy6)
        self.splitter_tables.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget_3 = QWidget(self.splitter_tables)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.vertival_layout_pset = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vertival_layout_pset.setObjectName(u"vertival_layout_pset")
        self.vertival_layout_pset.setContentsMargins(0, 0, 0, 0)
        self.label_proeprty_sets = QLabel(self.verticalLayoutWidget_3)
        self.label_proeprty_sets.setObjectName(u"label_proeprty_sets")
        sizePolicy5.setHeightForWidth(self.label_proeprty_sets.sizePolicy().hasHeightForWidth())
        self.label_proeprty_sets.setSizePolicy(sizePolicy5)
        self.label_proeprty_sets.setMinimumSize(QSize(0, 24))
        self.label_proeprty_sets.setAlignment(Qt.AlignCenter)

        self.vertival_layout_pset.addWidget(self.label_proeprty_sets)

        self.table_widget_property_set = QTableWidget(self.verticalLayoutWidget_3)
        if (self.table_widget_property_set.columnCount() < 2):
            self.table_widget_property_set.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget_property_set.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget_property_set.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table_widget_property_set.setObjectName(u"table_widget_property_set")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.table_widget_property_set.sizePolicy().hasHeightForWidth())
        self.table_widget_property_set.setSizePolicy(sizePolicy7)
        self.table_widget_property_set.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget_property_set.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_property_set.horizontalHeader().setMinimumSectionSize(30)
        self.table_widget_property_set.horizontalHeader().setDefaultSectionSize(100)
        self.table_widget_property_set.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_property_set.horizontalHeader().setStretchLastSection(True)
        self.table_widget_property_set.verticalHeader().setVisible(False)
        self.table_widget_property_set.verticalHeader().setProperty("showSortIndicator", False)
        self.table_widget_property_set.verticalHeader().setStretchLastSection(False)

        self.vertival_layout_pset.addWidget(self.table_widget_property_set)

        self.splitter_tables.addWidget(self.verticalLayoutWidget_3)
        self.verticalLayoutWidget_2 = QWidget(self.splitter_tables)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.vertical_layout_attribute = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vertical_layout_attribute.setObjectName(u"vertical_layout_attribute")
        self.vertical_layout_attribute.setContentsMargins(0, 0, 0, 0)
        self.label_attributes = QLabel(self.verticalLayoutWidget_2)
        self.label_attributes.setObjectName(u"label_attributes")
        sizePolicy5.setHeightForWidth(self.label_attributes.sizePolicy().hasHeightForWidth())
        self.label_attributes.setSizePolicy(sizePolicy5)
        self.label_attributes.setMinimumSize(QSize(0, 24))
        self.label_attributes.setAlignment(Qt.AlignCenter)

        self.vertical_layout_attribute.addWidget(self.label_attributes)

        self.table_widget_attribute = QTableWidget(self.verticalLayoutWidget_2)
        if (self.table_widget_attribute.columnCount() < 3):
            self.table_widget_attribute.setColumnCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget_attribute.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget_attribute.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget_attribute.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        self.table_widget_attribute.setObjectName(u"table_widget_attribute")
        sizePolicy7.setHeightForWidth(self.table_widget_attribute.sizePolicy().hasHeightForWidth())
        self.table_widget_attribute.setSizePolicy(sizePolicy7)
        self.table_widget_attribute.setAutoScroll(False)
        self.table_widget_attribute.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget_attribute.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_attribute.horizontalHeader().setCascadingSectionResizes(True)
        self.table_widget_attribute.horizontalHeader().setMinimumSectionSize(20)
        self.table_widget_attribute.horizontalHeader().setDefaultSectionSize(50)
        self.table_widget_attribute.horizontalHeader().setHighlightSections(True)
        self.table_widget_attribute.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_attribute.horizontalHeader().setStretchLastSection(True)
        self.table_widget_attribute.verticalHeader().setVisible(False)
        self.table_widget_attribute.verticalHeader().setProperty("showSortIndicator", False)
        self.table_widget_attribute.verticalHeader().setStretchLastSection(False)

        self.vertical_layout_attribute.addWidget(self.table_widget_attribute)

        self.splitter_tables.addWidget(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget = QWidget(self.splitter_tables)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vertical_layout_value = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_value.setObjectName(u"vertical_layout_value")
        self.vertical_layout_value.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.check_box_values = QCheckBox(self.verticalLayoutWidget)
        self.check_box_values.setObjectName(u"check_box_values")
        self.check_box_values.setMinimumSize(QSize(0, 24))
        self.check_box_values.setMaximumSize(QSize(16777215, 24))
        self.check_box_values.setChecked(True)

        self.horizontalLayout_2.addWidget(self.check_box_values)

        self.label_value = QLabel(self.verticalLayoutWidget)
        self.label_value.setObjectName(u"label_value")
        sizePolicy5.setHeightForWidth(self.label_value.sizePolicy().hasHeightForWidth())
        self.label_value.setSizePolicy(sizePolicy5)
        self.label_value.setMinimumSize(QSize(0, 24))
        self.label_value.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout_2.addWidget(self.label_value)


        self.vertical_layout_value.addLayout(self.horizontalLayout_2)

        self.table_widget_value = QTableWidget(self.verticalLayoutWidget)
        if (self.table_widget_value.columnCount() < 2):
            self.table_widget_value.setColumnCount(2)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget_value.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_widget_value.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        self.table_widget_value.setObjectName(u"table_widget_value")
        sizePolicy6.setHeightForWidth(self.table_widget_value.sizePolicy().hasHeightForWidth())
        self.table_widget_value.setSizePolicy(sizePolicy6)
        self.table_widget_value.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget_value.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_value.horizontalHeader().setMinimumSectionSize(30)
        self.table_widget_value.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_value.horizontalHeader().setStretchLastSection(True)
        self.table_widget_value.verticalHeader().setVisible(False)

        self.vertical_layout_value.addWidget(self.table_widget_value)

        self.splitter_tables.addWidget(self.verticalLayoutWidget)

        self.verticalLayout_3.addWidget(self.splitter_tables)

        self.horzontal_layout_action_buttons = QHBoxLayout()
        self.horzontal_layout_action_buttons.setObjectName(u"horzontal_layout_action_buttons")
        self.button_settings = QPushButton(Form)
        self.button_settings.setObjectName(u"button_settings")
        self.button_settings.setMinimumSize(QSize(24, 24))
        self.button_settings.setMaximumSize(QSize(24, 24))

        self.horzontal_layout_action_buttons.addWidget(self.button_settings)

        self.horizontal_spacer_action_buttons = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horzontal_layout_action_buttons.addItem(self.horizontal_spacer_action_buttons)

        self.button_abort = QPushButton(Form)
        self.button_abort.setObjectName(u"button_abort")
        self.button_abort.setMinimumSize(QSize(0, 24))
        self.button_abort.setMaximumSize(QSize(16777215, 24))

        self.horzontal_layout_action_buttons.addWidget(self.button_abort)

        self.button_run = QPushButton(Form)
        self.button_run.setObjectName(u"button_run")
        self.button_run.setMinimumSize(QSize(0, 24))
        self.button_run.setMaximumSize(QSize(16777215, 24))

        self.horzontal_layout_action_buttons.addWidget(self.button_run)


        self.verticalLayout_3.addLayout(self.horzontal_layout_action_buttons)


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
        self.label_object_count.setText(QCoreApplication.translate("Form", u"Anzahl", None))
        self.label_proeprty_sets.setText(QCoreApplication.translate("Form", u"PropertySets", None))
        ___qtablewidgetitem = self.table_widget_property_set.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"PropertySet", None));
        ___qtablewidgetitem1 = self.table_widget_property_set.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Anzahl", None));
        self.label_attributes.setText(QCoreApplication.translate("Form", u"Attribute", None))
        ___qtablewidgetitem2 = self.table_widget_attribute.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Attribut", None));
        ___qtablewidgetitem3 = self.table_widget_attribute.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Anzahl", None));
        ___qtablewidgetitem4 = self.table_widget_attribute.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Eindeutig", None));
        self.check_box_values.setText(QCoreApplication.translate("Form", u"Alle", None))
        self.label_value.setText(QCoreApplication.translate("Form", u"Werte", None))
        ___qtablewidgetitem5 = self.table_widget_value.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Wert", None));
        ___qtablewidgetitem6 = self.table_widget_value.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Anzahl", None));
        self.button_settings.setText("")
        self.button_abort.setText(QCoreApplication.translate("Form", u"Abbrechen", None))
        self.button_run.setText(QCoreApplication.translate("Form", u"IFC Einlesen", None))
    # retranslateUi

