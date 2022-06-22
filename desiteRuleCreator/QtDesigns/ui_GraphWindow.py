# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GraphWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QPushButton, QSizePolicy, QWidget)

class Ui_GraphView(object):
    def setupUi(self, GraphView):
        if not GraphView.objectName():
            GraphView.setObjectName(u"GraphView")
        GraphView.resize(825, 576)
        self.gridLayout = QGridLayout(GraphView)
        self.gridLayout.setObjectName(u"gridLayout")
        self.combo_box = QComboBox(GraphView)
        self.combo_box.setObjectName(u"combo_box")

        self.gridLayout.addWidget(self.combo_box, 0, 0, 1, 1)

        self.button_reload = QPushButton(GraphView)
        self.button_reload.setObjectName(u"button_reload")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_reload.sizePolicy().hasHeightForWidth())
        self.button_reload.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.button_reload, 0, 1, 1, 1)

        self.graphicsView = QGraphicsView(GraphView)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 2)


        self.retranslateUi(GraphView)

        QMetaObject.connectSlotsByName(GraphView)
    # setupUi

    def retranslateUi(self, GraphView):
        GraphView.setWindowTitle(QCoreApplication.translate("GraphView", u"Form", None))
        self.button_reload.setText(QCoreApplication.translate("GraphView", u"R", None))
    # retranslateUi

