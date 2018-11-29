__author__ = 'shixuekai'


import configparser, Stringer
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt, QThread

class IniProducer(QThread):
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")
    progressChanged = pyqtSignal(float, arguments = ["percent"],name="progressChanged")
    addItem = pyqtSignal(str, str, arguments = ["name", "abstract"],name="addItem")
    minHideVersionChanged = pyqtSignal(str, arguments = ["version"],name="minHideVersionChanged")
    versionChanged = pyqtSignal(str, arguments = ["version"],name="versionChanged")
    versionNameChanged = pyqtSignal(str, arguments = ["versionName"],name="versionNameChanged")
    feedback = pyqtSignal(bool, arguments = ["enable"],name="feedback")


    def __init__(self, downloader, parent=None):
        super(QObject, self).__init__(parent)
        self._version = ""
        self._version_name = ""
        self._abstract = ""
        self._last_n_version_abstract = []
        self._update = {}
        self._min_hide_version = ""
        self._update_info_prefix  =""
        self._ini_path = ""
        self._enable_version_abstract = True


    @pyqtSlot(dict)
    def onUpdateChanged(self, value):
        self._update = value


    @pyqtSlot(list)
    def onLastNVersionAbstract(self, value):
        self._last_n_version_abstract = value


    @pyqtSlot(bool)
    def onEnableVersionAbstract(self, value):
        self._enable_version_abstract = value


    @pyqtSlot(str)
    def onUpdateInfoPrefix(self, value):
        self._update_info_prefix = value


    @pyqtSlot(str, str, str, str, str)
    def produce(self, version, version_name, min_hide_version, abstract, filename):
        self._version = version
        self._version_name = version_name
        self._abstract = Stringer.DisposeOfLineBreak(abstract)
        self._min_hide_version = min_hide_version
        self._ini_path = filename
        self.run()


    def ProduceImp(self):
        self.progressChanged.emit(0.0)

        try:
            config = configparser.ConfigParser(allow_no_value=True)
            config.optionxform = lambda option: option

            if self._enable_version_abstract:
                config["versionAbstract"] = {}
                config["versionAbstract"]["name_0"] = self._version_name
                config["versionAbstract"]["abstract_0"] = "\""+self._abstract.replace("\n", "===")+"\""
                for i in range(0, len(self._last_n_version_abstract)):
                    config["versionAbstract"]["name_"+str(i+1)] = self._last_n_version_abstract[i]["name"]
                    config["versionAbstract"]["abstract_"+str(i+1)] = self._last_n_version_abstract[i]["abstract"]

            config["update"] = self._update
            config["update"]["version"] = self._version
            config["update"]["minHideVersion"] = self._min_hide_version
            config["update"]["versionName"] = self._version_name

            update_info = "[updateInfo]\n"+self._update_info_prefix+self._version_name+"\n"+Stringer.AddSequence(self._abstract)
            config.read_string(update_info)

            with open(self._ini_path, 'w', encoding="utf-8") as configfile:
                config.write(configfile)

            self.print.emit("info", "GenerateVersion success !!!")
            self.progressChanged.emit(1.0)
            self.addItem.emit(self._version_name, self._abstract.replace("\n", "==="))
            return True
        except Exception as e:
            self.print.emit("error", "IniProducer.py:ProduceImp: TypeExcption: "+str(e))
            self.progressChanged.emit(0.0)
        return False


    def run(self):
        self.feedback.emit(True)
        if self.ProduceImp():
            self.minHideVersionChanged.emit(self._min_hide_version)
            self.versionChanged.emit(self._version)
            self.versionNameChanged.emit(self._version_name)
        self.feedback.emit(False)
