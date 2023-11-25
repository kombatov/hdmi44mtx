#!/usr/bin/env python3

import sys
import time
from PySide6 import QtWidgets, QtCore, QtGui
import socket
import res.hdmi_const as hdmi_const
import ClassMainSettings
from qtpy import uic
import SetsWindow
#import ui_loader


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.__connected = False
        QtWidgets.QWidget.__init__(self, parent)
        self.contextMenu = None
        self.uiFile = None
        uic.loadUi('res/main.ui', self)
        #ui_loader.load_ui('res/main.ui', self)

        # Признак необходимости пересобрать всплывающее меню
        self.bNeedMenuRecreate = True

        self.__labelRCdefault = self.labelRC.text()
        self.ActClick.triggered.connect(self.act_click_execute)
        self.ActMenu.triggered.connect(self.act_menu_show_execute)
        self.sock = socket.socket()
        self.sock.settimeout(2)
        self.try_connected()

    def __del__(self):
        self.sock.close()

    def try_connected(self):
        __pal = self.labelRC.palette()
        try:
            self.sock.connect((mainset.dev_ip, mainset.dev_port))
            self.__connected = True
            self.labelRC.setText(self.__labelRCdefault)
            __pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("black"))
        except:
            self.__connected = False
            self.labelRC.setText(self.__labelRCdefault + ' ' + str(mainset.dev_ipport))
            __pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.labelRC.setPalette(__pal)

    def act_click_execute(self):
        self.push_buttons([self.ActClick.sender().objectName()])

    def act_menu_recreate_execute(self):
        del self.contextMenu
        self.contextMenu = QtWidgets.QMenu(self)
        ActMenuQuit = self.contextMenu.addAction("Выход")
        ActMenuQuit.triggered.connect(self.close)
        ActMenuSets = self.contextMenu.addAction("Настройки")
        ActMenuSets.triggered.connect(self.act_menu_sets_execute)
        self.contextMenu.addSeparator()
        for i in range(len(mainset.command_list)):
            newact = QtGui.QAction(mainset.command_list[i]["caption"], self.contextMenu)
            newact.setData(mainset.command_list[i]["command"])  # список команд сохраняем в data
            newact.triggered.connect(self.act_menu_list_execute)
            self.contextMenu.addAction(newact)

    # Отображение всплывающего меню
    def act_menu_show_execute(self):
        if self.bNeedMenuRecreate:
            self.act_menu_recreate_execute()
            self.bNeedMenuRecreate = False
        # позиционируем по координатам относительно главного окна
        self.contextMenu.popup(self.mapToGlobal(self.btnMenu.pos()))

    # Форма настроек
    def act_menu_sets_execute(self):
        formsw = SetsWindow.SetsWindow(parent=self)
        formsw.exec()

    # Акшен выполнения команды нажатия настраиваемого пункта меню
    def act_menu_list_execute(self):
        # список команд приколочен к акшену
        self.push_buttons(self.sender().data())

    def push_buttons(self, arrNames):
        if not self.__connected:
            self.TryConnected()
        for curname in arrNames:
            valout, valinp = curname.lower()[6:].split("_")
            try:
                self.sock.send(hdmi_const.outs[int(valout)][valinp])
            except:
                self.TryConnected()
            time.sleep(1)


if __name__ == "__main__":
    mainset = ClassMainSettings.MainSet()
    try:
        app = QtWidgets.QApplication([])
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
    finally:
        del mainset
