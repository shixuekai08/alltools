__author__ = 'shixuekai'


import json, os
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt

class VersionManager(QObject):
    print = pyqtSignal(str, str, arguments = ["level", "msg"], name="print")
    lastNVersionAbstract = pyqtSignal(list, arguments = ["n"], name="lastNVersionAbstract")
    dataChanged = pyqtSignal(str, arguments = ["data"], name="dataChanged")

    parseResultChanged = pyqtSignal(bool, arguments = ["enable"],name="parseResultChanged")


    def __init__(self, path, parent=None):
        super(QObject, self).__init__(parent)
        self._version_path = path
        self._count = 3
        self._data = []


    def __del__(self):
        pass


    def Parse(self):
        if not os.path.exists(self._version_path):
            self.print.emit("error", self._version_path+" no exists")
            self.parseResultChanged.emit(False)
            return False

        try:
            self.print.emit("info", "start parse version.json file ... "+self._version_path)
            with open(self._version_path, 'r', encoding="utf-8") as f:
                self._data = json.load(f)
                f.close()

                data_len = len(self._data)
                if data_len >= self._count:
                    self.lastNVersionAbstract.emit(self._data[0:self._count])
                else:
                    ret = self._data
                    for x in range(len(self._data), self._count-1):
                        ret.append({"name":"null", "abstract": "null"})
                    self.lastNVersionAbstract.emit(ret)
                self.print.emit("info", "parse version.json file success")
                self.dataChanged.emit(json.dumps(self._data, ensure_ascii=False, indent=4))
            self.parseResultChanged.emit(True)
            return True
        except Exception as e:
            self.print.emit("error", "VersionManager.py:Parse: TypeException: "+str(e))
        self.parseResultChanged.emit(False)
        return False


    def Write(self):
        ret = os.path.split(self._version_path)
        if not os.path.exists(ret[0]):
            os.removedirs(ret[0])

        try:
            with open(self._version_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=True, indent=4)
            return True
        except Exception as e:
            self.print.emit("error", "VersionManager.py:Write: TypeException: "+str(e))
        return False


    @pyqtSlot(str)
    def load(self, path):
        if not os.path.exists(path):
            return False

        self._version_path = path
        return self.Parse()


    @pyqtSlot(str, str)
    def addItem(self, name, abstract):
        is_add = False
        for x in self._data:
            if x["name"] == name:
                x["abstract"] = "\""+abstract+"\""
                is_add = True
                break

        if not is_add:
            x = {}
            x["name"] = name
            x["abstract"] = "\""+abstract+"\""
            self._data.insert(0, x)

        self.Write()


    @pyqtSlot(int)
    def onVersionAbstractCount(self, value):
        if value > 1:
            self._count = value-1
        else:
            self._count = 2

