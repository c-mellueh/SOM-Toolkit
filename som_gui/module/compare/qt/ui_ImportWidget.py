# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QAbstractButton,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(500, 78)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(500, 0))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_top = QHBoxLayout()
        self.layout_top.setObjectName("layout_top")
        self.layout_input = QHBoxLayout()
        self.layout_input.setObjectName("layout_input")
        self.line_edit = QLineEdit(Dialog)
        self.line_edit.setObjectName("line_edit")

        self.layout_input.addWidget(self.line_edit)

        self.button = QPushButton(Dialog)
        self.button.setObjectName("button")
        self.button.setMinimumSize(QSize(25, 0))
        self.button.setMaximumSize(QSize(25, 16777215))

        self.layout_input.addWidget(self.button)

        self.layout_top.addLayout(self.layout_input)

        self.horizontalLayout.addLayout(self.layout_top)

        self.button_switch = QPushButton(Dialog)
        self.button_switch.setObjectName("button_switch")
        self.button_switch.setMinimumSize(QSize(25, 0))
        self.button_switch.setMaximumSize(QSize(25, 16777215))
        self.button_switch.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout.addWidget(self.button_switch)

        self.layout_bottom = QHBoxLayout()
        self.layout_bottom.setObjectName("layout_bottom")
        self.label_project = QLabel(Dialog)
        self.label_project.setObjectName("label_project")

        self.layout_bottom.addWidget(self.label_project)

        self.horizontalLayout.addLayout(self.layout_bottom)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Dialog", None))
        self.button.setText(QCoreApplication.translate("Dialog", "...", None))
        self.button_switch.setText(QCoreApplication.translate("Dialog", "SW", None))
        self.label_project.setText(
            QCoreApplication.translate("Dialog", "TextLabel", None)
        )

    # retranslateUi
