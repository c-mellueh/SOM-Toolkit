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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QDoubleSpinBox,
                               QGridLayout, QLabel, QSizePolicy, QVBoxLayout,
                               QWidget)

from som_gui.module.util.ui import (FileSelector, Progressbar)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 132)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.dsb_x = QDoubleSpinBox(Form)
        self.dsb_x.setObjectName(u"dsb_x")
        self.dsb_x.setMinimum(-10000000000000000000000.000000000000000)
        self.dsb_x.setMaximum(10000000000000000000000.000000000000000)

        self.gridLayout.addWidget(self.dsb_x, 1, 0, 1, 1)

        self.dsb_y = QDoubleSpinBox(Form)
        self.dsb_y.setObjectName(u"dsb_y")
        self.dsb_y.setMinimum(-10000000000000000000000.000000000000000)
        self.dsb_y.setMaximum(10000000000000000000000.000000000000000)

        self.gridLayout.addWidget(self.dsb_y, 1, 1, 1, 1)

        self.dsb_z = QDoubleSpinBox(Form)
        self.dsb_z.setObjectName(u"dsb_z")
        self.dsb_z.setMinimum(-10000000000000000000000.000000000000000)
        self.dsb_z.setMaximum(10000000000000000000000.000000000000000)

        self.gridLayout.addWidget(self.dsb_z, 1, 2, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.widget_file_selector = FileSelector(Form)
        self.widget_file_selector.setObjectName(u"widget_file_selector")

        self.verticalLayout.addWidget(self.widget_file_selector)

        self.widget_progress_bar = Progressbar(Form)
        self.widget_progress_bar.setObjectName(u"widget_progress_bar")

        self.verticalLayout.addWidget(self.widget_progress_bar)

        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply | QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"X-Verschiebung [m]", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Y-Verschiebung [m]", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Z-Verschieben [m]", None))
    # retranslateUi
