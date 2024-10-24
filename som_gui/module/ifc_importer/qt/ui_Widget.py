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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from som_gui.module.util.ui import (AttributeSelector, FileSelector)

class Ui_IfcImporter(object):
    def setupUi(self, IfcImporter):
        if not IfcImporter.objectName():
            IfcImporter.setObjectName(u"IfcImporter")
        IfcImporter.resize(955, 126)
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

        self.verticalLayout_2.addWidget(self.file_selector_widget)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.label_status = QLabel(IfcImporter)
        self.label_status.setObjectName(u"label_status")

        self.verticalLayout.addWidget(self.label_status)

        self.progress_bar = QProgressBar(IfcImporter)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)
        self.progress_bar.setTextVisible(True)

        self.verticalLayout.addWidget(self.progress_bar)

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
        self.label_status.setText(QCoreApplication.translate("IfcImporter", u"Status Label", None))
        self.button_close.setText(QCoreApplication.translate("IfcImporter", u"Close", None))
        self.button_run.setText(QCoreApplication.translate("IfcImporter", u"Run", None))
    # retranslateUi

