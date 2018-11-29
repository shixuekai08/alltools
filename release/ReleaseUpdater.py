__author__ = 'shixuekai'

import os, shutil, configparser, zipfile
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt, QThread
from DownloadUnziper import DownloadUnziper

class ReleaseUpdater(QThread):
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")
    feedback = pyqtSignal(bool, arguments = ["enable"],name="feedback")
    progressChanged = pyqtSignal(float, arguments = ["percent"],name="progressChanged")
    versionChanged = pyqtSignal(str, arguments = ["v"],name="versionChanged")
    minHideVersionChanged = pyqtSignal(str, arguments = ["version"],name="minHideVersionChanged")
    versionNameChanged = pyqtSignal(str, arguments = ["versionName"],name="versionNameChanged")
    addItem = pyqtSignal(str, str, str, arguments = ["version", "versionName", "minHideVersion"],name="addItem")
    addVersionAbstract = pyqtSignal(str, str, arguments = ["name", "abstract"],name="addVersionAbstract")


    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)
        self._deleted_suffix_ascade = []
        self._deleted_suffix = []
        self._deleted_file_ascade = []
        self._deleted_file = []
        self._deleted_folder = []
        self._deleted_workplace_suffix = []
        self._deleted_workplace_file = []
        self._src_path = ""
        self._dest_path = ""
        self._final_path = ""
        self._version = ""
        self._needed_files = []
        self._file_package = ""
        self._reset_prg_config = ""
        self._version_path = ""
        self._zdb_url = ""
        self._zdb_file = ""
        self._is_zip = False
        self._min_hide_version = ""
        self._version_name = ""
        self._is_check_sign = False
        self._pe_signed_list = []


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


    @pyqtSlot(list)
    def onDeletedWorkplaceFile(self, file):
        self._deleted_workplace_file = file


    @pyqtSlot(list)
    def onDeletedWorkplaceSuffix(self, file):
        self._deleted_workplace_suffix = file


    @pyqtSlot(str)
    def onSrcPath(self, path):
        self._src_path = path


    @pyqtSlot(str)
    def onDestPath(self, path):
        self._dest_path = path


    @pyqtSlot(str)
    def onFinalPath(self, path):
        self._final_path = path


    @pyqtSlot(list)
    def onNeededFiles(self, file):
        self._needed_files = file


    @pyqtSlot(str)
    def onFilePackage(self, file):
        self._file_package = file


    @pyqtSlot(str)
    def onResetPrgConfig(self, file):
        self._reset_prg_config = file


    @pyqtSlot(list)
    def onPeSignedChanged(self, value):
        self._pe_signed_list = value




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
            self.print.emit("error", "ReleaseUpdater.py:DeleteFilesWithSuffix: cascade: "+str(cascade)+"  TypeExcption: "+str(e))

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
            self.print.emit("error", "ReleaseUpdater.py:DeleteFilesWithSuffixs: cascade: "+str(cascade)+"  TypeExcption: "+str(e))


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
            self.print.emit("error", "ReleaseUpdater.py:DeleteFilesWithName: cascade: "+str(cascade)+"  TypeExcption: "+str(e))

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
            self.print.emit("error", "ReleaseUpdater.py:DeleteFilesWithNames: cascade: "+str(cascade)+"  TypeExcption: "+str(e))

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
            self.print.emit("error", "ReleaseUpdater.py:DeleteFolder: TypeExcption: "+str(e))

        return False


    def CopyVersionFile(self, src, dest):
        if os.path.exists(src) and os.path.isfile(src):
            shutil.copy2(src, dest)
            return True

        return False


    def CheckingResources(self):
        self.print.emit("info", "start check resources ")

        if not os.path.exists(self._final_path):
            self.print.emit("error", "请确保文件夹存在: "+self._final_path)
            return False

        current = os.getcwd()

        fullPath = os.path.join(current, self._file_package)
        if not os.path.exists(fullPath):
            self.print.emit("error", "请确保文件存在: "+fullPath)
            return False

        fullPath = os.path.join(current, self._reset_prg_config)
        if not os.path.exists(fullPath):
            self.print.emit("error", "请确保文件存在: "+fullPath)
            return False


        for file in self._needed_files:
            fullPath = os.path.join(current, file)
            if not os.path.exists(fullPath):
                self.print.emit("error", "请确保文件存在: "+fullPath)
                return False

        return True


    @pyqtSlot(str, str, str, str, str, bool, bool)
    def packing(self, zdb_url, zdb_file, version,version_name, min_hide_version, is_zip, is_check_sign):
        self._zdb_url = zdb_url
        self._zdb_file = zdb_file
        self._version = version
        self._version_name = version_name
        self._min_hide_version = min_hide_version
        self._is_zip = is_zip
        self._is_check_sign = is_check_sign
        self.start()


    def PackImpl(self,version):
        if not len(version) == 9 or not version.isdigit():
            self.print.emit("error", "请确保版本号是9位数字")
            return False

        #检验资源
        if not self.CheckingResources():
            self.print.emit("error", "CheckingResources fail")
            return False


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

        if not os.listdir(self._final_path):
            self.print.emit("error", "请确保文件夹非空: "+self._final_path)
            return False

        try:
            if os.path.exists(self._src_path):
                self.print.emit("info", "删除文件夹: "+self._src_path)
                shutil.rmtree(self._src_path)

            if os.path.exists(self._dest_path):
                self.print.emit("info", "删除文件夹: "+self._dest_path)
                shutil.rmtree(self._dest_path)
            os.makedirs(self._dest_path)

            #更新进度
            self.progressChanged.emit(0.1)

            self.print.emit("info", "拷贝文件夹: from "+self._final_path + " to "+self._dest_path+"\\"+self._version)
            shutil.copytree(self._final_path, self._src_path)

            #下载zdb
            downloader = DownloadUnziper()
            if not downloader or not downloader.DownloadAndUnzipImpl(self._zdb_url, self._src_path+"\\"+self._zdb_file, self._src_path):
                self.print.emit("error", "下载zdb文件失败")
                return False
            self.print.emit("info", "下载zdb文件成功")


            #更新进度
            self.progressChanged.emit(0.15)

            self.print.emit("info", "创建version.ini文件")
            if not self.CopyVersionFile(self._final_path+"\\version.ini", self._dest_path+"\\version.ini"):
                self.print.emit("error", "copy version.ini fail")
                return False

        except Exception as e:
            self.print.emit("error", "ReleaseUpdater.py:PackImpl: stage1 TypeExcption: "+str(e))
            return False

        #更新进度
        self.progressChanged.emit(0.2)
        self.print.emit("info", "清洁工作区 "+current+" ...")
        #删除工作区指定后缀的文件
        if not self.DeleteFilesWithSuffixs(current, self._deleted_workplace_suffix, False):
            self.print.emit("error", "DeleteFilesWithSuffixs fail !!!")
            return False

        #删除工作区指定文件名的文件
        if not self.DeleteFilesWithNames(current, self._deleted_workplace_file, False):
            self.print.emit("error", "DeleteFilesWithNames fail !!!")
            return False

        #更新进度
        self.progressChanged.emit(0.25)

        self.print.emit("info", "清洁 "+ self._src_path+" ...")
        if not self.DeleteFilesWithSuffixs(self._src_path, self._deleted_suffix, False):
            self.print.emit("error", "DeleteFilesWithSuffixs false fail !!!")
            return False

        if not self.DeleteFilesWithSuffixs(self._src_path, self._deleted_suffix_ascade, True):
            self.print.emit("error", "DeleteFilesWithSuffixs true fail !!!")
            return False

        if not self.DeleteFilesWithNames(self._src_path, self._deleted_file_ascade, True):
            self.print.emit("error", "DeleteFilesWithNames true fail !!!")
            return False

        if not self.DeleteFilesWithNames(self._src_path, self._deleted_file, False):
            self.print.emit("error", "DeleteFilesWithNames false fail !!!")
            return False

        if not self.DeleteFolder(self._src_path, self._deleted_folder):
            self.print.emit("error", "DeleteFolder fail !!!")
            return False

        try:
            #更新进度
            self.progressChanged.emit(0.3)

            self.print.emit("info", "拷贝文件夹: from "+self._src_path + " to "+self._dest_path+"\\"+self._version)
            shutil.copytree(self._src_path, self._dest_path+"\\"+self._version)

            self.print.emit("info", "Sha1 value calculation")
            rpc = current + "\\"+self._reset_prg_config+" "+self._dest_path+"\\"+self._version+" "+self._version
            ret = os.system(rpc)
            if ret != 0:
                self.print.emit("error", rpc+" fail "+str(ret))
                return False


            #更新进度
            self.progressChanged.emit(0.6)

            self.print.emit("info", "Zip archive")
            rpc = current + "\\"+self._file_package+" "+self._dest_path+"\\"+self._version
            ret = os.system(rpc)
            if ret != 0:
                self.print.emit("error", rpc+" fail "+str(ret))
                return False

            #更新进度
            self.progressChanged.emit(0.9)
            self.print.emit("info", "The publish file is in the publish directory")

            #是否压缩
            if self._is_zip:
                self.print.emit("info", "start zip ...")
                shutil.copytree(self._dest_path+"\\"+self._version, self._dest_path+"\\temp\\"+self._version)
                self.print.emit("info", "copy "+self._dest_path+"\\"+self._version+"  to "+self._dest_path+"\\temp\\"+self._version)

                self.CopyVersionFile(self._dest_path+"\\version.ini", self._dest_path+"\\temp\\version.ini")
                self.print.emit("info", "copy "+self._dest_path+"\\version.ini to "+self._dest_path+"\\temp\\version.ini")

                shutil.make_archive(self._dest_path+"\\"+self._version, 'zip', self._dest_path+"\\temp")
                self.print.emit("info", "zip "+self._dest_path+"\\temp into "+self._dest_path+"\\"+self._version+".zip")

                shutil.rmtree(self._dest_path+"\\temp")
                self.print.emit("info", "remove "+self._dest_path+"\\temp")

            self.print.emit("info", "packing success !!!")
            #更新进度
            self.progressChanged.emit(1.0)
            return True
        except Exception as e:
            self.print.emit("error", "ReleaseUpdater.py:PackImpl: stage2 TypeExcption: "+str(e))
        return False


    def run(self):
        self.feedback.emit(True)
        if not self.PackImpl(self._version):
            self.progressChanged.emit(0)
        else:
            self.versionChanged.emit(self._version)
            self.versionNameChanged.emit(self._version_name)
            self.minHideVersionChanged.emit(self._min_hide_version)
            self.addItem.emit(self._version, self._version_name, self._min_hide_version)
        self.feedback.emit(False)