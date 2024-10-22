# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsPath.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
                               QSizePolicy, QWidget)


class Ui_Project(object):
    def setupUi(self, Project):
        if not Project.objectName():
            Project.setObjectName(u"Project")
        Project.resize(621, 96)
        self.formLayout = QFormLayout(Project)
        self.formLayout.setObjectName(u"formLayout")
        self.la_project_path = QLabel(Project)
        self.la_project_path.setObjectName(u"la_project_path")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.la_project_path)

        self.le_project_path = QLineEdit(Project)
        self.le_project_path.setObjectName(u"le_project_path")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_project_path)

        self.le_save_path = QLineEdit(Project)
        self.le_save_path.setObjectName(u"le_save_path")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.le_save_path)

        self.la_save_path = QLabel(Project)
        self.la_save_path.setObjectName(u"la_save_path")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.la_save_path)

        self.le_open_path = QLineEdit(Project)
        self.le_open_path.setObjectName(u"le_open_path")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_open_path)

        self.la_open_path = QLabel(Project)
        self.la_open_path.setObjectName(u"la_open_path")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.la_open_path)

        self.retranslateUi(Project)

        QMetaObject.connectSlotsByName(Project)
    # setupUi

    def retranslateUi(self, Project):
        Project.setWindowTitle(QCoreApplication.translate("Project", u"Form", None))
        self.la_project_path.setText(QCoreApplication.translate("Project", u"Project Path:", None))
        self.la_save_path.setText(QCoreApplication.translate("Project", u"Save Path:", None))
        self.la_open_path.setText(QCoreApplication.translate("Project", u"Open Path:", None))
    # retranslateUi

