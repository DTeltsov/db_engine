# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_database.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 569)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table_list = QtWidgets.QListWidget(self.centralwidget)
        self.table_list.setGeometry(QtCore.QRect(10, 40, 171, 471))
        self.table_list.setObjectName("table_list")
        self.data_table = QtWidgets.QTableWidget(self.centralwidget)
        self.data_table.setGeometry(QtCore.QRect(200, 40, 591, 471))
        self.data_table.setObjectName("data_table")
        self.data_table.setColumnCount(0)
        self.data_table.setRowCount(0)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 0, 591, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_column_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_column_button.setObjectName("add_column_button")
        self.horizontalLayout.addWidget(self.add_column_button)
        self.delete_column_botton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_column_botton.setObjectName("delete_column_botton")
        self.horizontalLayout.addWidget(self.delete_column_botton)
        self.update_column_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.update_column_button.setObjectName("update_column_button")
        self.horizontalLayout.addWidget(self.update_column_button)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.add_row_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_row_button.setObjectName("add_row_button")
        self.horizontalLayout.addWidget(self.add_row_button)
        self.delete_row_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_row_button.setObjectName("delete_row_button")
        self.horizontalLayout.addWidget(self.delete_row_button)
        self.update_row_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.update_row_button.setObjectName("update_row_button")
        self.horizontalLayout.addWidget(self.update_row_button)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(9, 0, 171, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.delete_table_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.delete_table_button.setObjectName("delete_table_button")
        self.horizontalLayout_3.addWidget(self.delete_table_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuDatabase = QtWidgets.QMenu(self.menubar)
        self.menuDatabase.setObjectName("menuDatabase")
        MainWindow.setMenuBar(self.menubar)
        self.actionCreate_new = QtWidgets.QAction(MainWindow)
        self.actionCreate_new.setObjectName("actionCreate_new")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setMenuRole(QtWidgets.QAction.NoRole)
        self.actionSave.setShortcutVisibleInContextMenu(True)
        self.actionSave.setObjectName("actionSave")
        self.menuDatabase.addAction(self.actionCreate_new)
        self.menuDatabase.addAction(self.actionLoad)
        self.menuDatabase.addAction(self.actionSave)
        self.menubar.addAction(self.menuDatabase.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Database"))
        self.add_column_button.setText(_translate("MainWindow", "Add column"))
        self.delete_column_botton.setText(_translate("MainWindow", "Delete column"))
        self.update_column_button.setText(_translate("MainWindow", "Update column"))
        self.add_row_button.setText(_translate("MainWindow", "Add row"))
        self.delete_row_button.setText(_translate("MainWindow", "Delete row"))
        self.update_row_button.setText(_translate("MainWindow", "Update row"))
        self.pushButton.setText(_translate("MainWindow", "Add table"))
        self.delete_table_button.setText(_translate("MainWindow", "Delete table"))
        self.menuDatabase.setTitle(_translate("MainWindow", "Database"))
        self.actionCreate_new.setText(_translate("MainWindow", "Create"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))