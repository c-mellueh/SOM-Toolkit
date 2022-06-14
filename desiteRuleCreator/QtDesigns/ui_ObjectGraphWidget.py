# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ObjectGraphWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_object_graph_widget(object):
    def setupUi(self, object_graph_widget):
        if not object_graph_widget.objectName():
            object_graph_widget.setObjectName(u"object_graph_widget")
        object_graph_widget.resize(375, 432)
        self.verticalLayout = QVBoxLayout(object_graph_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_object_name = QLabel(object_graph_widget)
        self.label_object_name.setObjectName(u"label_object_name")
        self.label_object_name.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_object_name)

        self.list_widget_property_sets = QListWidget(object_graph_widget)
        self.list_widget_property_sets.setObjectName(u"list_widget_property_sets")

        self.verticalLayout.addWidget(self.list_widget_property_sets)


        self.retranslateUi(object_graph_widget)

        QMetaObject.connectSlotsByName(object_graph_widget)
    # setupUi

    def retranslateUi(self, object_graph_widget):
        object_graph_widget.setWindowTitle(QCoreApplication.translate("object_graph_widget", u"OG", None))
        self.label_object_name.setText(QCoreApplication.translate("object_graph_widget", u"TextLabel", None))
    # retranslateUi

