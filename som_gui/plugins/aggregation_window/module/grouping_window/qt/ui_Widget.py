# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QSizePolicy,
                               QVBoxLayout, QWidget)

from som_gui.module.util.ui import (AttributeSelector, FileSelector, Progressbar)

class Ui_Aggregation(object):
    def setupUi(self, Aggregation):
        if not Aggregation.objectName():
            Aggregation.setObjectName(u"Aggregation")
        Aggregation.resize(640, 122)
        self.verticalLayout = QVBoxLayout(Aggregation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_group_attribute = AttributeSelector(Aggregation)
        self.widget_group_attribute.setObjectName(u"widget_group_attribute")

        self.verticalLayout.addWidget(self.widget_group_attribute)

        self.widget_ident_attribute = AttributeSelector(Aggregation)
        self.widget_ident_attribute.setObjectName(u"widget_ident_attribute")

        self.verticalLayout.addWidget(self.widget_ident_attribute)

        self.widget_import = FileSelector(Aggregation)
        self.widget_import.setObjectName(u"widget_import")

        self.verticalLayout.addWidget(self.widget_import)

        self.widget_export = FileSelector(Aggregation)
        self.widget_export.setObjectName(u"widget_export")

        self.verticalLayout.addWidget(self.widget_export)

        self.widget_progress_bar = Progressbar(Aggregation)
        self.widget_progress_bar.setObjectName(u"widget_progress_bar")

        self.verticalLayout.addWidget(self.widget_progress_bar)

        self.buttonBox = QDialogButtonBox(Aggregation)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Apply | QDialogButtonBox.StandardButton.Cancel)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Aggregation)

        QMetaObject.connectSlotsByName(Aggregation)
    # setupUi

    def retranslateUi(self, Aggregation):
        Aggregation.setWindowTitle(QCoreApplication.translate("Aggregation", u"Form", None))
    # retranslateUi

