# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1161, 525)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.action_file_new = QAction(MainWindow)
        self.action_file_new.setObjectName(u"action_file_new")
        self.action_file_Save = QAction(MainWindow)
        self.action_file_Save.setObjectName(u"action_file_Save")
        self.action_file_Save_As = QAction(MainWindow)
        self.action_file_Save_As.setObjectName(u"action_file_Save_As")
        self.action_file_Open = QAction(MainWindow)
        self.action_file_Open.setObjectName(u"action_file_Open")
        self.action_desite_Settings = QAction(MainWindow)
        self.action_desite_Settings.setObjectName(u"action_desite_Settings")
        self.action_desite_Export = QAction(MainWindow)
        self.action_desite_Export.setObjectName(u"action_desite_Export")
        self.verticalLayout_main = QWidget(MainWindow)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.horizontalLayout_2 = QHBoxLayout(self.verticalLayout_main)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_objects = QVBoxLayout()
        self.verticalLayout_objects.setObjectName(u"verticalLayout_objects")
        self.gridLayout_objects = QGridLayout()
        self.gridLayout_objects.setObjectName(u"gridLayout_objects")
        self.lineEdit_ident_value = QLineEdit(self.verticalLayout_main)
        self.lineEdit_ident_value.setObjectName(u"lineEdit_ident_value")
        self.lineEdit_ident_value.setFrame(False)
        self.lineEdit_ident_value.setEchoMode(QLineEdit.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_value, 1, 3, 1, 1)

        self.label_object_name = QLabel(self.verticalLayout_main)
        self.label_object_name.setObjectName(u"label_object_name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_object_name.sizePolicy().hasHeightForWidth())
        self.label_object_name.setSizePolicy(sizePolicy)
        self.label_object_name.setMinimumSize(QSize(30, 0))
        self.label_object_name.setLineWidth(1)

        self.gridLayout_objects.addWidget(self.label_object_name, 0, 0, 1, 1)

        self.lineEdit_ident_attribute = QLineEdit(self.verticalLayout_main)
        self.lineEdit_ident_attribute.setObjectName(u"lineEdit_ident_attribute")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_ident_attribute.sizePolicy().hasHeightForWidth())
        self.lineEdit_ident_attribute.setSizePolicy(sizePolicy1)
        self.lineEdit_ident_attribute.setFrame(False)
        self.lineEdit_ident_attribute.setEchoMode(QLineEdit.Normal)
        self.lineEdit_ident_attribute.setCursorMoveStyle(Qt.LogicalMoveStyle)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_attribute, 1, 2, 1, 1)

        self.label_Ident = QLabel(self.verticalLayout_main)
        self.label_Ident.setObjectName(u"label_Ident")

        self.gridLayout_objects.addWidget(self.label_Ident, 1, 0, 1, 1)

        self.lineEdit_ident_pSet = QLineEdit(self.verticalLayout_main)
        self.lineEdit_ident_pSet.setObjectName(u"lineEdit_ident_pSet")
        sizePolicy1.setHeightForWidth(self.lineEdit_ident_pSet.sizePolicy().hasHeightForWidth())
        self.lineEdit_ident_pSet.setSizePolicy(sizePolicy1)
        self.lineEdit_ident_pSet.setFrame(False)
        self.lineEdit_ident_pSet.setEchoMode(QLineEdit.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_ident_pSet, 1, 1, 1, 1)

        self.lineEdit_object_name = QLineEdit(self.verticalLayout_main)
        self.lineEdit_object_name.setObjectName(u"lineEdit_object_name")
        sizePolicy1.setHeightForWidth(self.lineEdit_object_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_object_name.setSizePolicy(sizePolicy1)
        self.lineEdit_object_name.setFrame(False)
        self.lineEdit_object_name.setEchoMode(QLineEdit.Normal)

        self.gridLayout_objects.addWidget(self.lineEdit_object_name, 0, 1, 1, 1)

        self.horizontalLayout_object_button = QHBoxLayout()
        self.horizontalLayout_object_button.setObjectName(u"horizontalLayout_object_button")
        self.button_objects_update = QPushButton(self.verticalLayout_main)
        self.button_objects_update.setObjectName(u"button_objects_update")

        self.horizontalLayout_object_button.addWidget(self.button_objects_update)

        self.button_objects_delete = QPushButton(self.verticalLayout_main)
        self.button_objects_delete.setObjectName(u"button_objects_delete")

        self.horizontalLayout_object_button.addWidget(self.button_objects_delete)

        self.button_objects_add = QPushButton(self.verticalLayout_main)
        self.button_objects_add.setObjectName(u"button_objects_add")

        self.horizontalLayout_object_button.addWidget(self.button_objects_add)


        self.gridLayout_objects.addLayout(self.horizontalLayout_object_button, 0, 2, 1, 2)


        self.verticalLayout_objects.addLayout(self.gridLayout_objects)


        self.horizontalLayout_2.addLayout(self.verticalLayout_objects)

        self.horizontalLayout_pSet = QGroupBox(self.verticalLayout_main)
        self.horizontalLayout_pSet.setObjectName(u"horizontalLayout_pSet")
        self.verticalLayout_2 = QVBoxLayout(self.horizontalLayout_pSet)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout_pSet = QGridLayout()
        self.gridLayout_pSet.setObjectName(u"gridLayout_pSet")
        self.label_pSet_name = QLabel(self.horizontalLayout_pSet)
        self.label_pSet_name.setObjectName(u"label_pSet_name")
        self.label_pSet_name.setMinimumSize(QSize(30, 0))

        self.gridLayout_pSet.addWidget(self.label_pSet_name, 0, 0, 1, 1)

        self.lineEdit_pSet_name = QLineEdit(self.horizontalLayout_pSet)
        self.lineEdit_pSet_name.setObjectName(u"lineEdit_pSet_name")
        self.lineEdit_pSet_name.setFrame(False)

        self.gridLayout_pSet.addWidget(self.lineEdit_pSet_name, 0, 1, 1, 1)

        self.horizontalLayout_pSet_button = QHBoxLayout()
        self.horizontalLayout_pSet_button.setObjectName(u"horizontalLayout_pSet_button")
        self.button_Pset_rename = QPushButton(self.horizontalLayout_pSet)
        self.button_Pset_rename.setObjectName(u"button_Pset_rename")

        self.horizontalLayout_pSet_button.addWidget(self.button_Pset_rename)

        self.button_Pset_delete = QPushButton(self.horizontalLayout_pSet)
        self.button_Pset_delete.setObjectName(u"button_Pset_delete")

        self.horizontalLayout_pSet_button.addWidget(self.button_Pset_delete)

        self.button_Pset_add = QPushButton(self.horizontalLayout_pSet)
        self.button_Pset_add.setObjectName(u"button_Pset_add")

        self.horizontalLayout_pSet_button.addWidget(self.button_Pset_add)


        self.gridLayout_pSet.addLayout(self.horizontalLayout_pSet_button, 1, 0, 1, 2)


        self.verticalLayout_2.addLayout(self.gridLayout_pSet)

        self.tableWidget_inherited = QTableWidget(self.horizontalLayout_pSet)
        if (self.tableWidget_inherited.columnCount() < 2):
            self.tableWidget_inherited.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_inherited.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_inherited.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget_inherited.rowCount() < 1):
            self.tableWidget_inherited.setRowCount(1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_inherited.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_inherited.setItem(0, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_inherited.setItem(0, 1, __qtablewidgetitem4)
        self.tableWidget_inherited.setObjectName(u"tableWidget_inherited")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget_inherited.sizePolicy().hasHeightForWidth())
        self.tableWidget_inherited.setSizePolicy(sizePolicy2)
        self.tableWidget_inherited.setFocusPolicy(Qt.StrongFocus)
        self.tableWidget_inherited.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_inherited.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_inherited.setSortingEnabled(True)
        self.tableWidget_inherited.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableWidget_inherited.verticalHeader().setVisible(False)
        self.tableWidget_inherited.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_2.addWidget(self.tableWidget_inherited)


        self.horizontalLayout_2.addWidget(self.horizontalLayout_pSet)

        MainWindow.setCentralWidget(self.verticalLayout_main)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1161, 18))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuDesite = QMenu(self.menubar)
        self.menuDesite.setObjectName(u"menuDesite")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDesite.menuAction())
        self.menuFile.addAction(self.action_file_new)
        self.menuFile.addAction(self.action_file_Save)
        self.menuFile.addAction(self.action_file_Save_As)
        self.menuFile.addAction(self.action_file_Open)
        self.menuDesite.addAction(self.action_desite_Settings)
        self.menuDesite.addAction(self.action_desite_Export)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_file_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.action_file_Save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.action_file_Save_As.setText(QCoreApplication.translate("MainWindow", u"Save As ...", None))
        self.action_file_Open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.action_desite_Settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.action_desite_Export.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.lineEdit_ident_value.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Value", None))
        self.label_object_name.setText(QCoreApplication.translate("MainWindow", u"Object", None))
        self.lineEdit_ident_attribute.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Attribute", None))
        self.label_Ident.setText(QCoreApplication.translate("MainWindow", u"Ident", None))
        self.lineEdit_ident_pSet.setPlaceholderText(QCoreApplication.translate("MainWindow", u"PropertySet", None))
        self.lineEdit_object_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.button_objects_update.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.button_objects_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.button_objects_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.horizontalLayout_pSet.setTitle(QCoreApplication.translate("MainWindow", u"PropertySet", None))
        self.label_pSet_name.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.button_Pset_rename.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.button_Pset_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.button_Pset_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        ___qtablewidgetitem = self.tableWidget_inherited.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"PropertySet", None));
        ___qtablewidgetitem1 = self.tableWidget_inherited.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"InheritedBy", None));
        ___qtablewidgetitem2 = self.tableWidget_inherited.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Test", None));

        __sortingEnabled = self.tableWidget_inherited.isSortingEnabled()
        self.tableWidget_inherited.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.tableWidget_inherited.item(0, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"BestandsdatenqVerkehrsanlagen", None));
        ___qtablewidgetitem4 = self.tableWidget_inherited.item(0, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Verkehrsanlagen", None));
        self.tableWidget_inherited.setSortingEnabled(__sortingEnabled)

        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuDesite.setTitle(QCoreApplication.translate("MainWindow", u"Desite", None))
    # retranslateUi

