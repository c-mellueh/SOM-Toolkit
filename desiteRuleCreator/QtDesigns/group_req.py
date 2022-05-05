# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'group_name_request.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(456, 105)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pset_name = QtWidgets.QLineEdit(Dialog)
        self.pset_name.setObjectName("pset_name")
        self.gridLayout.addWidget(self.pset_name, 1, 0, 1, 1)
        self.attribute_name = QtWidgets.QLineEdit(Dialog)
        self.attribute_name.setObjectName("attribute_name")
        self.gridLayout.addWidget(self.attribute_name, 1, 1, 1, 1)
        self.attribute_value = QtWidgets.QLineEdit(Dialog)
        self.attribute_value.setObjectName("attribute_value")
        self.gridLayout.addWidget(self.attribute_value, 1, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 2)
        self.group_name = QtWidgets.QLineEdit(Dialog)
        self.group_name.setObjectName("group_name")
        self.gridLayout.addWidget(self.group_name, 0, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pset_name.setPlaceholderText(_translate("Dialog", "PropertySet"))
        self.attribute_name.setPlaceholderText(_translate("Dialog", "Attribute"))
        self.attribute_value.setPlaceholderText(_translate("Dialog", "Value"))
        self.group_name.setPlaceholderText(_translate("Dialog", "Name of object"))
