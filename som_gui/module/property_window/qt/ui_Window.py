# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSplitter, QTextEdit,
    QVBoxLayout, QWidget)

from som_gui.module.property_.ui import UnitComboBox

class Ui_PropertyWindow(object):
    def setupUi(self, PropertyWindow):
        if not PropertyWindow.objectName():
            PropertyWindow.setObjectName(u"PropertyWindow")
        PropertyWindow.resize(808, 536)
        self.verticalLayout = QVBoxLayout(PropertyWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(PropertyWindow)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)

        self.label = QLabel(PropertyWindow)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(PropertyWindow)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)

        self.combo_data_type = QComboBox(PropertyWindow)
        self.combo_data_type.setObjectName(u"combo_data_type")
        self.combo_data_type.setEditable(True)

        self.gridLayout_2.addWidget(self.combo_data_type, 1, 0, 1, 1)

        self.combo_value_type = QComboBox(PropertyWindow)
        self.combo_value_type.setObjectName(u"combo_value_type")
        self.combo_value_type.setEditable(True)

        self.gridLayout_2.addWidget(self.combo_value_type, 1, 1, 1, 1)

        self.combo_unit = UnitComboBox(PropertyWindow)
        self.combo_unit.setObjectName(u"combo_unit")
        self.combo_unit.setEditable(True)

        self.gridLayout_2.addWidget(self.combo_unit, 1, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 5)

        self.splitter = QSplitter(PropertyWindow)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.scroll_area = QScrollArea(self.splitter)
        self.scroll_area.setObjectName(u"scroll_area")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setMinimumSize(QSize(24, 24))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content.setObjectName(u"scroll_area_content")
        self.scroll_area_content.setGeometry(QRect(0, 0, 786, 203))
        self.verticalLayout_2 = QVBoxLayout(self.scroll_area_content)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scroll_area.setWidget(self.scroll_area_content)
        self.splitter.addWidget(self.scroll_area)
        self.description = QTextEdit(self.splitter)
        self.description.setObjectName(u"description")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy1)
        self.description.setMinimumSize(QSize(0, 28))
        self.description.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.description.setReadOnly(False)
        self.splitter.addWidget(self.description)

        self.gridLayout.addWidget(self.splitter, 7, 1, 1, 5)

        self.label_name = QLabel(PropertyWindow)
        self.label_name.setObjectName(u"label_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_name, 0, 1, 1, 1)

        self.check_box_inherit = QCheckBox(PropertyWindow)
        self.check_box_inherit.setObjectName(u"check_box_inherit")

        self.gridLayout.addWidget(self.check_box_inherit, 4, 5, 1, 1)

        self.button_add = QPushButton(PropertyWindow)
        self.button_add.setObjectName(u"button_add")

        self.gridLayout.addWidget(self.button_add, 0, 5, 1, 1)

        self.lineEdit_name = QLineEdit(PropertyWindow)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy3)
        self.lineEdit_name.setMinimumSize(QSize(350, 0))

        self.gridLayout.addWidget(self.lineEdit_name, 0, 2, 1, 3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 3, 1, 1)

        self.button_add_line = QPushButton(PropertyWindow)
        self.button_add_line.setObjectName(u"button_add_line")
        sizePolicy2.setHeightForWidth(self.button_add_line.sizePolicy().hasHeightForWidth())
        self.button_add_line.setSizePolicy(sizePolicy2)
        self.button_add_line.setMinimumSize(QSize(15, 15))
        self.button_add_line.setMaximumSize(QSize(24, 24))

        self.gridLayout.addWidget(self.button_add_line, 4, 1, 1, 1)

        self.label_values = QLabel(PropertyWindow)
        self.label_values.setObjectName(u"label_values")
        self.label_values.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.label_values, 4, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(PropertyWindow)

        QMetaObject.connectSlotsByName(PropertyWindow)
    # setupUi

    def retranslateUi(self, PropertyWindow):
        PropertyWindow.setWindowTitle(QCoreApplication.translate("PropertyWindow", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("PropertyWindow", u"Valuetype:", None))
        self.label.setText(QCoreApplication.translate("PropertyWindow", u"Datatype:", None))
        self.label_3.setText(QCoreApplication.translate("PropertyWindow", u"Unit:", None))
        self.description.setPlaceholderText(QCoreApplication.translate("PropertyWindow", u"Description", None))
        self.label_name.setText(QCoreApplication.translate("PropertyWindow", u"Name:", None))
        self.check_box_inherit.setText(QCoreApplication.translate("PropertyWindow", u"Inherit Values", None))
        self.button_add.setText(QCoreApplication.translate("PropertyWindow", u"Add", None))
        self.lineEdit_name.setPlaceholderText(QCoreApplication.translate("PropertyWindow", u"Name", None))
        self.button_add_line.setText(QCoreApplication.translate("PropertyWindow", u"+", None))
        self.label_values.setText(QCoreApplication.translate("PropertyWindow", u"Allowed Values:", None))
    # retranslateUi

