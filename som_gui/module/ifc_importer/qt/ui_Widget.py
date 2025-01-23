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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from som_gui.module.util.ui import (AttributeSelector, FileSelector)

class Ui_IfcImporter(object):
    def setupUi(self, IfcImporter):
        if not IfcImporter.objectName():
            IfcImporter.setObjectName(u"IfcImporter")
        IfcImporter.resize(944, 74)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(IfcImporter.sizePolicy().hasHeightForWidth())
        IfcImporter.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(IfcImporter)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_attribute_widget = AttributeSelector(IfcImporter)
        self.main_attribute_widget.setObjectName(u"main_attribute_widget")

        self.verticalLayout_2.addWidget(self.main_attribute_widget)

        self.file_selector_widget = FileSelector(IfcImporter)
        self.file_selector_widget.setObjectName(u"file_selector_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.file_selector_widget.sizePolicy().hasHeightForWidth())
        self.file_selector_widget.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.file_selector_widget)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.scrollArea = QScrollArea(IfcImporter)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setMinimumSize(QSize(0, 150))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 924, 148))
        self.layout_progress_bar = QVBoxLayout(self.scrollAreaWidgetContents)
        self.layout_progress_bar.setObjectName(u"layout_progress_bar")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.button_widget = QWidget(IfcImporter)
        self.button_widget.setObjectName(u"button_widget")
        self.horizontalLayout_2 = QHBoxLayout(self.button_widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(664, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.button_close = QPushButton(self.button_widget)
        self.button_close.setObjectName(u"button_close")

        self.horizontalLayout_2.addWidget(self.button_close)

        self.button_run = QPushButton(self.button_widget)
        self.button_run.setObjectName(u"button_run")

        self.horizontalLayout_2.addWidget(self.button_run)


        self.verticalLayout.addWidget(self.button_widget)


        self.retranslateUi(IfcImporter)

        QMetaObject.connectSlotsByName(IfcImporter)
    # setupUi

    def retranslateUi(self, IfcImporter):
        IfcImporter.setWindowTitle(QCoreApplication.translate("IfcImporter", u"Form", None))
        self.button_close.setText(QCoreApplication.translate("IfcImporter", u"Close", None))
        self.button_run.setText(QCoreApplication.translate("IfcImporter", u"Run", None))
    # retranslateUi

