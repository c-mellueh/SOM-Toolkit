# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QToolBox,
    QVBoxLayout,
    QWidget,
)


class Ui_BSDD(object):
    def setupUi(self, BSDD):
        if not BSDD.objectName():
            BSDD.setObjectName("BSDD")
        BSDD.resize(640, 480)
        self.verticalLayout = QVBoxLayout(BSDD)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QToolBox(BSDD)
        self.toolBox.setObjectName("toolBox")

        self.verticalLayout.addWidget(self.toolBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_export_path = QLineEdit(BSDD)
        self.le_export_path.setObjectName("le_export_path")

        self.horizontalLayout.addWidget(self.le_export_path)

        self.bu_select_path = QPushButton(BSDD)
        self.bu_select_path.setObjectName("bu_select_path")
        self.bu_select_path.setMaximumSize(QSize(24, 16777215))

        self.horizontalLayout.addWidget(self.bu_select_path)

        self.bu_run = QPushButton(BSDD)
        self.bu_run.setObjectName("bu_run")

        self.horizontalLayout.addWidget(self.bu_run)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(BSDD)

        self.toolBox.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(BSDD)

    # setupUi

    def retranslateUi(self, BSDD):
        BSDD.setWindowTitle(QCoreApplication.translate("BSDD", "Form", None))
        self.le_export_path.setPlaceholderText(
            QCoreApplication.translate("BSDD", "export path", None)
        )
        self.bu_select_path.setText(QCoreApplication.translate("BSDD", "...", None))
        self.bu_run.setText(QCoreApplication.translate("BSDD", "Run", None))

    # retranslateUi
