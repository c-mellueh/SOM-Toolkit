# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 122)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_group_attribute = AttributeSelector(Form)
        self.widget_group_attribute.setObjectName(u"widget_group_attribute")

        self.verticalLayout.addWidget(self.widget_group_attribute)

        self.widget_ident_attribute = AttributeSelector(Form)
        self.widget_ident_attribute.setObjectName(u"widget_ident_attribute")

        self.verticalLayout.addWidget(self.widget_ident_attribute)

        self.widget_import = FileSelector(Form)
        self.widget_import.setObjectName(u"widget_import")

        self.verticalLayout.addWidget(self.widget_import)

        self.widget_export = FileSelector(Form)
        self.widget_export.setObjectName(u"widget_export")

        self.verticalLayout.addWidget(self.widget_export)

        self.widget_progress_bar = Progressbar(Form)
        self.widget_progress_bar.setObjectName(u"widget_progress_bar")

        self.verticalLayout.addWidget(self.widget_progress_bar)

        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply | QDialogButtonBox.Cancel)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi
