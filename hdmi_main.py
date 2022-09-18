#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import socket
import res.hdmi_const as hdmi_const
import ClassMainSettings

class main_window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.__connected = False
        QtWidgets.QWidget.__init__(self, parent)

        self.LoadMainUi()

        self.__labelRCdefault = self.labelRC.text()
        self.ActClick.triggered.connect(self.ActClickImpl)
        self.ActSettings.triggered.connect(self.ActClickSettings)
        self.sock = socket.socket()
        self.sock.settimeout(2)
        self.TryConnected()

    def __del__(self):
        self.sock.close()

    def LoadMainUi(self):
        #uic.loadUi('res/hdmi_rc.ui', self)
        QtCore.QDir.addSearchPath('dir_ui', 'res')
        self.uiFile = QtCore.QFile("dir_ui:main.ui")
        self.uiFile.open(QtCore.QFile.ReadOnly)
        uic.loadUi(self.uiFile, self)

    def TryConnected(self):
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

    def ActClickImpl(self):
        self.PushButtons([self.ActClick.sender().objectName()])

    def ActClickSettings(self):
        contextMenu = QtWidgets.QMenu(self)
        ActSettingsQuit = contextMenu.addAction("Выход")
        ActSettingsQuit.triggered.connect(self.close)
        ActSettingsSets = contextMenu.addAction("Настройки")
        contextMenu.addSeparator()
        for i in range(len(mainset.command_templates)):
            newact = QtWidgets.QAction(mainset.command_templates[i]["caption"], contextMenu)
            newact.setData(i)
            newact.triggered.connect(self.ActTemplateApply)
            contextMenu.addAction(newact)
        contextMenu.popup(self.mapToGlobal(self.btnSettings.pos()))

    def ActTemplateApply(self):
        num_command = self.sender().data()
        list_command =mainset.command_templates[num_command]["command"]
        self.PushButtons(list_command)

    def PushButtons(self, arrNames):
        if not self.__connected:
            self.TryConnected()
        for curname in arrNames:
            __valout, __valinp = curname.lower()[6:].split("_")
            try:
                self.sock.send(hdmi_const.outs[int(__valout)][__valinp])
            except:
                self.TryConnected()


mainset = ClassMainSettings.MainSet()
try:
    app = QtWidgets.QApplication([])
    win = main_window()
    win.show()
    sys.exit(app.exec())
finally:
    del mainset
