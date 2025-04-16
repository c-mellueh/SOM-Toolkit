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
    QDialogButtonBox, QHeaderView, QLabel, QListWidget,
    QListWidgetItem, QSizePolicy, QSplitter, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

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
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.list_view_pset = QListWidget(self.widget)
        self.list_view_pset.setObjectName(u"list_view_pset")
        self.list_view_pset.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.list_view_pset.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view_pset.setEditTriggers(QAbstractItemView.EditTrigger.EditKeyPressed)
        self.list_view_pset.setSortingEnabled(False)

        self.verticalLayout.addWidget(self.list_view_pset)

        self.splitter.addWidget(self.widget)
        self.widget1 = QWidget(self.splitter)
        self.widget1.setObjectName(u"widget1")
        self.verticalLayout_2 = QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.table_widgets_classes = QTableWidget(self.widget1)
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

        self.verticalLayout_2.addWidget(self.table_widgets_classes)

        self.splitter.addWidget(self.widget1)
        self.widget2 = QWidget(self.splitter)
        self.widget2.setObjectName(u"widget2")
        self.verticalLayout_3 = QVBoxLayout(self.widget2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_properties = QLabel(self.widget2)
        self.label_properties.setObjectName(u"label_properties")

        self.verticalLayout_3.addWidget(self.label_properties)

        self.table_properties = PropertyTable(self.widget2)
        self.table_properties.setObjectName(u"table_properties")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_properties.sizePolicy().hasHeightForWidth())
        self.table_properties.setSizePolicy(sizePolicy)
        self.table_properties.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_properties.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.table_properties)

        self.splitter.addWidget(self.widget2)

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
        self.label_2.setText(QCoreApplication.translate("PredefinedPset", u"Inherits to:", None))
        ___qtablewidgetitem = self.table_widgets_classes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PredefinedPset", u"Name", None));
        ___qtablewidgetitem1 = self.table_widgets_classes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PredefinedPset", u"Identifier", None));
        self.label_properties.setText(QCoreApplication.translate("PredefinedPset", u"Properties:", None))
    # retranslateUi

