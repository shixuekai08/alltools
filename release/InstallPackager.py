__author__ = 'shixuekai'


import os, shutil
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt, QThread

class InstallPackager(QThread):
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")
    progressChanged = pyqtSignal(float, arguments = ["percent"],name="progressChanged")
    feedback = pyqtSignal(bool, arguments = ["enable"],name="feedback")


    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)
        self._deleted_suffix_ascade = []
        self._deleted_suffix = []
        self._deleted_file_ascade = []
        self._deleted_file = []
        self._deleted_folder = []
        self._final_path = ""
        self._package_path = ""
        self._pe_signed_list = []
        self._is_check_sign = False


    #从文件夹folder中删除以suffix为文件结尾的文件， cascade表示是否遍历folder中的文件夹
    def DeleteFilesWithSuffix(self, folder, suffix, cascade):
        if len(suffix) == 0 or not os.path.exists(folder):
            return True

        try:
            if cascade:
                for root, dirs, files in os.walk(folder):
                    for name in files:
                        fullPath = os.path.join(root, name)
                        pathname = os.path.splitext(fullPath)
                        if (pathname[1] == suffix):
                            os.remove(fullPath)
                            self.print.emit("info", "deleting "+fullPath)
            else:
                for file in os.listdir(folder):
                    fullPath = os.path.join(folder, file)
                    if os.path.isfile(fullPath):
                        pathname = os.path.splitext(fullPath)
                        if pathname[1] == suffix:
                            os.remove(fullPath)
                            self.print.emit("info", "deleting "+fullPath)
            return True
        except Exception as e:
            self.print.emit("error", "InstallPackager.py:DeleteFilesWithSuffix cascade: "+str(cascade)+"  TypeExcption: "+str(e))
        return False


    def DeleteFilesWithSuffixs(self, folder, suffixs, cascade):
        if len(suffixs) == 0 or not os.path.exists(folder):
            return True

        try:
            if cascade:
                for root, dirs, files in os.walk(folder):
                    for name in files:
                        fullPath = os.path.join(root, name)
                        pathname = os.path.splitext(fullPath)
                        if pathname[1] in suffixs:
                            os.remove(fullPath)
                            self.print.emit("info", "deleting "+fullPath)
            else:
                for file in os.listdir(folder):
                    fullPath = os.path.join(folder, file)
                    if os.path.isfile(fullPath):
                        pathname = os.path.splitext(fullPath)
                        if pathname[1] in suffixs:
                            os.remove(fullPath)
                            self.print.emit("info", "deleting "+fullPath)
            return True
        except Exception as e:
            self.print.emit("error", "InstallPackager.py:DeleteFilesWithSuffixs cascade: "+str(cascade)+"  TypeExcption: "+str(e))
        return False


    #从文件夹folder中删除文件名为filename的文件， cascade表示是否遍历folder中的文件夹
    def DeleteFilesWithName(self, folder, filename, cascade):
        if len(filename) == 0 or not os.path.exists(folder):
            return True

        try:
            if cascade:
                for root, dirs, files in os.walk(folder, cascade):
                    for name in files:
                        fullPath = os.path.join(root, name)
                        if (name == filename):
                            os.remove(fullPath)
                            self.print.emit("info", "deleting "+fullPath)
            else:
                for file in os.listdir(folder):
                    fullPath = os.path.join(folder, file)
                    if os.path.isfile(fullPath) and file == filename:
                        os.remove(fullPath)
                        self.print.emit("info", "deleting "+fullPath)

            return True
        except Exception as e:
            self.print.emit("error", "InstallPackager.py:DeleteFilesWithName cascade: "+str(cascade)+"  TypeExcption: "+str(e))
        return False


    def DeleteFilesWithNames(self, folder, filenames, cascade):
        if len(filenames) == 0 or not os.path.exists(folder):
            return True

        try:
            if cascade:
                for root, dirs, files in os.walk(folder):
                    for name in files:
                        fullPath = os.path.join(root, name)
                        if name in filenames:
                            os.remove(fullPath)
                            self.print.emit("info", "deleting "+fullPath)
            else:
                for file in os.listdir(folder):
                    fullPath = os.path.join(folder, file)
                    if os.path.isfile(fullPath) and file in filenames:
                        os.remove(fullPath)
                        self.print.emit("info", "deleting "+fullPath)
            return True
        except Exception as e:
            self.print.emit("error", "InstallPackager.py:DeleteFolder: cascade: "+str(cascade)+"   TypeExcption: "+str(e))
        return False


    def DeleteFolder(self, path, folders):
        if len(folders) == 0 or not os.path.exists(path):
            return True

        try:
            for folder in folders:
                fullPath = os.path.join(path, folder)
                if os.path.exists(fullPath) and os.path.isdir(fullPath):
                    shutil.rmtree(fullPath)
                    self.print.emit("info", "deleting "+fullPath)
            return True
        except Exception as e:
            self.print.emit("error", "InstallPackager.py:DeleteFolder: TypeExcption: "+str(e))
        return False


    @pyqtSlot(list)
    def onDeletedSuffixAscade(self, suffix):
        self._deleted_suffix_ascade = suffix


    @pyqtSlot(list)
    def onDeletedSuffix(self, suffix):
        self._deleted_suffix = suffix


    @pyqtSlot(list)
    def onDeletedFileAscade(self, file):
        self._deleted_file_ascade = file


    @pyqtSlot(list)
    def onDeletedFile(self, file):
        self._deleted_file = file


    @pyqtSlot(list)
    def onDeletedFolder(self, folder):
        self._deleted_folder = folder


    @pyqtSlot(str, str, bool)
    def packing(self, final_path, package_path, is_check_sign):
        self._final_path = final_path
        self._package_path = package_path
        self._is_check_sign = is_check_sign
        self.start()


    @pyqtSlot(list)
    def onPeSignedChanged(self, value):
        self._pe_signed_list = value


    def PackingImpl(self):
        try:
            current = os.getcwd()
            #检验签名
            if self._is_check_sign:
                for file in self._pe_signed_list:
                    filepath = self._final_path + "\\"+file
                    self.print.emit("info", "check whether "+filepath+" is signed")
                    rpc = current + "\\WhetherPeIsSigned.exe " + filepath
                    ret = os.system(rpc)
                    if ret != 0:
                        self.print.emit("error", filepath+" is not signed")
                        return False

            input_path = self._package_path+"/Input"

            self.print.emit("info", "clear "+input_path)
            if os.path.exists(input_path):
                shutil.rmtree(input_path)

            self.progressChanged.emit(0.1)

            self.print.emit("info", "拷贝文件夹: from "+self._final_path + " to "+input_path)
            shutil.copytree(self._final_path, input_path)

            #更新进度
            self.progressChanged.emit(0.5)


            self.print.emit("info", "清洁 "+ input_path+" ...")
            if not self.DeleteFilesWithSuffixs(input_path, self._deleted_suffix, False):
                self.print.emit("error", "DeleteFilesWithSuffixs false fail !!!")
                return False

            #更新进度
            self.progressChanged.emit(0.6)

            if not self.DeleteFilesWithSuffixs(input_path, self._deleted_suffix_ascade, True):
                self.print.emit("error", "DeleteFilesWithSuffixs true fail !!!")
                return False

            #更新进度
            self.progressChanged.emit(0.7)

            if not self.DeleteFilesWithNames(input_path, self._deleted_file_ascade, True):
                self.print.emit("error", "DeleteFilesWithNames true fail !!!")
                return False

            #更新进度
            self.progressChanged.emit(0.8)

            if not self.DeleteFilesWithNames(input_path, self._deleted_file, False):
                self.print.emit("error", "DeleteFilesWithNames false fail !!!")
                return False

            #更新进度
            self.progressChanged.emit(0.9)

            if not self.DeleteFolder(input_path, self._deleted_folder):
                self.print.emit("error", "DeleteFolder fail !!!")
                return False

            os.startfile(self._package_path)

            self.progressChanged.emit(1.0)
            self.print.emit("info", "打包成功")
            return True
        except Exception as e:
            self.print.emit("error", "InstallPackager.py:PackingImpl: TypeExcption: "+str(e))
        return False


    def run(self):
        self.feedback.emit(True)
        if self.PackingImpl():
            pass
        else:
            self.progressChanged.emit(0)
        self.feedback.emit(False)