__author__ = 'shixuekai'

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt

class LOG(QObject):
    infoChanged = pyqtSignal(str, arguments = ["msg"],name="infoChanged")
    warningChanged = pyqtSignal(str, arguments = ["msg"],name="warningChanged")
    errorChanged = pyqtSignal(str, arguments = ["msg"],name="errorChanged")

    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)

    @pyqtSlot(str, str)
    def print(self, level, msg):
        if "error" == level:
            self.errorChanged.emit(msg)
        elif "warn" == level:
            self.warningChanged.emit(msg)
        elif "info" == level:
            self.infoChanged.emit(msg)
