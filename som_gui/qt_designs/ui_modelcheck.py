# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Modelcheck.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Modelcheck(object):
    def setupUi(self, Modelcheck):
        if not Modelcheck.objectName():
            Modelcheck.setObjectName(u"Modelcheck")
        Modelcheck.resize(1271, 796)
        self.action_desite_js = QAction(Modelcheck)
        self.action_desite_js.setObjectName(u"action_desite_js")
        self.action_desite_attributes = QAction(Modelcheck)
        self.action_desite_attributes.setObjectName(u"action_desite_attributes")
        self.action_desite_csv = QAction(Modelcheck)
        self.action_desite_csv.setObjectName(u"action_desite_csv")
        self.action_bimcollab_zoom = QAction(Modelcheck)
        self.action_bimcollab_zoom.setObjectName(u"action_bimcollab_zoom")
        self.action_desite_fast = QAction(Modelcheck)
        self.action_desite_fast.setObjectName(u"action_desite_fast")
        self.action_ids = QAction(Modelcheck)
        self.action_ids.setObjectName(u"action_ids")
        self.centralwidget = QWidget(Modelcheck)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout.addLayout(self.horizontalLayout)

        Modelcheck.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Modelcheck)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1271, 22))
        self.menuDesite = QMenu(self.menubar)
        self.menuDesite.setObjectName(u"menuDesite")
        self.menuBIMcollab_ZOOM = QMenu(self.menubar)
        self.menuBIMcollab_ZOOM.setObjectName(u"menuBIMcollab_ZOOM")
        self.menuBuildingSmart = QMenu(self.menubar)
        self.menuBuildingSmart.setObjectName(u"menuBuildingSmart")
        Modelcheck.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuDesite.menuAction())
        self.menubar.addAction(self.menuBIMcollab_ZOOM.menuAction())
        self.menubar.addAction(self.menuBuildingSmart.menuAction())
        self.menuDesite.addAction(self.action_desite_js)
        self.menuDesite.addAction(self.action_desite_attributes)
        self.menuDesite.addAction(self.action_desite_csv)
        self.menuDesite.addAction(self.action_desite_fast)
        self.menuBIMcollab_ZOOM.addAction(self.action_bimcollab_zoom)
        self.menuBuildingSmart.addAction(self.action_ids)

        self.retranslateUi(Modelcheck)

        QMetaObject.connectSlotsByName(Modelcheck)
    # setupUi

    def retranslateUi(self, Modelcheck):
        Modelcheck.setWindowTitle(QCoreApplication.translate("Modelcheck", u"MainWindow", None))
        self.action_desite_js.setText(QCoreApplication.translate("Modelcheck", u"Export Javascript Rules", None))
        self.action_desite_attributes.setText(QCoreApplication.translate("Modelcheck", u"Export Attribute Rules", None))
        self.action_desite_csv.setText(QCoreApplication.translate("Modelcheck", u"Export Modelcheck-CSV", None))
        self.action_bimcollab_zoom.setText(QCoreApplication.translate("Modelcheck", u"Export Modelcheck", None))
        self.action_desite_fast.setText(QCoreApplication.translate("Modelcheck", u"Export Fast JS Rules", None))
        self.action_ids.setText(QCoreApplication.translate("Modelcheck", u"IDS", None))
        self.menuDesite.setTitle(QCoreApplication.translate("Modelcheck", u"Desite", None))
        self.menuBIMcollab_ZOOM.setTitle(QCoreApplication.translate("Modelcheck", u"BIMcollab ZOOM", None))
        self.menuBuildingSmart.setTitle(QCoreApplication.translate("Modelcheck", u"BuildingSmart", None))
    # retranslateUi

