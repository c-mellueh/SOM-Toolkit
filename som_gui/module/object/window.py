# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ObjectInfoWidget.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ObjectInfo(object):
    def setupUi(self, ObjectInfo):
        if not ObjectInfo.objectName():
            ObjectInfo.setObjectName(u"ObjectInfo")
        ObjectInfo.resize(782, 196)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ObjectInfo.sizePolicy().hasHeightForWidth())
        ObjectInfo.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ObjectInfo)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontal_layout_info = QHBoxLayout()
        self.horizontal_layout_info.setObjectName(u"horizontal_layout_info")
        self.label_name = QLabel(ObjectInfo)
        self.label_name.setObjectName(u"label_name")

        self.horizontal_layout_info.addWidget(self.label_name)

        self.line_edit_name = QLineEdit(ObjectInfo)
        self.line_edit_name.setObjectName(u"line_edit_name")

        self.horizontal_layout_info.addWidget(self.line_edit_name)

        self.label_abbreviation = QLabel(ObjectInfo)
        self.label_abbreviation.setObjectName(u"label_abbreviation")

        self.horizontal_layout_info.addWidget(self.label_abbreviation)

        self.line_edit_abbreviation = QLineEdit(ObjectInfo)
        self.line_edit_abbreviation.setObjectName(u"line_edit_abbreviation")

        self.horizontal_layout_info.addWidget(self.line_edit_abbreviation)


        self.verticalLayout.addLayout(self.horizontal_layout_info)

        self.button_gruppe = QRadioButton(ObjectInfo)
        self.button_gruppe.setObjectName(u"button_gruppe")

        self.verticalLayout.addWidget(self.button_gruppe)

        self.layout_ident_attribute = QHBoxLayout()
        self.layout_ident_attribute.setObjectName(u"layout_ident_attribute")
        self.combo_box_pset = QComboBox(ObjectInfo)
        self.combo_box_pset.setObjectName(u"combo_box_pset")

        self.layout_ident_attribute.addWidget(self.combo_box_pset)

        self.combo_box_attribute = QComboBox(ObjectInfo)
        self.combo_box_attribute.setObjectName(u"combo_box_attribute")

        self.layout_ident_attribute.addWidget(self.combo_box_attribute)

        self.line_edit_attribute_value = QLineEdit(ObjectInfo)
        self.line_edit_attribute_value.setObjectName(u"line_edit_attribute_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_attribute_value.sizePolicy().hasHeightForWidth())
        self.line_edit_attribute_value.setSizePolicy(sizePolicy1)

        self.layout_ident_attribute.addWidget(self.line_edit_attribute_value)


        self.verticalLayout.addLayout(self.layout_ident_attribute)

        self.horizontal_layout_ifc = QHBoxLayout()
        self.horizontal_layout_ifc.setObjectName(u"horizontal_layout_ifc")
        self.label_ifc_mapping = QLabel(ObjectInfo)
        self.label_ifc_mapping.setObjectName(u"label_ifc_mapping")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_ifc_mapping.sizePolicy().hasHeightForWidth())
        self.label_ifc_mapping.setSizePolicy(sizePolicy2)

        self.horizontal_layout_ifc.addWidget(self.label_ifc_mapping)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontal_layout_ifc.addItem(self.horizontal_spacer)

        self.button_add_ifc = QPushButton(ObjectInfo)
        self.button_add_ifc.setObjectName(u"button_add_ifc")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_add_ifc.sizePolicy().hasHeightForWidth())
        self.button_add_ifc.setSizePolicy(sizePolicy3)

        self.horizontal_layout_ifc.addWidget(self.button_add_ifc)


        self.verticalLayout.addLayout(self.horizontal_layout_ifc)

        self.vertical_layout_ifc = QVBoxLayout()
        self.vertical_layout_ifc.setObjectName(u"vertical_layout_ifc")

        self.verticalLayout.addLayout(self.vertical_layout_ifc)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.vertical_spacer)

        self.button_box = QDialogButtonBox(ObjectInfo)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.button_box)

        QWidget.setTabOrder(self.line_edit_name, self.line_edit_abbreviation)
        QWidget.setTabOrder(self.line_edit_abbreviation, self.button_add_ifc)

        self.retranslateUi(ObjectInfo)
        self.button_box.accepted.connect(ObjectInfo.accept)
        self.button_box.rejected.connect(ObjectInfo.reject)

        QMetaObject.connectSlotsByName(ObjectInfo)
    # setupUi

    def retranslateUi(self, ObjectInfo):
        ObjectInfo.setWindowTitle(QCoreApplication.translate("ObjectInfo", u"Dialog", None))
        self.label_name.setText(QCoreApplication.translate("ObjectInfo", u"Name", None))
        self.label_abbreviation.setText(QCoreApplication.translate("ObjectInfo", u"Abk\u00fcrzung:", None))
        self.button_gruppe.setText(QCoreApplication.translate("ObjectInfo", u"Gruppe", None))
        self.label_ifc_mapping.setText(QCoreApplication.translate("ObjectInfo", u"IFC Mapping", None))
        self.button_add_ifc.setText(QCoreApplication.translate("ObjectInfo", u"+", None))
    # retranslateUi

