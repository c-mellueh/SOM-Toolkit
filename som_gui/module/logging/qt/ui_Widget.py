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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
                               QSizePolicy, QWidget)

from som_gui.module.util.ui import FileSelector

class Ui_Logging(object):
    def setupUi(self, Logging):
        if not Logging.objectName():
            Logging.setObjectName(u"Logging")
        Logging.resize(640, 102)
        self.formLayout = QFormLayout(Logging)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Logging)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBox = QComboBox(Logging)
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.widget_export = FileSelector(Logging)
        self.widget_export.setObjectName(u"widget_export")
        self.widget_export.setMinimumSize(QSize(0, 50))

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.widget_export)

        self.retranslateUi(Logging)

        QMetaObject.connectSlotsByName(Logging)
    # setupUi

    def retranslateUi(self, Logging):
        Logging.setWindowTitle(QCoreApplication.translate("Logging", u"Form", None))
        self.label.setText(QCoreApplication.translate("Logging", u"Log Level:", None))
    # retranslateUi
