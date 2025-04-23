# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from som_gui.module.property_table.ui import PropertyTable

class Ui_PredefinedPset(object):
    def setupUi(self, PredefinedPset):
        if not PredefinedPset.objectName():
            PredefinedPset.setObjectName(u"PredefinedPset")
        PredefinedPset.resize(953, 569)
        PredefinedPset.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.verticalLayout_4 = QVBoxLayout(PredefinedPset)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.splitter = QSplitter(PredefinedPset)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layout_pset = QVBoxLayout(self.layoutWidget)
        self.layout_pset.setObjectName(u"layout_pset")
        self.layout_pset.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.layout_pset.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.button_pset = QPushButton(self.layoutWidget)
        self.button_pset.setObjectName(u"button_pset")

        self.horizontalLayout.addWidget(self.button_pset)


        self.layout_pset.addLayout(self.horizontalLayout)

        self.list_view_pset = QListWidget(self.layoutWidget)
        self.list_view_pset.setObjectName(u"list_view_pset")
        self.list_view_pset.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.list_view_pset.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view_pset.setEditTriggers(QAbstractItemView.EditTrigger.EditKeyPressed)
        self.list_view_pset.setSortingEnabled(False)

        self.layout_pset.addWidget(self.list_view_pset)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layout_inheritance = QVBoxLayout(self.layoutWidget1)
        self.layout_inheritance.setObjectName(u"layout_inheritance")
        self.layout_inheritance.setContentsMargins(0, 0, 0, 0)
        self.label_properties = QLabel(self.layoutWidget1)
        self.label_properties.setObjectName(u"label_properties")

        self.layout_inheritance.addWidget(self.label_properties)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.button_property = QPushButton(self.layoutWidget1)
        self.button_property.setObjectName(u"button_property")

        self.horizontalLayout_2.addWidget(self.button_property)


        self.layout_inheritance.addLayout(self.horizontalLayout_2)

        self.table_properties = PropertyTable(self.layoutWidget1)
        self.table_properties.setObjectName(u"table_properties")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_properties.sizePolicy().hasHeightForWidth())
        self.table_properties.setSizePolicy(sizePolicy)
        self.table_properties.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_properties.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_properties.horizontalHeader().setStretchLastSection(True)

        self.layout_inheritance.addWidget(self.table_properties)

        self.splitter.addWidget(self.layoutWidget1)
        self.layoutWidget2 = QWidget(self.splitter)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layout_property = QVBoxLayout(self.layoutWidget2)
        self.layout_property.setObjectName(u"layout_property")
        self.layout_property.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget2)
        self.label_2.setObjectName(u"label_2")

        self.layout_property.addWidget(self.label_2)

        self.table_widgets_classes = QTableWidget(self.layoutWidget2)
        if (self.table_widgets_classes.columnCount() < 2):
            self.table_widgets_classes.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widgets_classes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widgets_classes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table_widgets_classes.setObjectName(u"table_widgets_classes")
        self.table_widgets_classes.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widgets_classes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widgets_classes.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table_widgets_classes.setSortingEnabled(True)
        self.table_widgets_classes.horizontalHeader().setStretchLastSection(True)
        self.table_widgets_classes.verticalHeader().setVisible(False)

        self.layout_property.addWidget(self.table_widgets_classes)

        self.splitter.addWidget(self.layoutWidget2)

        self.verticalLayout_4.addWidget(self.splitter)

        self.buttonBox = QDialogButtonBox(PredefinedPset)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.retranslateUi(PredefinedPset)
        self.buttonBox.accepted.connect(PredefinedPset.accept)
        self.buttonBox.rejected.connect(PredefinedPset.reject)

        QMetaObject.connectSlotsByName(PredefinedPset)
    # setupUi

    def retranslateUi(self, PredefinedPset):
        PredefinedPset.setWindowTitle(QCoreApplication.translate("PredefinedPset", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("PredefinedPset", u"PropertySet", None))
        self.button_pset.setText(QCoreApplication.translate("PredefinedPset", u"New", None))
        self.label_properties.setText(QCoreApplication.translate("PredefinedPset", u"Properties:", None))
        self.button_property.setText(QCoreApplication.translate("PredefinedPset", u"New", None))
        self.label_2.setText(QCoreApplication.translate("PredefinedPset", u"Inherits to:", None))
        ___qtablewidgetitem = self.table_widgets_classes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PredefinedPset", u"Name", None));
        ___qtablewidgetitem1 = self.table_widgets_classes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PredefinedPset", u"Identifier", None));
    # retranslateUi

