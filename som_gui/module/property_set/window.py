# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PropertySetWindow.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
                               QSplitter, QTableWidgetItem, QTextEdit, QVBoxLayout,
                               QWidget)

from som_gui.module.attribute.ui import AttributeTable

class Ui_layout_main(object):
    def setupUi(self, layout_main):
        if not layout_main.objectName():
            layout_main.setObjectName(u"layout_main")
        layout_main.resize(996, 547)
        self.horizontalLayout = QHBoxLayout(layout_main)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter_2 = QSplitter(layout_main)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
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
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.combo_type.setObjectName(u"combo_type")

        self.gridLayout.addWidget(self.combo_type, 0, 2, 1, 1)

        self.button_add_line = QPushButton(self.gridLayoutWidget)
        self.button_add_line.setObjectName(u"button_add_line")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_add_line.sizePolicy().hasHeightForWidth())
        self.button_add_line.setSizePolicy(sizePolicy)
        self.button_add_line.setMinimumSize(QSize(15, 15))
        self.button_add_line.setMaximumSize(QSize(15, 15))

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
        self.combo_data_type.addItem("")
        self.combo_data_type.addItem("")
        self.combo_data_type.addItem("")
        self.combo_data_type.setObjectName(u"combo_data_type")

        self.gridLayout.addWidget(self.combo_data_type, 0, 1, 1, 1)

        self.line_edit_seperator = QLineEdit(self.gridLayoutWidget)
        self.line_edit_seperator.setObjectName(u"line_edit_seperator")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy2)
        self.lineEdit_name.setMinimumSize(QSize(350, 0))

        self.gridLayout.addWidget(self.lineEdit_name, 3, 0, 1, 5)

        self.splitter = QSplitter(self.gridLayoutWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.scroll_area = QScrollArea(self.splitter)
        self.scroll_area.setObjectName(u"scroll_area")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy3)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_content.setObjectName(u"scroll_area_content")
        self.scroll_area_content.setGeometry(QRect(0, 0, 489, 242))
        self.verticalLayout_2 = QVBoxLayout(self.scroll_area_content)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scroll_area.setWidget(self.scroll_area_content)
        self.splitter.addWidget(self.scroll_area)
        self.description = QTextEdit(self.splitter)
        self.description.setObjectName(u"description")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy4)
        self.description.setMinimumSize(QSize(0, 28))
        self.description.setAutoFormatting(QTextEdit.AutoAll)
        self.description.setReadOnly(False)
        self.splitter.addWidget(self.description)

        self.gridLayout.addWidget(self.splitter, 4, 0, 1, 5)

        self.splitter_2.addWidget(self.gridLayoutWidget)
        self.table_widget = AttributeTable(self.splitter_2)
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
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.table_widget.sizePolicy().hasHeightForWidth())
        self.table_widget.setSizePolicy(sizePolicy5)
        self.table_widget.setMinimumSize(QSize(480, 0))
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setDragEnabled(True)
        self.table_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
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


        self.retranslateUi(layout_main)

        QMetaObject.connectSlotsByName(layout_main)
    # setupUi

    def retranslateUi(self, layout_main):
        layout_main.setWindowTitle(QCoreApplication.translate("layout_main", u"Form", None))
        self.label_values.setText(QCoreApplication.translate("layout_main", u"Werte", None))
        self.combo_type.setItemText(0, QCoreApplication.translate("layout_main", u"Liste", None))
        self.combo_type.setItemText(1, QCoreApplication.translate("layout_main", u"Formatvorgabe", None))
        self.combo_type.setItemText(2, QCoreApplication.translate("layout_main", u"Wertebereich", None))

        self.button_add_line.setText(QCoreApplication.translate("layout_main", u"+", None))
        self.button_add.setText(QCoreApplication.translate("layout_main", u"Hinzuf\u00fcgen", None))
        self.check_box_seperator.setText(QCoreApplication.translate("layout_main", u"Trennzeichen:", None))
        self.check_box_inherit.setText(QCoreApplication.translate("layout_main", u"Vererbt", None))
        self.combo_data_type.setItemText(0, QCoreApplication.translate("layout_main", u"xs:string", None))
        self.combo_data_type.setItemText(1, QCoreApplication.translate("layout_main", u"xs:int", None))
        self.combo_data_type.setItemText(2, QCoreApplication.translate("layout_main", u"xs:double", None))

        self.label_name.setText(QCoreApplication.translate("layout_main", u"Name", None))
        self.lineEdit_name.setPlaceholderText(QCoreApplication.translate("layout_main", u"Name", None))
        self.description.setPlaceholderText(QCoreApplication.translate("layout_main", u"Beschreibung", None))
        ___qtablewidgetitem = self.table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("layout_main", u"Name", None));
        ___qtablewidgetitem1 = self.table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("layout_main", u"Datentyp", None));
        ___qtablewidgetitem2 = self.table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("layout_main", u"Format", None));
        ___qtablewidgetitem3 = self.table_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("layout_main", u"Wert", None));
        ___qtablewidgetitem4 = self.table_widget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("layout_main", u"Optional", None));

        __sortingEnabled = self.table_widget.isSortingEnabled()
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

