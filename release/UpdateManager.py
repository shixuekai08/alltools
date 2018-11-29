__author__ = 'shixuekai'


import json, os
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt

class UpdateManager(QObject):
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")
    dataChanged = pyqtSignal(dict, arguments = ["data"],name="dataChanged")

    parseResultChanged = pyqtSignal(bool, arguments = ["enable"],name="parseResultChanged")


    def __init__(self, path, parent=None):
        super(QObject, self).__init__(parent)
        self._update_path = path
        self._data = {}


    def Parse(self):
        if not os.path.exists(self._update_path):
            self.print.emit("error", self._update_path+" no exists")
            self.parseResultChanged.emit(False)
            return False

        try:
            self.print.emit("info", "start parse update.json file ... "+self._update_path)
            with open(self._update_path, 'r', encoding="utf-8") as f:
                self._data = json.load(f)
                self.dataChanged.emit(self._data)
                self.print.emit("info", "parse update.json file success")

                self.parseResultChanged.emit(True)
                f.close()
                return True
        except Exception as e:
            self.print.emit("error", "UpdateManager.py:Parse: TypeException: "+str(e))

        self.parseResultChanged.emit(False)
        return False


    def Write(self):
        ret = os.path.split(self._update_path)
        if not os.path.exists(ret[0]):
            os.removedirs(ret[0])

        try:
            with open(self._update_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=True, indent=4)
            return True
        except Exception as e:
            self.print.emit("error", "UpdateManager.py:Write: TypeException: "+str(e))
        return False


    @pyqtSlot(str, str ,str)
    def onAddItem(self, version, version_name, min_hide_version):
        item = {}
        item["minHideVersion"] = int(min_hide_version)
        item["version"] = version_name
        self._data[version] = item

        self.Write()
