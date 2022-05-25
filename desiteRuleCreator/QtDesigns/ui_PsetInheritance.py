# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PropertySetInheritance.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_PsetInherWidget(object):
    def setupUi(self, PsetInherWidget):
        if not PsetInherWidget.objectName():
            PsetInherWidget.setObjectName(u"PsetInherWidget")
        PsetInherWidget.resize(907, 465)
        self.gridLayout = QGridLayout(PsetInherWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.push_button_edit = QPushButton(PsetInherWidget)
        self.push_button_edit.setObjectName(u"push_button_edit")

        self.horizontalLayout.addWidget(self.push_button_edit)

        self.push_button_add_pset = QPushButton(PsetInherWidget)
        self.push_button_add_pset.setObjectName(u"push_button_add_pset")

        self.horizontalLayout.addWidget(self.push_button_add_pset)

        self.push_button_remove_pset = QPushButton(PsetInherWidget)
        self.push_button_remove_pset.setObjectName(u"push_button_remove_pset")

        self.horizontalLayout.addWidget(self.push_button_remove_pset)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.label = QLabel(PsetInherWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(PsetInherWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.list_view_pset = QListWidget(PsetInherWidget)
        QListWidgetItem(self.list_view_pset)
        QListWidgetItem(self.list_view_pset)
        QListWidgetItem(self.list_view_pset)
        self.list_view_pset.setObjectName(u"list_view_pset")

        self.gridLayout.addWidget(self.list_view_pset, 1, 0, 1, 1)

        self.list_view_existance = QListWidget(PsetInherWidget)
        QListWidgetItem(self.list_view_existance)
        QListWidgetItem(self.list_view_existance)
        QListWidgetItem(self.list_view_existance)
        QListWidgetItem(self.list_view_existance)
        self.list_view_existance.setObjectName(u"list_view_existance")

        self.gridLayout.addWidget(self.list_view_existance, 1, 1, 1, 1)


        self.retranslateUi(PsetInherWidget)

        QMetaObject.connectSlotsByName(PsetInherWidget)
    # setupUi

    def retranslateUi(self, PsetInherWidget):
        PsetInherWidget.setWindowTitle(QCoreApplication.translate("PsetInherWidget", u"Form", None))
        self.push_button_edit.setText(QCoreApplication.translate("PsetInherWidget", u"Edit", None))
        self.push_button_add_pset.setText(QCoreApplication.translate("PsetInherWidget", u"+", None))
        self.push_button_remove_pset.setText(QCoreApplication.translate("PsetInherWidget", u"-", None))
        self.label.setText(QCoreApplication.translate("PsetInherWidget", u"PropertySet", None))
        self.label_2.setText(QCoreApplication.translate("PsetInherWidget", u"Inherits to:", None))

        __sortingEnabled = self.list_view_pset.isSortingEnabled()
        self.list_view_pset.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_view_pset.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("PsetInherWidget", u"ADSD", None));
        ___qlistwidgetitem1 = self.list_view_pset.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("PsetInherWidget", u"ASFASF", None));
        ___qlistwidgetitem2 = self.list_view_pset.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("PsetInherWidget", u"ASF", None));
        self.list_view_pset.setSortingEnabled(__sortingEnabled)


        __sortingEnabled1 = self.list_view_existance.isSortingEnabled()
        self.list_view_existance.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.list_view_existance.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("PsetInherWidget", u"ASFASDFQWEFD", None));
        ___qlistwidgetitem4 = self.list_view_existance.item(1)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("PsetInherWidget", u"WQFDQWF", None));
        ___qlistwidgetitem5 = self.list_view_existance.item(2)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("PsetInherWidget", u"QWDF", None));
        ___qlistwidgetitem6 = self.list_view_existance.item(3)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("PsetInherWidget", u"QWD", None));
        self.list_view_existance.setSortingEnabled(__sortingEnabled1)

    # retranslateUi

