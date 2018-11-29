__author__ = 'shixuekai'


import json, os
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt

class TemplateParser(QObject):
    urlChanged = pyqtSignal(str, arguments = ["url"],name="urlChanged")
    appCodeChanged = pyqtSignal(str, arguments = ["code"],name="appCodeChanged")
    zdbFileChanged = pyqtSignal(str, arguments = ["file"],name="zdbFileChanged")
    srcPathChanged = pyqtSignal(str, arguments = ["path"],name="srcPathChanged")
    destPathChanged = pyqtSignal(str, arguments = ["path"],name="destPathChanged")
    finalPathChanged = pyqtSignal(str, arguments = ["path"],name="finalPathChanged")
    packagePathChanged = pyqtSignal(str, arguments = ["path"],name="packagePathChanged")

    deletedSuffixCascadeChanged = pyqtSignal(list, arguments = ["suffix"],name="deletedSuffixCascadeChanged")
    deletedSuffixChanged = pyqtSignal(list, arguments = ["suffix"],name="deletedSuffixChanged")
    deletedFileCascadeChanged = pyqtSignal(list, arguments = ["file"],name="deletedFileCascadeChanged")
    deletedFileChanged = pyqtSignal(list, arguments = ["file"],name="deletedFileChanged")
    deletedFolderChanged = pyqtSignal(list, arguments = ["folder"],name="deletedFolderChanged")
    deletedWorkplaceSuffixChanged = pyqtSignal(list, arguments = ["suffix"],name="deletedWorkplaceSuffixChanged")
    deletedWorkplaceFileChanged = pyqtSignal(list, arguments = ["file"],name="deletedWorkplaceFileChanged")
    deletedPackageFileChanged = pyqtSignal(list, arguments = ["file"],name="deletedWorkplaceFileChanged")

    neededFilesChanged = pyqtSignal(list, arguments = ["file"],name="neededFilesChanged")
    filePackageChanged = pyqtSignal(str, arguments = ["exe"],name="filePackageChanged")
    resetPrgConfigChanged = pyqtSignal(str, arguments = ["exe"],name="resetPrgConfigChanged")
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")

    versionAbstractChanged = pyqtSignal(bool, arguments = ["value"], name="versionAbstractChanged")
    versionAbstractCountChanged = pyqtSignal(int, arguments = ["n"],name="versionAbstractCountChanged")
    updateInfoChanged = pyqtSignal(str, arguments = ["prefix"],name="updateInfoChanged")
    updateChanged = pyqtSignal(dict, arguments = ["update"],name="updateChanged")

    peSignedChanged = pyqtSignal(list, arguments = ["pelist"],name="peSignedChanged")

    parseResultChanged = pyqtSignal(bool, arguments = ["enable"],name="parseResultChanged")


    def __init__(self, path, parent=None):
        super(QObject, self).__init__(parent)
        self._template_path = path
        self._data = {}


    def Parse(self):
        if not os.path.exists(self._template_path):
            self.print.emit("error", self._template_path+" no exists")
            return False

        try:
            self.print.emit("info", "start parse template.json file ..."+self._template_path)
            with open(self._template_path, 'r', encoding="utf-8") as f:
                self._data = json.load(f)
                url = self._data.get("url", "")
                self.urlChanged.emit(url)

                app_code = self._data.get("appCode", "")
                self.appCodeChanged.emit(app_code)

                self._zdb_file = self._data.get("zdbFile", "")
                self.zdbFileChanged.emit(self._zdb_file)

                currentPath = os.getcwd()
                src_path = self._data.get("srcPath", "")
                self.srcPathChanged.emit(currentPath +"\\" + src_path)

                dest_path = self._data.get("destPath", "")
                self.destPathChanged.emit(currentPath + "\\" + dest_path)

                final_path = self._data.get("finalPath", "")
                self.finalPathChanged.emit(currentPath + "\\" + final_path)

                self.packagePathChanged.emit(self._data.get("packagePath", ""))

                self.deletedPackageFileChanged.emit(self._data.get("deletedPackageFile", []))

                self.deletedSuffixCascadeChanged.emit(self._data.get("deletedSuffixCascade", []))

                self.deletedSuffixChanged.emit(self._data.get("deletedSuffix", []))

                self.deletedFileCascadeChanged.emit(self._data.get("deletedFileCascade", []))

                self.deletedFileChanged.emit(self._data.get("deletedFile", []))

                self.deletedFolderChanged.emit(self._data.get("deletedFolder", []))

                self.deletedWorkplaceSuffixChanged.emit(self._data.get("deletedWorkplaceSuffix", []))

                self.deletedWorkplaceFileChanged.emit(self._data.get("deletedWorkplaceFile", []))

                self.neededFilesChanged.emit(self._data.get("neededFiles", []))

                self.filePackageChanged.emit(self._data.get("filePackage", "FilePackage.exe"))

                self.resetPrgConfigChanged.emit(self._data.get("resetPrgConfig", "ResetPrgConfig.exe"))

                self.versionAbstractChanged.emit(self._data.get("versionAbstract", "true") == "true")

                self.versionAbstractCountChanged.emit(self._data.get("versionAbstractCount", 3))

                self.updateInfoChanged.emit(self._data.get("updateInfo", ""))

                self.updateChanged.emit(self._data.get("update", {}))

                self.peSignedChanged.emit(self._data.get("peSigned", []))

                self.print.emit("info", "parse template.json file success")

                f.close()
                return True
        except Exception as e:
            self.print.emit("error", "TemplateParser.py:Parse: TypeExpeption: "+str(e))
        return False


    @pyqtSlot(str)
    def load(self, path):
        if not os.path.exists(path):
            return False

        self._template_path = path
        return self.Parse()