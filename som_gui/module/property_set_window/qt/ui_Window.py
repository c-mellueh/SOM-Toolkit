# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Window.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSplitter, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

from som_gui.module.attribute_table.ui import AttributeTable

class Ui_PropertySetWindow(object):
    def setupUi(self, PropertySetWindow):
        if not PropertySetWindow.objectName():
            PropertySetWindow.setObjectName(u"PropertySetWindow")
        PropertySetWindow.resize(994, 542)
        self.horizontalLayout = QHBoxLayout(PropertySetWindow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter_2 = QSplitter(PropertySetWindow)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.gridLayoutWidget = QWidget(self.splitter_2)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_values = QLabel(self.gridLayoutWidget)
        self.label_values.setObjectName(u"label_values")
        self.label_values.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.label_values, 1, 0, 1, 1)

        self.combo_type = QComboBox(self.gridLayoutWidget)
        self.combo_type.setObjectName(u"combo_type")

        self.gridLayout.addWidget(self.combo_type, 0, 2, 1, 1)

        self.button_add_line = QPushButton(self.gridLayoutWidget)
        self.button_add_line.setObjectName(u"button_add_line")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_add_line.sizePolicy().hasHeightForWidth())
        self.button_add_line.setSizePolicy(sizePolicy)
        self.button_add_line.setMinimumSize(QSize(15, 15))
        self.button_add_line.setMaximumSize(QSize(24, 24))

        self.gridLayout.addWidget(self.button_add_line, 1, 4, 1, 1)

        self.button_add = QPushButton(self.gridLayoutWidget)
        self.button_add.setObjectName(u"button_add")

        self.gridLayout.addWidget(self.button_add, 0, 3, 1, 2)

        self.check_box_seperator = QCheckBox(self.gridLayoutWidget)
        self.check_box_seperator.setObjectName(u"check_box_seperator")
        self.check_box_seperator.setChecked(True)

        self.gridLayout.addWidget(self.check_box_seperator, 1, 2, 1, 1)

        self.check_box_inherit = QCheckBox(self.gridLayoutWidget)
        self.check_box_inherit.setObjectName(u"check_box_inherit")

        self.gridLayout.addWidget(self.check_box_inherit, 1, 1, 1, 1)

        self.combo_data_type = QComboBox(self.gridLayoutWidget)
        self.combo_data_type.setObjectName(u"combo_data_type")

        self.gridLayout.addWidget(self.combo_data_type, 0, 1, 1, 1)

        self.line_edit_seperator = QLineEdit(self.gridLayoutWidget)
        self.line_edit_seperator.setObjectName(u"line_edit_seperator")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line_edit_seperator.sizePolicy().hasHeightForWidth())
        self.line_edit_seperator.setSizePolicy(sizePolicy1)
        self.line_edit_seperator.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.line_edit_seperator, 1, 3, 1, 1)

        self.label_name = QLabel(self.gridLayoutWidget)
        self.label_name.setObjectName(u"label_name")
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)

        self.lineEdit_name = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy2)
        self.lineEdit_name.setMinimumSize(QSize(350, 0))

        self.gridLayout.addWidget(self.lineEdit_name, 3, 0, 1, 5)

        self.splitter = QSplitter(self.gridLayoutWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.scroll_area = QScrollArea(self.splitter)
        self.scroll_area.setObjectName(u"scroll_area")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy3)
        self.scroll_area.setMinimumSize(QSize(24, 24))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content.setObjectName(u"scroll_area_content")
        self.scroll_area_content.setGeometry(QRect(0, 0, 487, 235))
        self.verticalLayout_2 = QVBoxLayout(self.scroll_area_content)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scroll_area.setWidget(self.scroll_area_content)
        self.splitter.addWidget(self.scroll_area)
        self.description = QTextEdit(self.splitter)
        self.description.setObjectName(u"description")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy4)
        self.description.setMinimumSize(QSize(0, 28))
        self.description.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.description.setReadOnly(False)
        self.splitter.addWidget(self.description)

        self.gridLayout.addWidget(self.splitter, 4, 0, 1, 5)

        self.splitter_2.addWidget(self.gridLayoutWidget)
        self.table_widget = AttributeTable(self.splitter_2)
        if (self.table_widget.rowCount() < 5):
            self.table_widget.setRowCount(5)
        self.table_widget.setObjectName(u"table_widget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.table_widget.sizePolicy().hasHeightForWidth())
        self.table_widget.setSizePolicy(sizePolicy5)
        self.table_widget.setMinimumSize(QSize(480, 0))
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget.setDragEnabled(True)
        self.table_widget.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget.setIconSize(QSize(10, 10))
        self.table_widget.setShowGrid(True)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setCornerButtonEnabled(True)
        self.table_widget.setRowCount(5)
        self.splitter_2.addWidget(self.table_widget)
        self.table_widget.horizontalHeader().setVisible(True)
        self.table_widget.horizontalHeader().setCascadingSectionResizes(False)
        self.table_widget.horizontalHeader().setMinimumSectionSize(50)
        self.table_widget.horizontalHeader().setDefaultSectionSize(70)
        self.table_widget.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(True)
        self.table_widget.verticalHeader().setCascadingSectionResizes(False)
        self.table_widget.verticalHeader().setProperty(u"showSortIndicator", False)
        self.table_widget.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout.addWidget(self.splitter_2)


        self.retranslateUi(PropertySetWindow)

        QMetaObject.connectSlotsByName(PropertySetWindow)
    # setupUi

    def retranslateUi(self, PropertySetWindow):
        PropertySetWindow.setWindowTitle(QCoreApplication.translate("PropertySetWindow", u"Form", None))
        self.label_values.setText(QCoreApplication.translate("PropertySetWindow", u"Values", None))
        self.button_add_line.setText(QCoreApplication.translate("PropertySetWindow", u"+", None))
        self.button_add.setText(QCoreApplication.translate("PropertySetWindow", u"Add", None))
        self.check_box_seperator.setText(QCoreApplication.translate("PropertySetWindow", u"Splitter", None))
        self.check_box_inherit.setText(QCoreApplication.translate("PropertySetWindow", u"Inherit Values", None))
        self.label_name.setText(QCoreApplication.translate("PropertySetWindow", u"Name", None))
        self.lineEdit_name.setPlaceholderText(QCoreApplication.translate("PropertySetWindow", u"Name", None))
        self.description.setPlaceholderText(QCoreApplication.translate("PropertySetWindow", u"Description", None))
    # retranslateUi

