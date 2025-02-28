# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from som_gui.module.util.ui import (AttributeSelector, FileSelector)

class Ui_Aggregation(object):
    def setupUi(self, Aggregation):
        if not Aggregation.objectName():
            Aggregation.setObjectName(u"Aggregation")
        Aggregation.resize(640, 184)
        self.layout_main = QVBoxLayout(Aggregation)
        self.layout_main.setObjectName(u"layout_main")
        self.widget_group_attribute = AttributeSelector(Aggregation)
        self.widget_group_attribute.setObjectName(u"widget_group_attribute")

        self.layout_main.addWidget(self.widget_group_attribute)

        self.widget_ident_attribute = AttributeSelector(Aggregation)
        self.widget_ident_attribute.setObjectName(u"widget_ident_attribute")

        self.layout_main.addWidget(self.widget_ident_attribute)

        self.widget_import = FileSelector(Aggregation)
        self.widget_import.setObjectName(u"widget_import")

        self.layout_main.addWidget(self.widget_import)

        self.widget_export = FileSelector(Aggregation)
        self.widget_export.setObjectName(u"widget_export")

        self.layout_main.addWidget(self.widget_export)

        self.scrollArea = QScrollArea(Aggregation)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 620, 70))
        self.layout_progress_bar = QVBoxLayout(self.scrollAreaWidgetContents)
        self.layout_progress_bar.setObjectName(u"layout_progress_bar")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layout_main.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(Aggregation)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel)

        self.layout_main.addWidget(self.buttonBox)


        self.retranslateUi(Aggregation)

        QMetaObject.connectSlotsByName(Aggregation)
    # setupUi

    def retranslateUi(self, Aggregation):
        Aggregation.setWindowTitle(QCoreApplication.translate("Aggregation", u"Form", None))
    # retranslateUi

