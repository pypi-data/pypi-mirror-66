# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/mesonui-layout/activity_install.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Ui_Activity_Dist_Dialog:
    def setupUi(self, Activity_Dist_Dialog):
        Activity_Dist_Dialog.setObjectName("Activity_Dist_Dialog")
        Activity_Dist_Dialog.resize(741, 420)
        Activity_Dist_Dialog.setStyleSheet("")
        self.GroupBox = QtWidgets.QGroupBox(Activity_Dist_Dialog)
        self.GroupBox.setGeometry(QtCore.QRect(0, 0, 741, 351))
        self.GroupBox.setStyleSheet("")
        self.GroupBox.setObjectName("GroupBox")
        self.label_5 = QtWidgets.QLabel(self.GroupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 81, 71))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("")
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/icon/mesonui-icon/meson_modern.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.GroupBox)
        self.label.setGeometry(QtCore.QRect(30, 163, 121, 16))
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.combo_no_rebuild = QtWidgets.QComboBox(self.GroupBox)
        self.combo_no_rebuild.setGeometry(QtCore.QRect(160, 160, 191, 26))
        self.combo_no_rebuild.setStyleSheet("")
        self.combo_no_rebuild.setObjectName("combo_no_rebuild")
        self.label_2 = QtWidgets.QLabel(self.GroupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 200, 121, 16))
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.combo_only_changed = QtWidgets.QComboBox(self.GroupBox)
        self.combo_only_changed.setGeometry(QtCore.QRect(160, 200, 191, 26))
        self.combo_only_changed.setStyleSheet("")
        self.combo_only_changed.setObjectName("combo_only_changed")
        self.label_3 = QtWidgets.QLabel(self.GroupBox)
        self.label_3.setGeometry(QtCore.QRect(360, 160, 351, 16))
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.GroupBox)
        self.label_4.setGeometry(QtCore.QRect(360, 197, 371, 31))
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.info = QtWidgets.QPlainTextEdit(self.GroupBox)
        self.info.setGeometry(QtCore.QRect(140, 30, 571, 111))
        self.info.setStyleSheet("")
        self.info.setReadOnly(True)
        self.info.setObjectName("info")
        self.label_6 = QtWidgets.QLabel(self.GroupBox)
        self.label_6.setGeometry(QtCore.QRect(360, 237, 371, 31))
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.combo_quiet = QtWidgets.QComboBox(self.GroupBox)
        self.combo_quiet.setGeometry(QtCore.QRect(160, 240, 191, 26))
        self.combo_quiet.setStyleSheet("")
        self.combo_quiet.setObjectName("combo_quiet")
        self.label_7 = QtWidgets.QLabel(self.GroupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 240, 121, 16))
        self.label_7.setStyleSheet("")
        self.label_7.setObjectName("label_7")
        self.layoutWidget = QtWidgets.QWidget(Activity_Dist_Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(370, 360, 368, 32))
        self.layoutWidget.setStyleSheet("")
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.control_push_do_update = QtWidgets.QPushButton(self.layoutWidget)
        self.control_push_do_update.setStyleSheet("")
        self.control_push_do_update.setObjectName("control_push_do_update")
        self.horizontalLayout.addWidget(self.control_push_do_update)
        self.control_push_do_install = QtWidgets.QPushButton(self.layoutWidget)
        self.control_push_do_install.setStyleSheet("")
        self.control_push_do_install.setObjectName("control_push_do_install")
        self.horizontalLayout.addWidget(self.control_push_do_install)
        self.control_push_no_install = QtWidgets.QPushButton(Activity_Dist_Dialog)
        self.control_push_no_install.setGeometry(QtCore.QRect(20, 365, 168, 24))
        self.control_push_no_install.setStyleSheet("")
        self.control_push_no_install.setObjectName("control_push_no_install")

        self.retranslateUi(Activity_Dist_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Activity_Dist_Dialog)

    def retranslateUi(self, Activity_Dist_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Activity_Dist_Dialog.setWindowTitle(_translate("Activity_Dist_Dialog", "Meson Build Installer"))
        self.GroupBox.setTitle(_translate("Activity_Dist_Dialog", "Installer View:"))
        self.label.setText(_translate("Activity_Dist_Dialog", "no rebuild:"))
        self.label_2.setText(_translate("Activity_Dist_Dialog", "only changed:"))
        self.label_3.setText(_translate("Activity_Dist_Dialog", "Do not rebuild before installing."))
        self.label_4.setText(_translate("Activity_Dist_Dialog", "Only overwrite files that are older than the copied file."))
        self.info.setPlainText(_translate("Activity_Dist_Dialog", "Installing the built software is just as simple. Even Meson-UI supports this feature in the background:"))
        self.label_6.setText(_translate("Activity_Dist_Dialog", "Do not print every file that was installed."))
        self.label_7.setText(_translate("Activity_Dist_Dialog", "quiet:"))
        self.control_push_do_update.setText(_translate("Activity_Dist_Dialog", "Apply Current Settings"))
        self.control_push_do_install.setText(_translate("Activity_Dist_Dialog", "Install Project"))
        self.control_push_no_install.setText(_translate("Activity_Dist_Dialog", "Don\'t Not Install"))

try:
    from . import resource_rc
except ImportError:
    print(f'Resource not found in UI layout Main')
    print(f'Qt version {resource_rc.qt_version}')
