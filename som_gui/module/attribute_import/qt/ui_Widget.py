# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QPushButton, QSizePolicy, QSplitter,
    QTableWidgetItem, QVBoxLayout, QWidget)

from som_gui.module.attribute_import.ui import (AttributeTable, IfcTypeComboBox, PropertySetTable, SOMTypeComboBox,
    ValueTable)

class Ui_AttributeImport(object):
    def setupUi(self, AttributeImport):
        if not AttributeImport.objectName():
            AttributeImport.setObjectName(u"AttributeImport")
        AttributeImport.resize(1383, 831)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AttributeImport.sizePolicy().hasHeightForWidth())
        AttributeImport.setSizePolicy(sizePolicy)
        AttributeImport.setMinimumSize(QSize(0, 0))
        self.main_layout = QVBoxLayout(AttributeImport)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.horizontal_layout_buttons = QHBoxLayout()
        self.horizontal_layout_buttons.setObjectName(u"horizontal_layout_buttons")
        self.horizontal_layout_buttons.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.combo_box_ifc_type = IfcTypeComboBox(AttributeImport)
        self.combo_box_ifc_type.setObjectName(u"combo_box_ifc_type")

        self.horizontal_layout_buttons.addWidget(self.combo_box_ifc_type)

        self.combo_box_identifier = SOMTypeComboBox(AttributeImport)
        self.combo_box_identifier.setObjectName(u"combo_box_identifier")

        self.horizontal_layout_buttons.addWidget(self.combo_box_identifier)

        self.label_object_count = QLabel(AttributeImport)
        self.label_object_count.setObjectName(u"label_object_count")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_object_count.sizePolicy().hasHeightForWidth())
        self.label_object_count.setSizePolicy(sizePolicy1)
        self.label_object_count.setMinimumSize(QSize(0, 24))
        self.label_object_count.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontal_layout_buttons.addWidget(self.label_object_count)


        self.main_layout.addLayout(self.horizontal_layout_buttons)

        self.splitter_tables = QSplitter(AttributeImport)
        self.splitter_tables.setObjectName(u"splitter_tables")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter_tables.sizePolicy().hasHeightForWidth())
        self.splitter_tables.setSizePolicy(sizePolicy2)
        self.splitter_tables.setOrientation(Qt.Orientation.Horizontal)
        self.verticalLayoutWidget_3 = QWidget(self.splitter_tables)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.vertival_layout_pset = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vertival_layout_pset.setObjectName(u"vertival_layout_pset")
        self.vertival_layout_pset.setContentsMargins(0, 0, 0, 0)
        self.label_proeprty_sets = QLabel(self.verticalLayoutWidget_3)
        self.label_proeprty_sets.setObjectName(u"label_proeprty_sets")
        sizePolicy1.setHeightForWidth(self.label_proeprty_sets.sizePolicy().hasHeightForWidth())
        self.label_proeprty_sets.setSizePolicy(sizePolicy1)
        self.label_proeprty_sets.setMinimumSize(QSize(0, 24))
        self.label_proeprty_sets.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vertival_layout_pset.addWidget(self.label_proeprty_sets)

        self.table_widget_property_set = PropertySetTable(self.verticalLayoutWidget_3)
        self.table_widget_property_set.setObjectName(u"table_widget_property_set")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.table_widget_property_set.sizePolicy().hasHeightForWidth())
        self.table_widget_property_set.setSizePolicy(sizePolicy3)
        self.table_widget_property_set.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table_widget_property_set.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table_widget_property_set.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget_property_set.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_widget_property_set.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget_property_set.horizontalHeader().setMinimumSectionSize(1)
        self.table_widget_property_set.horizontalHeader().setDefaultSectionSize(39)
        self.table_widget_property_set.horizontalHeader().setHighlightSections(True)
        self.table_widget_property_set.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.table_widget_property_set.horizontalHeader().setStretchLastSection(True)
        self.table_widget_property_set.verticalHeader().setVisible(False)
        self.table_widget_property_set.verticalHeader().setHighlightSections(False)

        self.vertival_layout_pset.addWidget(self.table_widget_property_set)

        self.splitter_tables.addWidget(self.verticalLayoutWidget_3)
        self.verticalLayoutWidget_2 = QWidget(self.splitter_tables)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.vertical_layout_attribute = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vertical_layout_attribute.setObjectName(u"vertical_layout_attribute")
        self.vertical_layout_attribute.setContentsMargins(0, 0, 0, 0)
        self.label_attributes = QLabel(self.verticalLayoutWidget_2)
        self.label_attributes.setObjectName(u"label_attributes")
        sizePolicy1.setHeightForWidth(self.label_attributes.sizePolicy().hasHeightForWidth())
        self.label_attributes.setSizePolicy(sizePolicy1)
        self.label_attributes.setMinimumSize(QSize(0, 24))
        self.label_attributes.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vertical_layout_attribute.addWidget(self.label_attributes)

        self.table_widget_attribute = AttributeTable(self.verticalLayoutWidget_2)
        self.table_widget_attribute.setObjectName(u"table_widget_attribute")
        sizePolicy3.setHeightForWidth(self.table_widget_attribute.sizePolicy().hasHeightForWidth())
        self.table_widget_attribute.setSizePolicy(sizePolicy3)
        self.table_widget_attribute.setAutoScroll(False)
        self.table_widget_attribute.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget_attribute.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_widget_attribute.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget_attribute.horizontalHeader().setCascadingSectionResizes(True)
        self.table_widget_attribute.horizontalHeader().setMinimumSectionSize(1)
        self.table_widget_attribute.horizontalHeader().setDefaultSectionSize(50)
        self.table_widget_attribute.horizontalHeader().setHighlightSections(True)
        self.table_widget_attribute.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.table_widget_attribute.horizontalHeader().setStretchLastSection(True)
        self.table_widget_attribute.verticalHeader().setVisible(False)

        self.vertical_layout_attribute.addWidget(self.table_widget_attribute)

        self.splitter_tables.addWidget(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget = QWidget(self.splitter_tables)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.vertical_layout_value = QVBoxLayout(self.verticalLayoutWidget)
        self.vertical_layout_value.setObjectName(u"vertical_layout_value")
        self.vertical_layout_value.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.check_box_values = QCheckBox(self.verticalLayoutWidget)
        self.check_box_values.setObjectName(u"check_box_values")
        self.check_box_values.setEnabled(True)
        self.check_box_values.setMinimumSize(QSize(0, 24))
        self.check_box_values.setMaximumSize(QSize(16777215, 24))
        self.check_box_values.setChecked(False)
        self.check_box_values.setTristate(False)

        self.horizontalLayout_2.addWidget(self.check_box_values)

        self.label_value = QLabel(self.verticalLayoutWidget)
        self.label_value.setObjectName(u"label_value")
        sizePolicy1.setHeightForWidth(self.label_value.sizePolicy().hasHeightForWidth())
        self.label_value.setSizePolicy(sizePolicy1)
        self.label_value.setMinimumSize(QSize(0, 24))
        self.label_value.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout_2.addWidget(self.label_value)


        self.vertical_layout_value.addLayout(self.horizontalLayout_2)

        self.table_widget_value = ValueTable(self.verticalLayoutWidget)
        self.table_widget_value.setObjectName(u"table_widget_value")
        sizePolicy2.setHeightForWidth(self.table_widget_value.sizePolicy().hasHeightForWidth())
        self.table_widget_value.setSizePolicy(sizePolicy2)
        self.table_widget_value.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget_value.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget_value.horizontalHeader().setMinimumSectionSize(1)
        self.table_widget_value.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.table_widget_value.horizontalHeader().setStretchLastSection(True)
        self.table_widget_value.verticalHeader().setVisible(False)

        self.vertical_layout_value.addWidget(self.table_widget_value)

        self.splitter_tables.addWidget(self.verticalLayoutWidget)

        self.main_layout.addWidget(self.splitter_tables)

        self.horzontal_layout_action_buttons = QHBoxLayout()
        self.horzontal_layout_action_buttons.setObjectName(u"horzontal_layout_action_buttons")
        self.button_settings = QPushButton(AttributeImport)
        self.button_settings.setObjectName(u"button_settings")
        self.button_settings.setMinimumSize(QSize(24, 24))
        self.button_settings.setMaximumSize(QSize(24, 24))

        self.horzontal_layout_action_buttons.addWidget(self.button_settings)

        self.button_download = QPushButton(AttributeImport)
        self.button_download.setObjectName(u"button_download")
        self.button_download.setMaximumSize(QSize(24, 24))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.button_download.setIcon(icon)

        self.horzontal_layout_action_buttons.addWidget(self.button_download)

        self.buttonBox = QDialogButtonBox(AttributeImport)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horzontal_layout_action_buttons.addWidget(self.buttonBox)


        self.main_layout.addLayout(self.horzontal_layout_action_buttons)


        self.retranslateUi(AttributeImport)

        QMetaObject.connectSlotsByName(AttributeImport)
    # setupUi

    def retranslateUi(self, AttributeImport):
        AttributeImport.setWindowTitle(QCoreApplication.translate("AttributeImport", u"Form", None))
        self.label_object_count.setText(QCoreApplication.translate("AttributeImport", u"Count", None))
        self.label_proeprty_sets.setText(QCoreApplication.translate("AttributeImport", u"PropertySets", None))
        self.label_attributes.setText(QCoreApplication.translate("AttributeImport", u"Attribute", None))
        self.check_box_values.setText(QCoreApplication.translate("AttributeImport", u"All", None))
        self.label_value.setText(QCoreApplication.translate("AttributeImport", u"Values", None))
        self.button_settings.setText("")
        self.button_download.setText("")
    # retranslateUi

