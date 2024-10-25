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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialogButtonBox,
                               QHeaderView, QLabel, QSizePolicy, QSplitter,
                               QVBoxLayout, QWidget)

from som_gui.module.modelcheck_window.ui import (ObjectTree, PsetTree)
from som_gui.module.util.ui import (AttributeSelector, FileSelector, Progressbar)

class Ui_Modelcheck(object):
    def setupUi(self, Modelcheck):
        if not Modelcheck.objectName():
            Modelcheck.setObjectName(u"Modelcheck")
        Modelcheck.resize(1037, 684)
        self.verticalLayout = QVBoxLayout(Modelcheck)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Modelcheck)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.object_tree = ObjectTree(self.splitter)
        self.object_tree.setObjectName(u"object_tree")
        self.object_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.object_tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.splitter.addWidget(self.object_tree)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_object = QLabel(self.verticalLayoutWidget)
        self.label_object.setObjectName(u"label_object")

        self.verticalLayout_2.addWidget(self.label_object)

        self.property_set_tree = PsetTree(self.verticalLayoutWidget)
        self.property_set_tree.setObjectName(u"property_set_tree")
        self.property_set_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.property_set_tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout_2.addWidget(self.property_set_tree)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.verticalLayout.addWidget(self.splitter)

        self.main_attribute_widget = AttributeSelector(Modelcheck)
        self.main_attribute_widget.setObjectName(u"main_attribute_widget")
        self.main_attribute_widget.setMinimumSize(QSize(0, 10))

        self.verticalLayout.addWidget(self.main_attribute_widget)

        self.widget_import = FileSelector(Modelcheck)
        self.widget_import.setObjectName(u"widget_import")
        self.widget_import.setMinimumSize(QSize(0, 30))

        self.verticalLayout.addWidget(self.widget_import)

        self.widget_export = FileSelector(Modelcheck)
        self.widget_export.setObjectName(u"widget_export")
        self.widget_export.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.widget_export)

        self.widget_progress_bar = Progressbar(Modelcheck)
        self.widget_progress_bar.setObjectName(u"widget_progress_bar")

        self.verticalLayout.addWidget(self.widget_progress_bar)

        self.buttonBox = QDialogButtonBox(Modelcheck)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Apply | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Modelcheck)

        QMetaObject.connectSlotsByName(Modelcheck)
    # setupUi

    def retranslateUi(self, Modelcheck):
        Modelcheck.setWindowTitle(QCoreApplication.translate("Modelcheck", u"Form", None))
        self.label_object.setText(QCoreApplication.translate("Modelcheck", u"TextLabel", None))
    # retranslateUi

