__author__ = 'shixuekai'

import json, os
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt

class ConfigManager(QObject):
    lastVersionChanged = pyqtSignal(str, arguments = ["version"],name="lastVersionChanged")
    minHideVersionChanged = pyqtSignal(str, arguments = ["version"],name="minHideVersionChanged")
    finalPathChanged = pyqtSignal(str, arguments = ["path"],name="finalPathChanged")
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")

    parseResultChanged = pyqtSignal(bool, arguments = ["enable"],name="parseResultChanged")


    def __init__(self, path, parent=None):
        super(QObject, self).__init__(parent)
        self._config_path = path
        self._data = {}


    def __del__(self):
        pass


    def Parse(self):
        if not os.path.exists(self._config_path):
            self.print.emit("error", self._config_path+" no exists")
            self.parseResultChanged.emit(False)
            return False

        try:
            self.print.emit("info", "start parse config.json file ..."+self._config_path)
            with open(self._config_path, 'r', encoding="utf-8") as f:
                self._data = json.load(f)

                last_version = self._data.get("lastVersion", "")
                self.lastVersionChanged.emit(last_version)


                self.minHideVersionChanged.emit(self._data.get("minHideVersion", ""))

                currentPath = os.getcwd()
                final_path = self._data.get("finalPath", "")
                if os.path.exists(currentPath + "\\" + final_path):
                    final_path = currentPath + "\\" + final_path
                self.finalPathChanged.emit(final_path)

                self.print.emit("info", "parse config.json file success")

                self.parseResultChanged.emit(True)
                f.close()
                return True
        except Exception as e:
            self.print.emit("error", "ConfigManager.py:Parse: TypeException: "+str(e))

        self.parseResultChanged.emit(False)
        return False


    def Write(self):
        ret = os.path.split(self._config_path)
        if not os.path.exists(ret[0]):
            os.removedirs(ret[0])

        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=True, indent=4)
            return True
        except Exception as e:
            self.print.emit("error", "ConfigManager.py:Write: TypeException: "+str(e))
        return False


    @pyqtSlot(str)
    def load(self, path):
        if not os.path.exists(path):
            return False

        self._config_path = path
        return self.Parse()


    @pyqtSlot(str)
    def onFinalPath(self, path):
        currentPath = os.getcwd()
        if os.path.exists(currentPath + "\\" + path):
            self._final_path = currentPath + "\\" + path
        else:
            self._final_path = path

        self._data["finalPath"] = self._final_path
        self.Write()


    @pyqtSlot(str)
    def onLastVersionChanged(self, value):
        if len(value) == 9 and value.isdigit():
            self._data["lastVersion"] = value
            self.Write()
        else:
            raise ValueError('last_version must be 9 digit number!')


    @pyqtSlot(str)
    def onMinHideVersionChanged(self, value):
        if len(value) == 9 and value.isdigit():
            self._data["minHideVersion"] = value
            self.Write()
        else:
            raise ValueError('last_version must be 9 digit number!')