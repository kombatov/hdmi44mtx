#!/usr/bin/env python3

import sys
import io
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import socket
import hdmi_const

class hdmi_window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.__connected = False
        self.__valout = ""
        self.__valinp = ""
        self.__ipport = ("192.168.0.221", 8899)
        QtWidgets.QWidget.__init__(self, parent)

        self.LoadMainUi()

        self.__labelRCdefault = self.labelRC.text()
        self.ActClick.triggered.connect(self.ActClickImpl)
        self.sock = socket.socket()
        self.sock.settimeout(2)
        self.TryConnected()

    def __del__(self):
        self.sock.close()

    def LoadMainUi(self):
        QtCore.QDir.addSearchPath('dir_ui', '.')
        self.uiFile = QtCore.QFile("dir_ui:hdmi_rc.ui")
        self.uiFile.open(QtCore.QFile.ReadOnly)
        self.data = self.uiFile.readAll()
        self.uiFile.close()
        self.uiFile = io.BytesIO(bytes(self.data))
        uic.loadUi(self.uiFile, self)

    def TryConnected(self):
        self.__pal = self.labelRC.palette()
        try:
            self.sock.connect(self.__ipport)
            self.__connected = True
            self.labelRC.setText(self.__labelRCdefault)
            self.__pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("black"))
        except:
            self.__connected = False
            self.labelRC.setText(self.__labelRCdefault + ' ' + str(self.__ipport))
            self.__pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        self.labelRC.setPalette(self.__pal)

    def ActClickImpl(self):
        self.__valout, self.__valinp = self.ActClick.sender().objectName().lower()[6:].split("_")
        if not self.__connected:
            self.TryConnected()
        try:
            self.sock.send(hdmi_const.outs[int(self.__valout)][self.__valinp])
        except:
            self.TryConnected()


app = QtWidgets.QApplication([])
win = hdmi_window()
win.show()
sys.exit(app.exec())