# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(281, 198)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.check_box_boolean_values = QCheckBox(SettingsDialog)
        self.check_box_boolean_values.setObjectName("check_box_boolean_values")
        self.check_box_boolean_values.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_boolean_values)

        self.check_box_regex = QCheckBox(SettingsDialog)
        self.check_box_regex.setObjectName("check_box_regex")
        self.check_box_regex.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_regex)

        self.check_box_range = QCheckBox(SettingsDialog)
        self.check_box_range.setObjectName("check_box_range")
        self.check_box_range.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_range)

        self.check_box_existing_properties = QCheckBox(SettingsDialog)
        self.check_box_existing_properties.setObjectName(
            "check_box_existing_properties"
        )
        self.check_box_existing_properties.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft
        )

        self.verticalLayout.addWidget(self.check_box_existing_properties)

        self.check_box_color = QCheckBox(SettingsDialog)
        self.check_box_color.setObjectName("check_box_color")
        self.check_box_color.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.check_box_color.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.check_box_color)

        self.check_box_class_filter = QCheckBox(SettingsDialog)
        self.check_box_class_filter.setObjectName("check_box_class_filter")
        self.check_box_class_filter.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout.addWidget(self.check_box_class_filter)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)

    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(
            QCoreApplication.translate("SettingsDialog", "Dialog", None)
        )
        self.check_box_boolean_values.setText(
            QCoreApplication.translate("SettingsDialog", "show IfcBoolean", None)
        )
        self.check_box_regex.setText(
            QCoreApplication.translate("SettingsDialog", "show RegEx", None)
        )
        self.check_box_range.setText(
            QCoreApplication.translate("SettingsDialog", "show Range", None)
        )
        self.check_box_existing_properties.setText(
            QCoreApplication.translate("SettingsDialog", "show allready Existing", None)
        )
        self.check_box_color.setText(
            QCoreApplication.translate("SettingsDialog", "color Data", None)
        )
        self.check_box_class_filter.setText(
            QCoreApplication.translate(
                "SettingsDialog", "filter by Usecase/Phase", None
            )
        )

    # retranslateUi
