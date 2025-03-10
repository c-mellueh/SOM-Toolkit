# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from som_gui.module.property_.ui import UnitComboBox
from som_gui.module.property_table.ui import PropertyTable


class Ui_PropertySetWindow(object):
    def setupUi(self, PropertySetWindow):
        if not PropertySetWindow.objectName():
            PropertySetWindow.setObjectName("PropertySetWindow")
        PropertySetWindow.resize(1074, 600)
        self.horizontalLayout = QHBoxLayout(PropertySetWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter_2 = QSplitter(PropertySetWindow)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.gridLayoutWidget = QWidget(self.splitter_2)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)

        self.combo_data_type = QComboBox(self.gridLayoutWidget)
        self.combo_data_type.setObjectName("combo_data_type")
        self.combo_data_type.setEditable(True)

        self.gridLayout_2.addWidget(self.combo_data_type, 1, 0, 1, 1)

        self.combo_value_type = QComboBox(self.gridLayoutWidget)
        self.combo_value_type.setObjectName("combo_value_type")
        self.combo_value_type.setEditable(True)

        self.gridLayout_2.addWidget(self.combo_value_type, 1, 1, 1, 1)

        self.combo_unit = UnitComboBox(self.gridLayoutWidget)
        self.combo_unit.setObjectName("combo_unit")
        self.combo_unit.setEditable(True)

        self.gridLayout_2.addWidget(self.combo_unit, 1, 2, 1, 1)

        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 5)

        self.splitter = QSplitter(self.gridLayoutWidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.scroll_area = QScrollArea(self.splitter)
        self.scroll_area.setObjectName("scroll_area")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setMinimumSize(QSize(24, 24))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content.setObjectName("scroll_area_content")
        self.scroll_area_content.setGeometry(QRect(0, 0, 567, 267))
        self.verticalLayout_2 = QVBoxLayout(self.scroll_area_content)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scroll_area.setWidget(self.scroll_area_content)
        self.splitter.addWidget(self.scroll_area)
        self.description = QTextEdit(self.splitter)
        self.description.setObjectName("description")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy1)
        self.description.setMinimumSize(QSize(0, 28))
        self.description.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.description.setReadOnly(False)
        self.splitter.addWidget(self.description)

        self.gridLayout.addWidget(self.splitter, 7, 1, 1, 5)

        self.label_name = QLabel(self.gridLayoutWidget)
        self.label_name.setObjectName("label_name")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_name, 0, 1, 1, 1)

        self.check_box_inherit = QCheckBox(self.gridLayoutWidget)
        self.check_box_inherit.setObjectName("check_box_inherit")

        self.gridLayout.addWidget(self.check_box_inherit, 4, 5, 1, 1)

        self.button_add = QPushButton(self.gridLayoutWidget)
        self.button_add.setObjectName("button_add")

        self.gridLayout.addWidget(self.button_add, 0, 5, 1, 1)

        self.lineEdit_name = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.lineEdit_name.sizePolicy().hasHeightForWidth()
        )
        self.lineEdit_name.setSizePolicy(sizePolicy3)
        self.lineEdit_name.setMinimumSize(QSize(350, 0))

        self.gridLayout.addWidget(self.lineEdit_name, 0, 2, 1, 3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 3, 1, 1)

        self.button_add_line = QPushButton(self.gridLayoutWidget)
        self.button_add_line.setObjectName("button_add_line")
        sizePolicy2.setHeightForWidth(
            self.button_add_line.sizePolicy().hasHeightForWidth()
        )
        self.button_add_line.setSizePolicy(sizePolicy2)
        self.button_add_line.setMinimumSize(QSize(15, 15))
        self.button_add_line.setMaximumSize(QSize(24, 24))

        self.gridLayout.addWidget(self.button_add_line, 4, 1, 1, 1)

        self.label_values = QLabel(self.gridLayoutWidget)
        self.label_values.setObjectName("label_values")
        self.label_values.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.label_values, 4, 2, 1, 1)

        self.splitter_2.addWidget(self.gridLayoutWidget)
        self.table_widget = PropertyTable(self.splitter_2)
        if self.table_widget.rowCount() < 5:
            self.table_widget.setRowCount(5)
        self.table_widget.setObjectName("table_widget")
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.table_widget.sizePolicy().hasHeightForWidth()
        )
        self.table_widget.setSizePolicy(sizePolicy4)
        self.table_widget.setMinimumSize(QSize(480, 0))
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget.setDragEnabled(True)
        self.table_widget.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.table_widget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
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
        self.table_widget.horizontalHeader().setProperty("showSortIndicator", True)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(True)
        self.table_widget.verticalHeader().setCascadingSectionResizes(False)
        self.table_widget.verticalHeader().setProperty("showSortIndicator", False)
        self.table_widget.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout.addWidget(self.splitter_2)

        self.retranslateUi(PropertySetWindow)

        QMetaObject.connectSlotsByName(PropertySetWindow)

    # setupUi

    def retranslateUi(self, PropertySetWindow):
        PropertySetWindow.setWindowTitle(
            QCoreApplication.translate("PropertySetWindow", "Form", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("PropertySetWindow", "Valuetype:", None)
        )
        self.label.setText(
            QCoreApplication.translate("PropertySetWindow", "Datatype:", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("PropertySetWindow", "Unit:", None)
        )
        self.description.setPlaceholderText(
            QCoreApplication.translate("PropertySetWindow", "Description", None)
        )
        self.label_name.setText(
            QCoreApplication.translate("PropertySetWindow", "Name:", None)
        )
        self.check_box_inherit.setText(
            QCoreApplication.translate("PropertySetWindow", "Inherit Values", None)
        )
        self.button_add.setText(
            QCoreApplication.translate("PropertySetWindow", "Add", None)
        )
        self.lineEdit_name.setPlaceholderText(
            QCoreApplication.translate("PropertySetWindow", "Name", None)
        )
        self.button_add_line.setText(
            QCoreApplication.translate("PropertySetWindow", "+", None)
        )
        self.label_values.setText(
            QCoreApplication.translate("PropertySetWindow", "Allowed Values:", None)
        )

    # retranslateUi
