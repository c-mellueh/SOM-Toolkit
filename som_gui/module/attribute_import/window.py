# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AttributeImport.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
                               QPushButton, QSizePolicy, QSpacerItem, QSplitter,
                               QTableView, QVBoxLayout, QWidget)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1073, 440)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(0, 0))
        self.main_layout = QVBoxLayout(Form)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_object_count.sizePolicy().hasHeightForWidth())
        self.label_object_count.setSizePolicy(sizePolicy1)
        self.label_object_count.setMinimumSize(QSize(0, 24))
        self.label_object_count.setAlignment(Qt.AlignCenter)

        self.horizontal_layout_buttons.addWidget(self.label_object_count)

        self.main_layout.addLayout(self.horizontal_layout_buttons)

        self.splitter_tables = QSplitter(Form)
        self.splitter_tables.setObjectName(u"splitter_tables")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter_tables.sizePolicy().hasHeightForWidth())
        self.splitter_tables.setSizePolicy(sizePolicy2)
        self.splitter_tables.setOrientation(Qt.Horizontal)
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
        self.label_proeprty_sets.setAlignment(Qt.AlignCenter)

        self.vertival_layout_pset.addWidget(self.label_proeprty_sets)

        self.table_widget_property_set = QTableView(self.verticalLayoutWidget_3)
        self.table_widget_property_set.setObjectName(u"table_widget_property_set")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.table_widget_property_set.sizePolicy().hasHeightForWidth())
        self.table_widget_property_set.setSizePolicy(sizePolicy3)
        self.table_widget_property_set.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_widget_property_set.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_widget_property_set.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget_property_set.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_property_set.horizontalHeader().setMinimumSectionSize(25)
        self.table_widget_property_set.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_property_set.horizontalHeader().setStretchLastSection(True)
        self.table_widget_property_set.verticalHeader().setVisible(False)
        self.table_widget_property_set.verticalHeader().setCascadingSectionResizes(True)
        self.table_widget_property_set.verticalHeader().setDefaultSectionSize(24)
        self.table_widget_property_set.verticalHeader().setProperty("showSortIndicator", False)

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
        self.label_attributes.setAlignment(Qt.AlignCenter)

        self.vertical_layout_attribute.addWidget(self.label_attributes)

        self.table_widget_attribute = QTableView(self.verticalLayoutWidget_2)
        self.table_widget_attribute.setObjectName(u"table_widget_attribute")
        sizePolicy3.setHeightForWidth(self.table_widget_attribute.sizePolicy().hasHeightForWidth())
        self.table_widget_attribute.setSizePolicy(sizePolicy3)
        self.table_widget_attribute.setAutoScroll(False)
        self.table_widget_attribute.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget_attribute.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_attribute.horizontalHeader().setMinimumSectionSize(50)
        self.table_widget_attribute.horizontalHeader().setHighlightSections(True)
        self.table_widget_attribute.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget_attribute.horizontalHeader().setStretchLastSection(True)
        self.table_widget_attribute.verticalHeader().setVisible(False)
        self.table_widget_attribute.verticalHeader().setCascadingSectionResizes(True)
        self.table_widget_attribute.verticalHeader().setDefaultSectionSize(24)

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
        self.check_box_values.setEnabled(False)
        self.check_box_values.setMinimumSize(QSize(0, 24))
        self.check_box_values.setMaximumSize(QSize(16777215, 24))
        self.check_box_values.setChecked(False)

        self.horizontalLayout_2.addWidget(self.check_box_values)

        self.label_value = QLabel(self.verticalLayoutWidget)
        self.label_value.setObjectName(u"label_value")
        sizePolicy1.setHeightForWidth(self.label_value.sizePolicy().hasHeightForWidth())
        self.label_value.setSizePolicy(sizePolicy1)
        self.label_value.setMinimumSize(QSize(0, 24))
        self.label_value.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout_2.addWidget(self.label_value)

        self.vertical_layout_value.addLayout(self.horizontalLayout_2)

        self.table_widget_value = QTableView(self.verticalLayoutWidget)
        self.table_widget_value.setObjectName(u"table_widget_value")
        sizePolicy2.setHeightForWidth(self.table_widget_value.sizePolicy().hasHeightForWidth())
        self.table_widget_value.setSizePolicy(sizePolicy2)
        self.table_widget_value.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget_value.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget_value.horizontalHeader().setStretchLastSection(True)
        self.table_widget_value.verticalHeader().setVisible(False)
        self.table_widget_value.verticalHeader().setCascadingSectionResizes(True)
        self.table_widget_value.verticalHeader().setDefaultSectionSize(24)

        self.vertical_layout_value.addWidget(self.table_widget_value)

        self.splitter_tables.addWidget(self.verticalLayoutWidget)

        self.main_layout.addWidget(self.splitter_tables)

        self.horzontal_layout_action_buttons = QHBoxLayout()
        self.horzontal_layout_action_buttons.setObjectName(u"horzontal_layout_action_buttons")
        self.button_settings = QPushButton(Form)
        self.button_settings.setObjectName(u"button_settings")
        self.button_settings.setMinimumSize(QSize(24, 24))
        self.button_settings.setMaximumSize(QSize(24, 24))

        self.horzontal_layout_action_buttons.addWidget(self.button_settings)

        self.horizontal_spacer_action_buttons = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                                            QSizePolicy.Policy.Minimum)

        self.horzontal_layout_action_buttons.addItem(self.horizontal_spacer_action_buttons)

        self.button_abort = QPushButton(Form)
        self.button_abort.setObjectName(u"button_abort")
        self.button_abort.setMinimumSize(QSize(0, 24))
        self.button_abort.setMaximumSize(QSize(16777215, 24))

        self.horzontal_layout_action_buttons.addWidget(self.button_abort)

        self.button_accept = QPushButton(Form)
        self.button_accept.setObjectName(u"button_accept")

        self.horzontal_layout_action_buttons.addWidget(self.button_accept)

        self.button_run = QPushButton(Form)
        self.button_run.setObjectName(u"button_run")
        self.button_run.setMinimumSize(QSize(0, 24))
        self.button_run.setMaximumSize(QSize(16777215, 24))

        self.horzontal_layout_action_buttons.addWidget(self.button_run)

        self.main_layout.addLayout(self.horzontal_layout_action_buttons)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_object_count.setText(QCoreApplication.translate("Form", u"Anzahl", None))
        self.label_proeprty_sets.setText(QCoreApplication.translate("Form", u"PropertySets", None))
        self.label_attributes.setText(QCoreApplication.translate("Form", u"Attribute", None))
        self.check_box_values.setText(QCoreApplication.translate("Form", u"Alle", None))
        self.label_value.setText(QCoreApplication.translate("Form", u"Werte", None))
        self.button_settings.setText("")
        self.button_abort.setText(QCoreApplication.translate("Form", u"Abbrechen", None))
        self.button_accept.setText(QCoreApplication.translate("Form", u"Werte \u00dcbernehmen", None))
        self.button_run.setText(QCoreApplication.translate("Form", u"IFC Einlesen", None))
    # retranslateUi
