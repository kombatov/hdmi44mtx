import sys
from PySide6 import QtWidgets, QtCore, QtGui
from qtpy import uic
import ClassMainSettings
import hdmi_main


class SetsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        uic.loadUi('res/settings.ui', self)
        self.resize(parent.width(), parent.height())
        # Было ли сохранение настроек
        bChangeSaved = False


    def sync_ms2form(self):
        pass

    def sync_form2ms(self):
        pass