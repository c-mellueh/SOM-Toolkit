# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mapping_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSplitter, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1151, 470)
        self.gridLayout_3 = QGridLayout(Form)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setFrameShape(QFrame.Box)
        self.splitter.setOrientation(Qt.Horizontal)
        self.pset_table = QTableWidget(self.splitter)
        if (self.pset_table.columnCount() < 2):
            self.pset_table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.pset_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.pset_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.pset_table.setObjectName(u"pset_table")
        self.splitter.addWidget(self.pset_table)
        self.gridLayoutWidget = QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.right_layout = QGridLayout(self.gridLayoutWidget)
        self.right_layout.setObjectName(u"right_layout")
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.collector_widget = QWidget(self.gridLayoutWidget)
        self.collector_widget.setObjectName(u"collector_widget")
        self.upper_layout = QGridLayout(self.collector_widget)
        self.upper_layout.setObjectName(u"upper_layout")
        self.upper_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.upper_layout.setHorizontalSpacing(6)
        self.label_name = QLabel(self.collector_widget)
        self.label_name.setObjectName(u"label_name")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)

        self.upper_layout.addWidget(self.label_name, 0, 0, 1, 1)

        self.button_add = QPushButton(self.collector_widget)
        self.button_add.setObjectName(u"button_add")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_add.sizePolicy().hasHeightForWidth())
        self.button_add.setSizePolicy(sizePolicy1)
        self.button_add.setMaximumSize(QSize(27, 16777215))

        self.upper_layout.addWidget(self.button_add, 2, 3, 1, 1)

        self.label_ifcmapping = QLabel(self.collector_widget)
        self.label_ifcmapping.setObjectName(u"label_ifcmapping")
        sizePolicy.setHeightForWidth(self.label_ifcmapping.sizePolicy().hasHeightForWidth())
        self.label_ifcmapping.setSizePolicy(sizePolicy)

        self.upper_layout.addWidget(self.label_ifcmapping, 1, 0, 1, 1)

        self.label_name_modifiable = QLabel(self.collector_widget)
        self.label_name_modifiable.setObjectName(u"label_name_modifiable")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_name_modifiable.sizePolicy().hasHeightForWidth())
        self.label_name_modifiable.setSizePolicy(sizePolicy2)

        self.upper_layout.addWidget(self.label_name_modifiable, 0, 1, 1, 1)

        self.button_update = QPushButton(self.collector_widget)
        self.button_update.setObjectName(u"button_update")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_update.sizePolicy().hasHeightForWidth())
        self.button_update.setSizePolicy(sizePolicy3)
        self.button_update.setMaximumSize(QSize(100, 16777215))
        self.button_update.setLayoutDirection(Qt.RightToLeft)

        self.upper_layout.addWidget(self.button_update, 0, 2, 1, 2)

        self.line_edit_ifcmapping = QLineEdit(self.collector_widget)
        self.line_edit_ifcmapping.setObjectName(u"line_edit_ifcmapping")

        self.upper_layout.addWidget(self.line_edit_ifcmapping, 2, 0, 1, 3)


        self.right_layout.addWidget(self.collector_widget, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.attribute_table = QTableWidget(self.gridLayoutWidget)
        if (self.attribute_table.columnCount() < 2):
            self.attribute_table.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.attribute_table.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.attribute_table.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.attribute_table.setObjectName(u"attribute_table")

        self.verticalLayout.addWidget(self.attribute_table)

        self.attribute_widget = QWidget(self.gridLayoutWidget)
        self.attribute_widget.setObjectName(u"attribute_widget")
        self.attribute_widget.setEnabled(False)
        self.gridLayout = QGridLayout(self.attribute_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_edit_attribute = QLineEdit(self.attribute_widget)
        self.line_edit_attribute.setObjectName(u"line_edit_attribute")

        self.gridLayout.addWidget(self.line_edit_attribute, 2, 0, 1, 3)

        self.label_attribute = QLabel(self.attribute_widget)
        self.label_attribute.setObjectName(u"label_attribute")
        sizePolicy.setHeightForWidth(self.label_attribute.sizePolicy().hasHeightForWidth())
        self.label_attribute.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_attribute, 0, 0, 1, 1)

        self.button_update_attribute = QPushButton(self.attribute_widget)
        self.button_update_attribute.setObjectName(u"button_update_attribute")
        self.button_update_attribute.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.button_update_attribute.sizePolicy().hasHeightForWidth())
        self.button_update_attribute.setSizePolicy(sizePolicy3)
        self.button_update_attribute.setMaximumSize(QSize(100, 16777215))
        self.button_update_attribute.setLayoutDirection(Qt.RightToLeft)
        self.button_update_attribute.setCheckable(False)

        self.gridLayout.addWidget(self.button_update_attribute, 0, 2, 1, 1)

        self.label_attribute_name = QLabel(self.attribute_widget)
        self.label_attribute_name.setObjectName(u"label_attribute_name")
        sizePolicy2.setHeightForWidth(self.label_attribute_name.sizePolicy().hasHeightForWidth())
        self.label_attribute_name.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_attribute_name, 0, 1, 1, 1)

        self.label_revit_mapping = QLabel(self.attribute_widget)
        self.label_revit_mapping.setObjectName(u"label_revit_mapping")
        sizePolicy.setHeightForWidth(self.label_revit_mapping.sizePolicy().hasHeightForWidth())
        self.label_revit_mapping.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_revit_mapping, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.attribute_widget)


        self.right_layout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.splitter.addWidget(self.gridLayoutWidget)

        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)

        QWidget.setTabOrder(self.pset_table, self.line_edit_ifcmapping)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtablewidgetitem = self.pset_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"PropertySet", None));
        ___qtablewidgetitem1 = self.pset_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Ifc Mapping", None));
        self.label_name.setText(QCoreApplication.translate("Form", u"PropertySet", None))
        self.button_add.setText(QCoreApplication.translate("Form", u"+", None))
        self.label_ifcmapping.setText(QCoreApplication.translate("Form", u"Ifc Mapping", None))
        self.label_name_modifiable.setText("")
        self.button_update.setText(QCoreApplication.translate("Form", u"Update", None))
        ___qtablewidgetitem2 = self.attribute_table.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Attribut", None));
        ___qtablewidgetitem3 = self.attribute_table.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Revit Mapping", None));
        self.label_attribute.setText(QCoreApplication.translate("Form", u"Attribute", None))
        self.button_update_attribute.setText(QCoreApplication.translate("Form", u"Update", None))
        self.label_attribute_name.setText("")
        self.label_revit_mapping.setText(QCoreApplication.translate("Form", u"Revit Mapping", None))
    # retranslateUi

