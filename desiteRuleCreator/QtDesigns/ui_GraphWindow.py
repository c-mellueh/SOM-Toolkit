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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QSizePolicy,
    QWidget)

class Ui_GraphView(object):
    def setupUi(self, GraphView):
        if not GraphView.objectName():
            GraphView.setObjectName(u"GraphView")
        GraphView.resize(1406, 766)
        self.gridLayout = QGridLayout(GraphView)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(GraphView)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)


        self.retranslateUi(GraphView)

        QMetaObject.connectSlotsByName(GraphView)
    # setupUi

    def retranslateUi(self, GraphView):
        GraphView.setWindowTitle(QCoreApplication.translate("GraphView", u"Form", None))
    # retranslateUi

