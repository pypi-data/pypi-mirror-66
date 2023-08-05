# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/mesonui-layout/activity_dist.ui'
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
        self.groupBox = QtWidgets.QGroupBox(Activity_Dist_Dialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 731, 351))
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 81, 71))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("")
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/icon/mesonui-icon/meson_modern.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 160, 121, 16))
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.combo_formats = QtWidgets.QComboBox(self.groupBox)
        self.combo_formats.setGeometry(QtCore.QRect(160, 160, 191, 26))
        self.combo_formats.setStyleSheet("")
        self.combo_formats.setObjectName("combo_formats")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 200, 121, 16))
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.combo_include_subprojects = QtWidgets.QComboBox(self.groupBox)
        self.combo_include_subprojects.setGeometry(QtCore.QRect(160, 200, 191, 26))
        self.combo_include_subprojects.setStyleSheet("")
        self.combo_include_subprojects.setObjectName("combo_include_subprojects")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(360, 160, 351, 16))
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(360, 200, 371, 31))
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.info = QtWidgets.QPlainTextEdit(self.groupBox)
        self.info.setGeometry(QtCore.QRect(140, 30, 571, 111))
        self.info.setStyleSheet("")
        self.info.setReadOnly(True)
        self.info.setObjectName("info")
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
        self.control_push_do_dist = QtWidgets.QPushButton(self.layoutWidget)
        self.control_push_do_dist.setStyleSheet("")
        self.control_push_do_dist.setObjectName("control_push_do_dist")
        self.horizontalLayout.addWidget(self.control_push_do_dist)
        self.control_push_no_dist = QtWidgets.QPushButton(Activity_Dist_Dialog)
        self.control_push_no_dist.setGeometry(QtCore.QRect(20, 365, 168, 24))
        self.control_push_no_dist.setStyleSheet("")
        self.control_push_no_dist.setObjectName("control_push_no_dist")

        self.retranslateUi(Activity_Dist_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Activity_Dist_Dialog)

    def retranslateUi(self, Activity_Dist_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Activity_Dist_Dialog.setWindowTitle(_translate("Activity_Dist_Dialog", "Dist"))
        self.groupBox.setTitle(_translate("Activity_Dist_Dialog", "Dist view:"))
        self.label.setText(_translate("Activity_Dist_Dialog", "formats type:"))
        self.label_2.setText(_translate("Activity_Dist_Dialog", "include subprojects:"))
        self.label_3.setText(_translate("Activity_Dist_Dialog", "Comma separated list of archive types to create."))
        self.label_4.setText(_translate("Activity_Dist_Dialog", "Include source code of subprojects that have been used\n"
" for the build."))
        self.info.setPlainText(_translate("Activity_Dist_Dialog", "In addition to development, almost all projects provide periodical source releases. These are standalone packages (usually either in tar or zip format) of the source code. They do not contain any revision control metadata, only the source code.  Meson provides a simple way of generating these, with the meson dist command.  Meson-UI supports this feature in the background:"))
        self.control_push_do_update.setText(_translate("Activity_Dist_Dialog", "Apply Current Settings"))
        self.control_push_do_dist.setText(_translate("Activity_Dist_Dialog", "Create My New Release"))
        self.control_push_no_dist.setText(_translate("Activity_Dist_Dialog", "Don\'t Not Setup Yet"))

try:
    from . import resource_rc
except ImportError:
    print(f'Resource not found in UI layout Main')
    print(f'Qt version {resource_rc.qt_version}')
