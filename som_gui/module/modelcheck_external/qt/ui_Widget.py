# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
    QAbstractButton,
    QAbstractItemView,
    QApplication,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenuBar,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from som_gui.module.modelcheck_window.ui import ObjectTree, PsetTree
from som_gui.module.util.ui import PropertySelector


class Ui_Modelcheck(object):
    def setupUi(self, Modelcheck):
        if not Modelcheck.objectName():
            Modelcheck.setObjectName("Modelcheck")
        Modelcheck.resize(1383, 868)
        self.centralwidget = QWidget(Modelcheck)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_attribute_widget = PropertySelector(self.centralwidget)
        self.main_attribute_widget.setObjectName("main_attribute_widget")
        self.main_attribute_widget.setMinimumSize(QSize(0, 10))

        self.verticalLayout.addWidget(self.main_attribute_widget)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.object_tree = ObjectTree(self.splitter)
        self.object_tree.setObjectName("object_tree")
        self.object_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.object_tree.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.splitter.addWidget(self.object_tree)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_object = QLabel(self.verticalLayoutWidget)
        self.label_object.setObjectName("label_object")

        self.verticalLayout_2.addWidget(self.label_object)

        self.property_set_tree = PsetTree(self.verticalLayoutWidget)
        self.property_set_tree.setObjectName("property_set_tree")
        self.property_set_tree.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.property_set_tree.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )

        self.verticalLayout_2.addWidget(self.property_set_tree)

        self.splitter.addWidget(self.verticalLayoutWidget)

        self.verticalLayout.addWidget(self.splitter)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        Modelcheck.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Modelcheck)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1383, 33))
        Modelcheck.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Modelcheck)
        self.statusbar.setObjectName("statusbar")
        Modelcheck.setStatusBar(self.statusbar)

        self.retranslateUi(Modelcheck)

        QMetaObject.connectSlotsByName(Modelcheck)

    # setupUi

    def retranslateUi(self, Modelcheck):
        Modelcheck.setWindowTitle(
            QCoreApplication.translate("Modelcheck", "MainWindow", None)
        )
        self.label_object.setText(
            QCoreApplication.translate("Modelcheck", "TextLabel", None)
        )

    # retranslateUi
