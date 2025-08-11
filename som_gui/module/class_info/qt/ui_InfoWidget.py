# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InfoWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QSizePolicy,
    QTextEdit,
    QToolBox,
    QVBoxLayout,
    QWidget,
)


class Ui_ClassInfo(object):
    def setupUi(self, ClassInfo):
        if not ClassInfo.objectName():
            ClassInfo.setObjectName("ClassInfo")
        ClassInfo.resize(798, 572)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClassInfo.sizePolicy().hasHeightForWidth())
        ClassInfo.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ClassInfo)
        self.verticalLayout.setObjectName("verticalLayout")
        self.group_main = QGroupBox(ClassInfo)
        self.group_main.setObjectName("group_main")
        self.verticalLayout_3 = QVBoxLayout(self.group_main)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontal_layout_info = QHBoxLayout()
        self.horizontal_layout_info.setObjectName("horizontal_layout_info")
        self.label_name = QLabel(self.group_main)
        self.label_name.setObjectName("label_name")

        self.horizontal_layout_info.addWidget(self.label_name)

        self.line_edit_name = QLineEdit(self.group_main)
        self.line_edit_name.setObjectName("line_edit_name")

        self.horizontal_layout_info.addWidget(self.line_edit_name)

        self.verticalLayout_3.addLayout(self.horizontal_layout_info)

        self.horizontal_layout_group = QHBoxLayout()
        self.horizontal_layout_group.setObjectName("horizontal_layout_group")
        self.button_gruppe = QRadioButton(self.group_main)
        self.button_gruppe.setObjectName("button_gruppe")

        self.horizontal_layout_group.addWidget(self.button_gruppe)

        self.verticalLayout_3.addLayout(self.horizontal_layout_group)

        self.layout_ident_property = QHBoxLayout()
        self.layout_ident_property.setObjectName("layout_ident_property")
        self.combo_box_pset = QComboBox(self.group_main)
        self.combo_box_pset.setObjectName("combo_box_pset")
        self.combo_box_pset.setEditable(True)

        self.layout_ident_property.addWidget(self.combo_box_pset)

        self.combo_box_property = QComboBox(self.group_main)
        self.combo_box_property.setObjectName("combo_box_property")
        self.combo_box_property.setEditable(True)

        self.layout_ident_property.addWidget(self.combo_box_property)

        self.line_edit_property_value = QLineEdit(self.group_main)
        self.line_edit_property_value.setObjectName("line_edit_property_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.line_edit_property_value.sizePolicy().hasHeightForWidth()
        )
        self.line_edit_property_value.setSizePolicy(sizePolicy1)

        self.layout_ident_property.addWidget(self.line_edit_property_value)

        self.verticalLayout_3.addLayout(self.layout_ident_property)

        self.verticalLayout.addWidget(self.group_main)

        self.group_ifc = QGroupBox(ClassInfo)
        self.group_ifc.setObjectName("group_ifc")
        self.verticalLayout_2 = QVBoxLayout(self.group_ifc)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox = QToolBox(self.group_ifc)
        self.toolBox.setObjectName("toolBox")

        self.verticalLayout_2.addWidget(self.toolBox)

        self.verticalLayout.addWidget(self.group_ifc)

        self.group_description = QGroupBox(ClassInfo)
        self.group_description.setObjectName("group_description")
        self.verticalLayout_4 = QVBoxLayout(self.group_description)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.text_edit_description = QTextEdit(self.group_description)
        self.text_edit_description.setObjectName("text_edit_description")

        self.verticalLayout_4.addWidget(self.text_edit_description)

        self.verticalLayout.addWidget(self.group_description)

        self.button_box = QDialogButtonBox(ClassInfo)
        self.button_box.setObjectName("button_box")
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )

        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(ClassInfo)
        self.button_box.accepted.connect(ClassInfo.accept)
        self.button_box.rejected.connect(ClassInfo.reject)

        self.toolBox.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(ClassInfo)

    # setupUi

    def retranslateUi(self, ClassInfo):
        ClassInfo.setWindowTitle(
            QCoreApplication.translate("ClassInfo", "Dialog", None)
        )
        self.group_main.setTitle(QCoreApplication.translate("ClassInfo", "Main", None))
        self.label_name.setText(QCoreApplication.translate("ClassInfo", "Name", None))
        self.button_gruppe.setText(
            QCoreApplication.translate("ClassInfo", "Group", None)
        )
        self.group_ifc.setTitle(
            QCoreApplication.translate("ClassInfo", "IFC-Mapping", None)
        )
        self.group_description.setTitle(
            QCoreApplication.translate("ClassInfo", "Description", None)
        )
        self.text_edit_description.setPlaceholderText(
            QCoreApplication.translate("ClassInfo", "Description", None)
        )

    # retranslateUi
