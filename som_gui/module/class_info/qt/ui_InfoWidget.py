# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InfoWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
    QRadioButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_ClassInfo(object):
    def setupUi(self, ClassInfo):
        if not ClassInfo.objectName():
            ClassInfo.setObjectName(u"ClassInfo")
        ClassInfo.resize(881, 309)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClassInfo.sizePolicy().hasHeightForWidth())
        ClassInfo.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ClassInfo)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontal_layout_info = QHBoxLayout()
        self.horizontal_layout_info.setObjectName(u"horizontal_layout_info")
        self.label_name = QLabel(ClassInfo)
        self.label_name.setObjectName(u"label_name")

        self.horizontal_layout_info.addWidget(self.label_name)

        self.line_edit_name = QLineEdit(ClassInfo)
        self.line_edit_name.setObjectName(u"line_edit_name")

        self.horizontal_layout_info.addWidget(self.line_edit_name)


        self.verticalLayout.addLayout(self.horizontal_layout_info)

        self.horizontal_layout_group = QHBoxLayout()
        self.horizontal_layout_group.setObjectName(u"horizontal_layout_group")
        self.button_gruppe = QRadioButton(ClassInfo)
        self.button_gruppe.setObjectName(u"button_gruppe")

        self.horizontal_layout_group.addWidget(self.button_gruppe)


        self.verticalLayout.addLayout(self.horizontal_layout_group)

        self.layout_ident_property = QHBoxLayout()
        self.layout_ident_property.setObjectName(u"layout_ident_property")
        self.combo_box_pset = QComboBox(ClassInfo)
        self.combo_box_pset.setObjectName(u"combo_box_pset")
        self.combo_box_pset.setEditable(True)

        self.layout_ident_property.addWidget(self.combo_box_pset)

        self.combo_box_property = QComboBox(ClassInfo)
        self.combo_box_property.setObjectName(u"combo_box_property")
        self.combo_box_property.setEditable(True)

        self.layout_ident_property.addWidget(self.combo_box_property)

        self.line_edit_property_value = QLineEdit(ClassInfo)
        self.line_edit_property_value.setObjectName(u"line_edit_property_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_property_value.sizePolicy().hasHeightForWidth())
        self.line_edit_property_value.setSizePolicy(sizePolicy1)

        self.layout_ident_property.addWidget(self.line_edit_property_value)


        self.verticalLayout.addLayout(self.layout_ident_property)

        self.vertical_layout_ifc = QVBoxLayout()
        self.vertical_layout_ifc.setObjectName(u"vertical_layout_ifc")

        self.verticalLayout.addLayout(self.vertical_layout_ifc)

        self.text_edit_description = QTextEdit(ClassInfo)
        self.text_edit_description.setObjectName(u"text_edit_description")

        self.verticalLayout.addWidget(self.text_edit_description)

        self.button_box = QDialogButtonBox(ClassInfo)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)

        QWidget.setTabOrder(self.line_edit_name, self.button_gruppe)
        QWidget.setTabOrder(self.button_gruppe, self.combo_box_pset)
        QWidget.setTabOrder(self.combo_box_pset, self.combo_box_property)
        QWidget.setTabOrder(self.combo_box_property, self.line_edit_property_value)
        QWidget.setTabOrder(self.line_edit_property_value, self.text_edit_description)

        self.retranslateUi(ClassInfo)
        self.button_box.accepted.connect(ClassInfo.accept)
        self.button_box.rejected.connect(ClassInfo.reject)

        QMetaObject.connectSlotsByName(ClassInfo)
    # setupUi

    def retranslateUi(self, ClassInfo):
        ClassInfo.setWindowTitle(QCoreApplication.translate("ClassInfo", u"Dialog", None))
        self.label_name.setText(QCoreApplication.translate("ClassInfo", u"Name", None))
        self.button_gruppe.setText(QCoreApplication.translate("ClassInfo", u"Group", None))
        self.text_edit_description.setPlaceholderText(QCoreApplication.translate("ClassInfo", u"Description", None))
    # retranslateUi

