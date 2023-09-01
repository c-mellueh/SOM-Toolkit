# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProjectPhaseWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QHeaderView,
    QSizePolicy, QSplitter, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1341, 550)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.object_tree = QTreeWidget(self.splitter)
        self.object_tree.setObjectName(u"object_tree")
        self.splitter.addWidget(self.object_tree)
        self.property_set_tree = QTreeWidget(self.splitter)
        self.property_set_tree.setObjectName(u"property_set_tree")
        self.splitter.addWidget(self.property_set_tree)

        self.verticalLayout.addWidget(self.splitter)

        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Leistungsphase", None))
        ___qtreewidgetitem = self.object_tree.headerItem()
        ___qtreewidgetitem.setText(10, QCoreApplication.translate("Form", u"LP9", None));
        ___qtreewidgetitem.setText(9, QCoreApplication.translate("Form", u"LP8", None));
        ___qtreewidgetitem.setText(8, QCoreApplication.translate("Form", u"LP7", None));
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("Form", u"LP6", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("Form", u"LP5", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("Form", u"LP4", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Form", u"LP3", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Form", u"LP2", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Form", u"LP1", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"Identifier", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Name", None));
        ___qtreewidgetitem1 = self.property_set_tree.headerItem()
        ___qtreewidgetitem1.setText(9, QCoreApplication.translate("Form", u"LP9", None));
        ___qtreewidgetitem1.setText(8, QCoreApplication.translate("Form", u"LP8", None));
        ___qtreewidgetitem1.setText(7, QCoreApplication.translate("Form", u"LP7", None));
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("Form", u"LP6", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("Form", u"LP5", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("Form", u"LP4", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Form", u"LP3", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Form", u"LP2", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Form", u"LP1", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Form", u"Name", None));
    # retranslateUi

