# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PropertySetWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_layout_main(object):
    def setupUi(self, layout_main):
        if not layout_main.objectName():
            layout_main.setObjectName(u"layout_main")
        layout_main.resize(1138, 563)
        self.horizontalLayout = QHBoxLayout(layout_main)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.layout_grid = QGridLayout()
        self.layout_grid.setObjectName(u"layout_grid")
        self.check_box_inherit = QCheckBox(layout_main)
        self.check_box_inherit.setObjectName(u"check_box_inherit")

        self.layout_grid.addWidget(self.check_box_inherit, 4, 1, 1, 1)

        self.check_box_seperator = QCheckBox(layout_main)
        self.check_box_seperator.setObjectName(u"check_box_seperator")
        self.check_box_seperator.setChecked(True)

        self.layout_grid.addWidget(self.check_box_seperator, 4, 2, 1, 1)

        self.description = QTextEdit(layout_main)
        self.description.setObjectName(u"description")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setMinimumSize(QSize(0, 28))

        self.layout_grid.addWidget(self.description, 9, 0, 1, 4)

        self.label_name = QLabel(layout_main)
        self.label_name.setObjectName(u"label_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy1)

        self.layout_grid.addWidget(self.label_name, 2, 0, 1, 1)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_grid.addItem(self.spacer, 7, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout_input = QHBoxLayout()
        self.layout_input.setObjectName(u"layout_input")
        self.button_add_line = QPushButton(layout_main)
        self.button_add_line.setObjectName(u"button_add_line")
        sizePolicy1.setHeightForWidth(self.button_add_line.sizePolicy().hasHeightForWidth())
        self.button_add_line.setSizePolicy(sizePolicy1)
        self.button_add_line.setMinimumSize(QSize(15, 15))
        self.button_add_line.setMaximumSize(QSize(15, 15))

        self.layout_input.addWidget(self.button_add_line)


        self.verticalLayout.addLayout(self.layout_input)


        self.layout_grid.addLayout(self.verticalLayout, 6, 0, 1, 4)

        self.label_values = QLabel(layout_main)
        self.label_values.setObjectName(u"label_values")
        self.label_values.setMinimumSize(QSize(0, 0))

        self.layout_grid.addWidget(self.label_values, 4, 0, 1, 1)

        self.lineEdit_name = QLineEdit(layout_main)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy2)
        self.lineEdit_name.setMinimumSize(QSize(350, 0))

        self.layout_grid.addWidget(self.lineEdit_name, 3, 0, 1, 4)

        self.combo_type = QComboBox(layout_main)
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.combo_type.setObjectName(u"combo_type")

        self.layout_grid.addWidget(self.combo_type, 2, 2, 1, 1)

        self.combo_data_type = QComboBox(layout_main)
        self.combo_data_type.addItem("")
        self.combo_data_type.addItem("")
        self.combo_data_type.addItem("")
        self.combo_data_type.addItem("")
        self.combo_data_type.setObjectName(u"combo_data_type")

        self.layout_grid.addWidget(self.combo_data_type, 2, 1, 1, 1)

        self.button_add = QPushButton(layout_main)
        self.button_add.setObjectName(u"button_add")

        self.layout_grid.addWidget(self.button_add, 2, 3, 1, 1)

        self.line_edit_seperator = QLineEdit(layout_main)
        self.line_edit_seperator.setObjectName(u"line_edit_seperator")
        sizePolicy3 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line_edit_seperator.sizePolicy().hasHeightForWidth())
        self.line_edit_seperator.setSizePolicy(sizePolicy3)
        self.line_edit_seperator.setMaximumSize(QSize(16777215, 16777215))

        self.layout_grid.addWidget(self.line_edit_seperator, 4, 3, 1, 1)

        self.label = QLabel(layout_main)
        self.label.setObjectName(u"label")

        self.layout_grid.addWidget(self.label, 8, 0, 1, 1)


        self.horizontalLayout.addLayout(self.layout_grid)

        self.table_widget = QTableWidget(layout_main)
        if (self.table_widget.columnCount() < 5):
            self.table_widget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.table_widget.rowCount() < 5):
            self.table_widget.setRowCount(5)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget.setItem(0, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_widget.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_widget.setItem(0, 2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_widget.setItem(0, 3, __qtablewidgetitem8)
        self.table_widget.setObjectName(u"table_widget")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.table_widget.sizePolicy().hasHeightForWidth())
        self.table_widget.setSizePolicy(sizePolicy4)
        self.table_widget.setMinimumSize(QSize(480, 0))
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setDragEnabled(True)
        self.table_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setIconSize(QSize(10, 10))
        self.table_widget.setShowGrid(True)
        self.table_widget.setCornerButtonEnabled(True)
        self.table_widget.setRowCount(5)
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

        self.horizontalLayout.addWidget(self.table_widget)


        self.retranslateUi(layout_main)

        QMetaObject.connectSlotsByName(layout_main)
    # setupUi

    def retranslateUi(self, layout_main):
        layout_main.setWindowTitle(QCoreApplication.translate("layout_main", u"Form", None))
        self.check_box_inherit.setText(QCoreApplication.translate("layout_main", u"inherit", None))
        self.check_box_seperator.setText(QCoreApplication.translate("layout_main", u"Seperate:", None))
        self.label_name.setText(QCoreApplication.translate("layout_main", u"Name", None))
        self.button_add_line.setText(QCoreApplication.translate("layout_main", u"+", None))
        self.label_values.setText(QCoreApplication.translate("layout_main", u"Values", None))
        self.lineEdit_name.setPlaceholderText(QCoreApplication.translate("layout_main", u"Name", None))
        self.combo_type.setItemText(0, QCoreApplication.translate("layout_main", u"List", None))
        self.combo_type.setItemText(1, QCoreApplication.translate("layout_main", u"Format", None))
        self.combo_type.setItemText(2, QCoreApplication.translate("layout_main", u"Range", None))

        self.combo_data_type.setItemText(0, QCoreApplication.translate("layout_main", u"xs:string", None))
        self.combo_data_type.setItemText(1, QCoreApplication.translate("layout_main", u"xs:int", None))
        self.combo_data_type.setItemText(2, QCoreApplication.translate("layout_main", u"xs:bool", None))
        self.combo_data_type.setItemText(3, QCoreApplication.translate("layout_main", u"xs:double", None))

        self.button_add.setText(QCoreApplication.translate("layout_main", u"Add", None))
        self.label.setText(QCoreApplication.translate("layout_main", u"Beschreibung", None))
        ___qtablewidgetitem = self.table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("layout_main", u"Name", None));
        ___qtablewidgetitem1 = self.table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("layout_main", u"Data Format", None));
        ___qtablewidgetitem2 = self.table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("layout_main", u"Format", None));
        ___qtablewidgetitem3 = self.table_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("layout_main", u"Values", None));
        ___qtablewidgetitem4 = self.table_widget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("layout_main", u"Optional", None));

        __sortingEnabled = self.table_widget.isSortingEnabled()
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

