# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/mesonui-layout/activity_wrap.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Ui_Activity_Wrap_Dialog:
    def setupUi(self, Activity_Wrap_Dialog):
        Activity_Wrap_Dialog.setObjectName("Activity_Wrap_Dialog")
        Activity_Wrap_Dialog.resize(741, 422)
        Activity_Wrap_Dialog.setStyleSheet("")
        self.control_push_ok = QtWidgets.QPushButton(Activity_Wrap_Dialog)
        self.control_push_ok.setGeometry(QtCore.QRect(20, 370, 167, 24))
        self.control_push_ok.setStyleSheet("")
        self.control_push_ok.setObjectName("control_push_ok")
        self.GroupBox = QtWidgets.QGroupBox(Activity_Wrap_Dialog)
        self.GroupBox.setGeometry(QtCore.QRect(0, 0, 741, 361))
        self.GroupBox.setStyleSheet("")
        self.GroupBox.setObjectName("GroupBox")
        self.label_5 = QtWidgets.QLabel(self.GroupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 71, 61))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("")
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/icon/mesonui-icon/wrapdb_logo.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.layoutWidget = QtWidgets.QWidget(self.GroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 130, 701, 32))
        self.layoutWidget.setStyleSheet("")
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.control_push_install = QtWidgets.QPushButton(self.layoutWidget)
        self.control_push_install.setStyleSheet("")
        self.control_push_install.setObjectName("control_push_install")
        self.horizontalLayout.addWidget(self.control_push_install)
        self.control_push_update = QtWidgets.QPushButton(self.layoutWidget)
        self.control_push_update.setStyleSheet("")
        self.control_push_update.setObjectName("control_push_update")
        self.horizontalLayout.addWidget(self.control_push_update)
        self.control_push_info = QtWidgets.QPushButton(self.layoutWidget)
        self.control_push_info.setStyleSheet("")
        self.control_push_info.setObjectName("control_push_info")
        self.horizontalLayout.addWidget(self.control_push_info)
        self.control_push_status = QtWidgets.QPushButton(self.layoutWidget)
        self.control_push_status.setStyleSheet("")
        self.control_push_status.setObjectName("control_push_status")
        self.horizontalLayout.addWidget(self.control_push_status)
        self.edit_wrap_item = QtWidgets.QLineEdit(self.GroupBox)
        self.edit_wrap_item.setGeometry(QtCore.QRect(120, 100, 601, 21))
        self.edit_wrap_item.setClearButtonEnabled(False)
        self.edit_wrap_item.setObjectName("edit_wrap_item")
        self.info = QtWidgets.QPlainTextEdit(self.GroupBox)
        self.info.setGeometry(QtCore.QRect(120, 30, 601, 61))
        self.info.setStyleSheet("")
        self.info.setObjectName("info")
        self.control_push_search = QtWidgets.QPushButton(self.GroupBox)
        self.control_push_search.setGeometry(QtCore.QRect(20, 100, 91, 21))
        self.control_push_search.setStyleSheet("")
        self.control_push_search.setObjectName("control_push_search")
        self.output_console_dashboard = QtWidgets.QGroupBox(self.GroupBox)
        self.output_console_dashboard.setGeometry(QtCore.QRect(0, 170, 741, 191))
        self.output_console_dashboard.setFocusPolicy(QtCore.Qt.NoFocus)
        self.output_console_dashboard.setStyleSheet("")
        self.output_console_dashboard.setObjectName("output_console_dashboard")
        self.output_console = QtWidgets.QPlainTextEdit(self.output_console_dashboard)
        self.output_console.setGeometry(QtCore.QRect(20, 30, 701, 151))
        self.output_console.setStyleSheet("")
        self.output_console.setReadOnly(True)
        self.output_console.setPlainText("")
        self.output_console.setObjectName("output_console")

        self.retranslateUi(Activity_Wrap_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Activity_Wrap_Dialog)

    def retranslateUi(self, Activity_Wrap_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Activity_Wrap_Dialog.setWindowTitle(_translate("Activity_Wrap_Dialog", "WrapDB Tools"))
        self.control_push_ok.setText(_translate("Activity_Wrap_Dialog", "OK"))
        self.GroupBox.setTitle(_translate("Activity_Wrap_Dialog", "Wrap Tools view:"))
        self.control_push_install.setText(_translate("Activity_Wrap_Dialog", "Install"))
        self.control_push_update.setText(_translate("Activity_Wrap_Dialog", "Update"))
        self.control_push_info.setText(_translate("Activity_Wrap_Dialog", "Info"))
        self.control_push_status.setText(_translate("Activity_Wrap_Dialog", "Status"))
        self.edit_wrap_item.setPlaceholderText(_translate("Activity_Wrap_Dialog", "   wrap file name here"))
        self.info.setPlainText(_translate("Activity_Wrap_Dialog", "Wraptool is a subcommand of Meson that allows you to manage your source dependencies using the WrapDB database."))
        self.control_push_search.setText(_translate("Activity_Wrap_Dialog", "Search"))
        self.output_console_dashboard.setTitle(_translate("Activity_Wrap_Dialog", "Output Console:"))

try:
    from . import resource_rc
except ImportError:
    print(f'Resource not found in UI layout Main')
    print(f'Qt version {resource_rc.qt_version}')
