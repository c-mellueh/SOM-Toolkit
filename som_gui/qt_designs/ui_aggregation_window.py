# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AggregationWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
    QHBoxLayout, QPushButton, QSizePolicy, QToolButton,
    QWidget)

class Ui_GraphView(object):
    def setupUi(self, GraphView):
        if not GraphView.objectName():
            GraphView.setObjectName(u"GraphView")
        GraphView.resize(1236, 740)
        self.gridLayout = QGridLayout(GraphView)
        self.gridLayout.setObjectName(u"gridLayout")
        self.combo_box = QComboBox(GraphView)
        self.combo_box.setObjectName(u"combo_box")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_box.sizePolicy().hasHeightForWidth())
        self.combo_box.setSizePolicy(sizePolicy)
        self.combo_box.setInsertPolicy(QComboBox.InsertAlphabetically)

        self.gridLayout.addWidget(self.combo_box, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_filter = QToolButton(GraphView)
        self.button_filter.setObjectName(u"button_filter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_filter.sizePolicy().hasHeightForWidth())
        self.button_filter.setSizePolicy(sizePolicy1)
        self.button_filter.setMinimumSize(QSize(24, 0))
        self.button_filter.setMaximumSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.button_filter)

        self.button_add = QPushButton(GraphView)
        self.button_add.setObjectName(u"button_add")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.button_add.sizePolicy().hasHeightForWidth())
        self.button_add.setSizePolicy(sizePolicy2)
        self.button_add.setMaximumSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.button_add)

        self.button_delete = QPushButton(GraphView)
        self.button_delete.setObjectName(u"button_delete")
        sizePolicy2.setHeightForWidth(self.button_delete.sizePolicy().hasHeightForWidth())
        self.button_delete.setSizePolicy(sizePolicy2)
        self.button_delete.setMaximumSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.button_delete)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.graphicsView = QGraphicsView(GraphView)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 2)


        self.retranslateUi(GraphView)

        QMetaObject.connectSlotsByName(GraphView)
    # setupUi

    def retranslateUi(self, GraphView):
        GraphView.setWindowTitle(QCoreApplication.translate("GraphView", u"Graphs", None))
#if QT_CONFIG(tooltip)
        self.button_filter.setToolTip(QCoreApplication.translate("GraphView", u"Diagramme Filtern", None))
#endif // QT_CONFIG(tooltip)
        self.button_filter.setText(QCoreApplication.translate("GraphView", u"...", None))
#if QT_CONFIG(tooltip)
        self.button_add.setToolTip(QCoreApplication.translate("GraphView", u"Diagramm Hinzuf\u00fcgen", None))
#endif // QT_CONFIG(tooltip)
        self.button_add.setText(QCoreApplication.translate("GraphView", u"+", None))
#if QT_CONFIG(tooltip)
        self.button_delete.setToolTip(QCoreApplication.translate("GraphView", u"Diagramm L\u00f6schen", None))
#endif // QT_CONFIG(tooltip)
        self.button_delete.setText(QCoreApplication.translate("GraphView", u"-", None))
    # retranslateUi

