# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
                               QDialogButtonBox, QGridLayout, QHeaderView, QLabel,
                               QListWidget, QListWidgetItem, QSizePolicy, QTableWidget,
                               QTableWidgetItem, QWidget)


class Ui_PredefinedPset(object):
    def setupUi(self, PredefinedPset):
        if not PredefinedPset.objectName():
            PredefinedPset.setObjectName(u"PredefinedPset")
        PredefinedPset.resize(659, 492)
        PredefinedPset.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.gridLayout = QGridLayout(PredefinedPset)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(PredefinedPset)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.list_view_pset = QListWidget(PredefinedPset)
        self.list_view_pset.setObjectName(u"list_view_pset")
        self.list_view_pset.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.list_view_pset.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_view_pset.setEditTriggers(QAbstractItemView.EditTrigger.EditKeyPressed)
        self.list_view_pset.setSortingEnabled(False)

        self.gridLayout.addWidget(self.list_view_pset, 1, 0, 1, 1)

        self.label = QLabel(PredefinedPset)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(PredefinedPset)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.table_widgets_objects = QTableWidget(PredefinedPset)
        if (self.table_widgets_objects.columnCount() < 2):
            self.table_widgets_objects.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widgets_objects.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widgets_objects.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table_widgets_objects.setObjectName(u"table_widgets_objects")
        self.table_widgets_objects.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widgets_objects.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widgets_objects.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table_widgets_objects.setSortingEnabled(True)
        self.table_widgets_objects.horizontalHeader().setStretchLastSection(True)
        self.table_widgets_objects.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.table_widgets_objects, 1, 1, 1, 1)

        self.retranslateUi(PredefinedPset)
        self.buttonBox.accepted.connect(PredefinedPset.accept)
        self.buttonBox.rejected.connect(PredefinedPset.reject)

        QMetaObject.connectSlotsByName(PredefinedPset)
    # setupUi

    def retranslateUi(self, PredefinedPset):
        PredefinedPset.setWindowTitle(QCoreApplication.translate("PredefinedPset", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("PredefinedPset", u"PropertySet", None))
        self.label_2.setText(QCoreApplication.translate("PredefinedPset", u"Inherits to:", None))
        ___qtablewidgetitem = self.table_widgets_objects.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PredefinedPset", u"Name", None));
        ___qtablewidgetitem1 = self.table_widgets_objects.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PredefinedPset", u"Identifier", None));
    # retranslateUi

