__author__ = 'shixuekai'

import urllib.request, zipfile, os
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt, QThread

class DownloadUnziper(QThread):
    progressChanged = pyqtSignal(float, arguments = ["percent"],name="progressChanged")
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")
    feedback = pyqtSignal(bool, arguments = ["enable"],name="feedback")


    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)
        self._url = ""
        self._filename = ""
        self._unzip_folder = ""
        self._unzip_file = ""


    def GetFileName(self, filename):
        file = filename.replace("/", "\\")
        arr = file.split("\\")
        if len(arr) > 0:
            ret = arr[-1].split(".zip")
            if len(ret) > 0:
                return ret[0]
            else:
                return ""
        else:
            return ""


    def DownloadImpl(self, url, filename):
        try:
            if os.path.exists(filename):
                os.remove(filename)
            self.print.emit("info", "start download from "+url)
            urllib.request.urlretrieve(url, filename)
            self.print.emit("info", "download success to "+filename)
            return True
        except Exception as e:
            self.print.emit("error", "DownloadUnziper.py:DownloadImpl: TypeExcption: "+str(e))
        return False


    def DownloadAndUnzipImpl(self, url, filename, unzip_folder):
        if self.download(url,filename):
            return self.unzip(filename, unzip_folder, True)

        return False


    def run(self):
        self.feedback.emit(True)
        self.progressChanged.emit(0.2)
        if self.download(self._url, self._filename):
            self.progressChanged.emit(0.5)
            if self.unzip(self._filename, self._unzip_folder, True):
                self.progressChanged.emit(1.0)
            else:
                self.progressChanged.emit(0.0)
        else:
            self.progressChanged.emit(0.0)

        self.feedback.emit(False)


    @pyqtSlot(str, str)
    def download(self, url, filename):
        if len(url) > 0 and len(url) > 0 and self.DownloadImpl(url, filename):
            return True
        return False


    def UnzipImpl(self, zip_path, unzip_folder, is_delete=True):
        try:
            if not zip_path.endswith(".zip"):
                return False

            #删除解压路径下的文件
            filename = self.GetFileName(zip_path)
            self._unzip_file = unzip_folder+"\\"+filename
            if os.path.exists(self._unzip_file):
                os.remove(self._unzip_file)

            self.print.emit("info", "start unzip "+zip_path+" to "+unzip_folder)
            #解压
            with zipfile.ZipFile(zip_path) as f:
                f.extractall(path=unzip_folder)

            self.print.emit("info", "unzip success "+zip_path+" to "+unzip_folder)
            if (is_delete):
                self.print.emit("info", "delete zip file "+zip_path)
                os.remove(zip_path)
                return True
        except zipfile.BadZipFile as e:
            self.print.emit("error", zip_path+" is a bad zip file ,please check!")
        except Exception as e:
            self.print.emit("error", "DownloadUnziper.py:UnzipImpl: TypeExcption: "+str(e))

        if (is_delete):
            self.print.emit("info", "delete zip file "+zip_path)
            os.remove(zip_path)
        return False


    @pyqtSlot(str, str, bool)
    def unzip(self, zip_path, unzip_folder, is_delete):
        return self.UnzipImpl(zip_path, unzip_folder, is_delete)


    @pyqtSlot(str, str, str)
    def downloadAndUnzip(self, url, filename, unzip_folder):
        self._url = url
        self._filename = filename
        self._unzip_folder = unzip_folder
        self.start()


    @pyqtSlot()
    def close(self):
        if os.path.exists(self._unzip_file):
            self.print.emit("info", "delete unzip file "+self._unzip_file)
            os.remove(self._unzip_file)

