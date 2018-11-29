__author__ = 'shixuekai'

import os, configparser, xlrd, xlwt
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt, QThread

class UpdateRater(QThread):
    print = pyqtSignal(str, str, arguments = ["level", "msg"],name="print")
    progressChanged = pyqtSignal(float, arguments = ["percent"],name="progressChanged")
    feedback = pyqtSignal(bool, arguments = ["enable"],name="feedback")

    totalLauncherChanged = pyqtSignal(list, arguments = ["tlmodel"],name="totalLauncherChanged")
    explicitLauncherChanged = pyqtSignal(list, arguments = ["elmodel"],name="explicitLauncherChanged")
    implicitLauncherChanged = pyqtSignal(list, arguments = ["ilmodel"],name="implicitLauncherChanged")

    totalDownloadChanged = pyqtSignal(list, arguments = ["tdmodel"],name="totalDownloadChanged")
    explicitDownloadChanged = pyqtSignal(list, arguments = ["edmodel"],name="explicitDownloadChanged")
    implicitDownloadChanged = pyqtSignal(list, arguments = ["idmodel"],name="implicitDownloadChanged")

    implicitCopyChanged = pyqtSignal(list, arguments = ["icmodel"],name="implicitCopyChanged")

    rateChanged = pyqtSignal(list, arguments = ["rmodel"],name="rateChanged")

    startDateListChanged = pyqtSignal(list, int, arguments = ["sdlmodel", "focusindex"],name="startDateListChanged")
    endDateListChanged = pyqtSignal(list, int, arguments = ["edlmodel", "focusindex"],name="endDateListChanged")

    startVersionListChanged = pyqtSignal(list, arguments = ["svlmodel"],name="startVersionListChanged")

    endVersionListChanged = pyqtSignal(list, arguments = ["evlmodel"],name="endVersionListChanged")


    def __init__(self, parent=None):
        super(QObject, self).__init__(parent)
        self._update_version_data = {}
        self._excel_table = None
        self._excel_path = ""
        self._success_explicit_pv = 0
        self._explicit_launcher_pv = 0
        self._success_implicit_pv = 0
        self._implicit_launcher_pv = 0

        self._date_list = ["ALL"]
        self._start_version_list = ["ALL"]
        self._end_version_list = ["ALL"]

        self._start_day_index = 0
        self._end_day_index = 0
        self._start_version_index = 0
        self._end_version_index = 0


    def runImpl(self):
        self.feedback.emit(True)
        if self.OpenExcel():
            self.progressChanged.emit(0.25)
            self.CensusSheet_1()
            self.progressChanged.emit(0.50)
            self.CensusSheet_2()
            self.progressChanged.emit(0.75)
            self.CensusSheet_3()
            self.progressChanged.emit(1.0)
            self.CensusRate()
        else:
            self.progressChanged.emit(0.0)
            self.print.emit("error", "OpenExcel fail!!!")

        self.feedback.emit(False)


    def run(self):
        startday = int(self._date_list[self._start_day_index])
        endday = int(self._date_list[-(self._end_day_index + 1)])

        start = None
        if self._start_version_index != 0 and self._start_version_index < len(self._start_version_list):
            start = int(self._start_version_list[self._start_version_index])

        end = None
        if self._end_version_index != 0 and self._end_version_index < len(self._end_version_list):
            end = int(self._end_version_list[self._end_version_index])

        self.CensusSheetByCondition_1(startday, endday, start, end)
        self.CensusSheetByCondition_2(startday, endday, start, end)
        self.CensusSheetByCondition_3(startday, endday, start, end)
        self.CensusRate()


    @pyqtSlot(str)
    def autoCensus(self, path):
        self._excel_path = path
        self.start()


    @pyqtSlot(dict)
    def onUpdateVersionData(self, data):
        self._update_version_data = data


    @pyqtSlot(str)
    def reload(self, file):
        self._excel_path = file
        if self.OpenExcel():
            if self.ParseExcel():
                self.feedback.emit(False)
        else:
            self.progressChanged.emit(0.0)
            self.print.emit("error", "OpenExcel fail!!!")


    @pyqtSlot(int, int)
    def censusByCondition(self, startindex, endindex):
        self._start_version_index = startindex
        self._end_version_index = endindex
        self.start()


    @pyqtSlot(int)
    def adjustStartDate(self, start):
        if start == self._start_day_index:
            return
        else:
            self._start_day_index = start
            self.endDateListChanged.emit(self._date_list[self._start_day_index:], self._end_day_index)


    @pyqtSlot(int)
    def adjustEndDate(self, end):
        if end == self._end_day_index:
            return
        else:
            print("end = "+str(end))
            self._end_day_index = end
            total_len = len(self._date_list) - self._end_day_index
            self.startDateListChanged.emit(self._date_list[0:total_len], self._start_day_index)
            print("self._start_day_index = "+str(self._start_day_index))


    #无条件统计表一
    def CensusSheet_1(self):
        if self._excel_table == None:
            self.print.emit("error", "sheet 1 excel table is none")
            return False

        table = self._excel_table.sheets()[0]
        rows = table.nrows

        total_uv = 0
        total_pv = 0
        explict_total_uv = 0 # 显示
        explict_total_pv = 0
        implict_total_uv = 0
        implict_total_pv = 0


        for row in range(rows):
            row_item = table.row_values(row)

            if type(row_item[3]) != float:
                continue

            r_ver = int(row_item[3])
            o = self._update_version_data.get(str(r_ver), None)
            if o == None:
                self.print.emit("error", "sheet 1 row = "+str(row)+"  r_ver="+str(r_ver)+" error!!!")
                continue

            total_uv += row_item[4]
            total_pv += row_item[5]

            min_hide_version = o["minHideVersion"]

            if row_item[2] > 0 and row_item[3] > 0 and row_item[2] >= min_hide_version and row_item[2] < row_item[3]:
                implict_total_uv += row_item[4]
                implict_total_pv += row_item[5]
            elif row_item[2] > 0 and row_item[3] > 0 and row_item[2] < min_hide_version:
                explict_total_uv += row_item[4]
                explict_total_pv += row_item[5]
            else:
                self.print.emit("warn", "sheet 1 row="+str(row)+" l_ver="+str(row_item[2])+"  r_ver="+str(r_ver))

        tlmodel = []
        c1 = {}
        c1["_name"] = "启动总UV:"
        c1["_value"] = str(total_uv)
        tlmodel.append(c1)

        c2 = {}
        c2["_name"] = "启动总PV:"
        c2["_value"] = total_pv
        tlmodel.append(c2)
        self.totalLauncherChanged.emit(tlmodel)


        elmodel = []
        c3 = {}
        c3["_name"] = "显示启动总UV:"
        c3["_value"] = explict_total_uv
        elmodel.append(c3)

        c4 = {}
        c4["_name"] = "显示启动总PV:"
        c4["_value"] = explict_total_pv
        elmodel.append(c4)
        self.explicitLauncherChanged.emit(elmodel)


        ilmodel = []
        c5 = {}
        c5["_name"] = "隐式启动总UV:"
        c5["_value"] = implict_total_uv
        ilmodel.append(c5)

        c6 = {}
        c6["_name"] = "隐式启动总PV:"
        c6["_value"] = implict_total_pv
        ilmodel.append(c6)
        self.implicitLauncherChanged.emit(ilmodel)

        self._explicit_launcher_pv = explict_total_pv
        self._implicit_launcher_pv = implict_total_pv
        return True


    #有条件的统计表一
    def CensusSheetByCondition_1(self, startday, endday, start=None, end=None):
        if self._excel_table == None:
            self.print.emit("error", "sheet 1 excel table is none")
            return False

        table = self._excel_table.sheets()[0]
        rows = table.nrows

        total_uv = 0
        total_pv = 0
        explict_total_uv = 0 # 显示
        explict_total_pv = 0
        implict_total_uv = 0
        implict_total_pv = 0


        for row in range(rows):
            row_item = table.row_values(row)

            #时间条件过滤
            if type(row_item[0]) == float:
                dayint = int(row_item[0])
                if dayint < startday or dayint > endday:
                    continue
            else:
                continue

            #起始版本条件过滤
            if start != None:
                if type(row_item[2]) == float:
                    if int(row_item[2]) != start:
                        continue
                else:
                    continue

            #中止版本条件过滤
            if end != None:
                if type(row_item[3]) == float:
                    if int(row_item[3]) != end:
                        continue
                else:
                    continue

            if type(row_item[3]) != float:
                continue

            r_ver = int(row_item[3])
            o = self._update_version_data.get(str(r_ver), None)
            if o == None:
                self.print.emit("error", "sheet 1 row="+str(row)+" data="+str(row_item))
                continue

            total_uv += row_item[4]
            total_pv += row_item[5]

            min_hide_version = o["minHideVersion"]

            if row_item[2] > -1 and row_item[3] > 0 and row_item[2] >= min_hide_version and row_item[2] <= row_item[3]:
                implict_total_uv += row_item[4]
                implict_total_pv += row_item[5]
            elif row_item[2] > -1 and row_item[3] > 0 and row_item[2] < min_hide_version:
                explict_total_uv += row_item[4]
                explict_total_pv += row_item[5]
            else:
                self.print.emit("warn", "sheet 1 row="+str(row)+" data="+str(row_item))

        tlmodel = []
        c1 = {}
        c1["_name"] = "启动总UV:"
        c1["_value"] = str(total_uv)
        tlmodel.append(c1)

        c2 = {}
        c2["_name"] = "启动总PV:"
        c2["_value"] = total_pv
        tlmodel.append(c2)
        self.totalLauncherChanged.emit(tlmodel)


        elmodel = []
        c3 = {}
        c3["_name"] = "显示启动总UV:"
        c3["_value"] = explict_total_uv
        elmodel.append(c3)

        c4 = {}
        c4["_name"] = "显示启动总PV:"
        c4["_value"] = explict_total_pv
        elmodel.append(c4)
        self.explicitLauncherChanged.emit(elmodel)


        ilmodel = []
        c5 = {}
        c5["_name"] = "隐式启动总UV:"
        c5["_value"] = implict_total_uv
        ilmodel.append(c5)

        c6 = {}
        c6["_name"] = "隐式启动总PV:"
        c6["_value"] = implict_total_pv
        ilmodel.append(c6)
        self.implicitLauncherChanged.emit(ilmodel)

        self._explicit_launcher_pv = explict_total_pv
        self._implicit_launcher_pv = implict_total_pv
        return True


    #无条件的统计表二
    def CensusSheet_2(self):
        if self._excel_table == None:
            self.print.emit("error", "sheet 2 excel table is none")
            return False
        table = self._excel_table.sheets()[1]
        rows = table.nrows

        total_uv = 0
        total_pv = 0

        explict_total_uv = 0 # 显示
        explict_total_pv = 0
        success_explict_total_uv = 0
        success_explict_total_pv = 0
        fail_explict_total_uv = 0
        fail_explict_total_pv = 0

        implict_total_uv = 0
        implict_total_pv = 0
        success_implict_total_uv = 0
        success_implict_total_pv = 0
        fail_implict_total_uv = 0
        fail_implict_total_pv = 0


        for row in range(rows):
            row_item = table.row_values(row)

            if type(row_item[3]) != float:
                continue

            r_ver = int(row_item[3])
            o = self._update_version_data.get(str(r_ver), None)
            if o == None:
                self.print.emit("error", "sheet 2 row = "+str(row)+"  r_ver="+str(r_ver)+" error!!!")
                continue

            min_hide_version = o["minHideVersion"]


            total_uv += row_item[8]
            total_pv += row_item[9]


            if row_item[2] > 0 and row_item[3] > 0 and row_item[2] >= min_hide_version and row_item[2] < row_item[3]:
                implict_total_uv += row_item[8]
                implict_total_pv += row_item[9]
                success_implict_total_uv += row_item[4]
                success_implict_total_pv += row_item[6]
                fail_implict_total_uv += row_item[5]
                fail_implict_total_pv += row_item[7]
            elif row_item[2] > 0 and row_item[3] > 0 and row_item[2] < min_hide_version:
                explict_total_uv += row_item[8]
                explict_total_pv += row_item[9]
                success_explict_total_uv += row_item[4]
                success_explict_total_pv += row_item[6]
                fail_explict_total_uv += row_item[5]
                fail_explict_total_pv += row_item[7]
            else:
                self.print.emit("warn", "sheet 2 row="+str(row)+"  l_ver="+str(row_item[2])+"  r_ver="+str(row_item[3])+" error!!!")

        tdmodel = []
        c1 = {}
        c1["_name"] = "下载总UV:"
        c1["_value"] = total_uv
        tdmodel.append(c1)

        c2 = {}
        c2["_name"] = "下载总PV:"
        c2["_value"] = total_pv
        tdmodel.append(c2)
        self.totalDownloadChanged.emit(tdmodel)


        edmodel = []
        c3 = {}
        c3["_name"] = "显示更新成功与否UV:"
        c3["_value"] = explict_total_uv
        edmodel.append(c3)

        c4 = {}
        c4["_name"] = "显示更新成功与否PV:"
        c4["_value"] = explict_total_pv
        edmodel.append(c4)

        c5 = {}
        c5["_name"] = "显示更新成功UV:"
        c5["_value"] = success_explict_total_uv
        edmodel.append(c5)

        c6 = {}
        c6["_name"] = "显示更新成功PV:"
        c6["_value"] = success_explict_total_pv
        edmodel.append(c6)

        c7 = {}
        c7["_name"] = "显示更新失败UV:"
        c7["_value"] = fail_explict_total_uv
        edmodel.append(c7)

        c8 = {}
        c8["_name"] = "显示更新失败PV:"
        c8["_value"] = fail_explict_total_pv
        edmodel.append(c8)
        self.explicitDownloadChanged.emit(edmodel)

        idmodel = []
        c9 = {}
        c9["_name"] = "隐式更新成功与否UV:"
        c9["_value"] = implict_total_uv
        idmodel.append(c9)

        c10 = {}
        c10["_name"] = "隐式更新成功与否PV:"
        c10["_value"] = implict_total_pv
        idmodel.append(c10)

        c11 = {}
        c11["_name"] = "隐式更新成功UV:"
        c11["_value"] = success_implict_total_uv
        idmodel.append(c11)

        c12 = {}
        c12["_name"] = "隐式更新成功PV:"
        c12["_value"] = success_implict_total_pv
        idmodel.append(c12)

        c13 = {}
        c13["_name"] = "隐式更新失败UV:"
        c13["_value"] = fail_implict_total_uv
        idmodel.append(c13)

        c14 = {}
        c14["_name"] = "隐式更新失败PV:"
        c14["_value"] = fail_implict_total_pv
        idmodel.append(c14)
        self.implicitDownloadChanged.emit(idmodel)

        self._success_explicit_pv = success_explict_total_pv
        return True


    #有条件的统计表二
    def CensusSheetByCondition_2(self, startday, endday, start=None, end=None):
        if self._excel_table == None:
            self.print.emit("error", "sheet 2 excel table is none")
            return False
        table = self._excel_table.sheets()[1]
        rows = table.nrows

        total_uv = 0
        total_pv = 0

        explict_total_uv = 0 # 显示
        explict_total_pv = 0
        success_explict_total_uv = 0
        success_explict_total_pv = 0
        fail_explict_total_uv = 0
        fail_explict_total_pv = 0

        implict_total_uv = 0
        implict_total_pv = 0
        success_implict_total_uv = 0
        success_implict_total_pv = 0
        fail_implict_total_uv = 0
        fail_implict_total_pv = 0


        for row in range(rows):
            row_item = table.row_values(row)

            #时间条件过滤
            if type(row_item[0]) == float:
                dayint = int(row_item[0])
                if dayint < startday or dayint > endday:
                    continue
            else:
                continue

            #起始版本条件过滤
            if start != None:
                if type(row_item[2]) == float:
                    if int(row_item[2]) != start:
                        continue
                else:
                    continue

            #中止版本条件过滤
            if end != None:
                if type(row_item[3]) == float:
                    if int(row_item[3]) != end:
                        continue
                else:
                    continue

            if type(row_item[3]) != float:
                continue

            r_ver = int(row_item[3])
            o = self._update_version_data.get(str(r_ver), None)
            if o == None:
                self.print.emit("error", "sheet 2 row="+str(row)+"  data="+str(row_item))
                continue

            min_hide_version = o["minHideVersion"]


            total_uv += row_item[8]
            total_pv += row_item[9]


            if row_item[2] > -1 and row_item[3] > 0 and row_item[2] >= min_hide_version and row_item[2] <= row_item[3]:
                implict_total_uv += row_item[8]
                implict_total_pv += row_item[9]
                success_implict_total_uv += row_item[4]
                success_implict_total_pv += row_item[6]
                fail_implict_total_uv += row_item[5]
                fail_implict_total_pv += row_item[7]
            elif row_item[2] > -1 and row_item[3] > 0 and row_item[2] < min_hide_version:
                explict_total_uv += row_item[8]
                explict_total_pv += row_item[9]
                success_explict_total_uv += row_item[4]
                success_explict_total_pv += row_item[6]
                fail_explict_total_uv += row_item[5]
                fail_explict_total_pv += row_item[7]
            else:
                self.print.emit("warn", "sheet 2 row="+str(row)+"  data="+str(row_item))

        tdmodel = []
        c1 = {}
        c1["_name"] = "下载总UV:"
        c1["_value"] = total_uv
        tdmodel.append(c1)

        c2 = {}
        c2["_name"] = "下载总PV:"
        c2["_value"] = total_pv
        tdmodel.append(c2)
        self.totalDownloadChanged.emit(tdmodel)


        edmodel = []
        c3 = {}
        c3["_name"] = "显示更新成功与否UV:"
        c3["_value"] = explict_total_uv
        edmodel.append(c3)

        c4 = {}
        c4["_name"] = "显示更新成功与否PV:"
        c4["_value"] = explict_total_pv
        edmodel.append(c4)

        c5 = {}
        c5["_name"] = "显示更新成功UV:"
        c5["_value"] = success_explict_total_uv
        edmodel.append(c5)

        c6 = {}
        c6["_name"] = "显示更新成功PV:"
        c6["_value"] = success_explict_total_pv
        edmodel.append(c6)

        c7 = {}
        c7["_name"] = "显示更新失败UV:"
        c7["_value"] = fail_explict_total_uv
        edmodel.append(c7)

        c8 = {}
        c8["_name"] = "显示更新失败PV:"
        c8["_value"] = fail_explict_total_pv
        edmodel.append(c8)
        self.explicitDownloadChanged.emit(edmodel)

        idmodel = []
        c9 = {}
        c9["_name"] = "隐式更新成功与否UV:"
        c9["_value"] = implict_total_uv
        idmodel.append(c9)

        c10 = {}
        c10["_name"] = "隐式更新成功与否PV:"
        c10["_value"] = implict_total_pv
        idmodel.append(c10)

        c11 = {}
        c11["_name"] = "隐式更新成功UV:"
        c11["_value"] = success_implict_total_uv
        idmodel.append(c11)

        c12 = {}
        c12["_name"] = "隐式更新成功PV:"
        c12["_value"] = success_implict_total_pv
        idmodel.append(c12)

        c13 = {}
        c13["_name"] = "隐式更新失败UV:"
        c13["_value"] = fail_implict_total_uv
        idmodel.append(c13)

        c14 = {}
        c14["_name"] = "隐式更新失败PV:"
        c14["_value"] = fail_implict_total_pv
        idmodel.append(c14)
        self.implicitDownloadChanged.emit(idmodel)

        self._success_explicit_pv = success_explict_total_pv
        return True


    #无条件的统计表三
    def CensusSheet_3(self):
        if self._excel_table == None:
            self.print.emit("error", "sheet 3 excel table is none")
            return False

        table = self._excel_table.sheets()[2]
        rows = table.nrows

        total_uv = 0
        total_pv = 0
        success_total_uv = 0 # 显示
        success_total_pv = 0
        fail_total_uv = 0
        fail_total_pv = 0


        for row in range(rows):
            row_item = table.row_values(row)

            if type(row_item[3]) != float:
                continue

            total_uv += row_item[8]
            total_pv += row_item[9]

            success_total_uv += row_item[4]
            success_total_pv += row_item[6]
            fail_total_uv += row_item[5]
            fail_total_pv += row_item[7]

        icmodel = []
        c1 = {}
        c1["_name"] = "隐式拷贝成功与否UV:"
        c1["_value"] = total_uv
        icmodel.append(c1)

        c2 = {}
        c2["_name"] = "隐式拷贝成功与否PV:"
        c2["_value"] = total_pv
        icmodel.append(c2)

        edmodel = []
        c3 = {}
        c3["_name"] = "隐式拷贝成功UV:"
        c3["_value"] = success_total_uv
        icmodel.append(c3)

        c4 = {}
        c4["_name"] = "隐式拷贝成功PV:"
        c4["_value"] = success_total_pv
        icmodel.append(c4)

        c5 = {}
        c5["_name"] = "隐式拷贝失败UV:"
        c5["_value"] = fail_total_uv
        icmodel.append(c5)

        c6 = {}
        c6["_name"] = "隐式拷贝失败PV:"
        c6["_value"] = fail_total_pv
        icmodel.append(c6)

        self.implicitCopyChanged.emit(icmodel)

        self._success_implicit_pv = success_total_pv
        return True


    #有条件的统计表三
    def CensusSheetByCondition_3(self, startday, endday, start=None, end=None):
        if self._excel_table == None:
            self.print.emit("error", "sheet 3 excel table is none")
            return False

        table = self._excel_table.sheets()[2]
        rows = table.nrows

        total_uv = 0
        total_pv = 0
        success_total_uv = 0 # 显示
        success_total_pv = 0
        fail_total_uv = 0
        fail_total_pv = 0


        for row in range(rows):
            row_item = table.row_values(row)

            #时间条件过滤
            if type(row_item[0]) == float:
                dayint = int(row_item[0])
                if dayint < startday or dayint > endday:
                    continue
            else:
                continue

            #起始版本条件过滤
            if start != None:
                if type(row_item[2]) == float:
                    if int(row_item[2]) != start:
                        continue
                else:
                    continue

            #中止版本条件过滤
            if end != None:
                if type(row_item[3]) == float:
                    if int(row_item[3]) != end:
                        continue
                else:
                    continue

            if type(row_item[3]) != float:
                continue

            r_ver = int(row_item[3])
            if None == self._update_version_data.get(str(r_ver), None):
                self.print.emit("error", "sheet 3 row="+str(row)+"  data="+str(row_item))
                continue

            total_uv += row_item[8]
            total_pv += row_item[9]

            success_total_uv += row_item[4]
            success_total_pv += row_item[6]
            fail_total_uv += row_item[5]
            fail_total_pv += row_item[7]

        icmodel = []
        c1 = {}
        c1["_name"] = "隐式拷贝成功与否UV:"
        c1["_value"] = total_uv
        icmodel.append(c1)

        c2 = {}
        c2["_name"] = "隐式拷贝成功与否PV:"
        c2["_value"] = total_pv
        icmodel.append(c2)

        edmodel = []
        c3 = {}
        c3["_name"] = "隐式拷贝成功UV:"
        c3["_value"] = success_total_uv
        icmodel.append(c3)

        c4 = {}
        c4["_name"] = "隐式拷贝成功PV:"
        c4["_value"] = success_total_pv
        icmodel.append(c4)

        c5 = {}
        c5["_name"] = "隐式拷贝失败UV:"
        c5["_value"] = fail_total_uv
        icmodel.append(c5)

        c6 = {}
        c6["_name"] = "隐式拷贝失败PV:"
        c6["_value"] = fail_total_pv
        icmodel.append(c6)

        self.implicitCopyChanged.emit(icmodel)

        self._success_implicit_pv = success_total_pv
        return True


    #更新率统计
    def CensusRate(self):
        rmodel = []
        c1 = {}
        c1["_name"] = "显示更新率（成功pv/启动pv）"
        if self._explicit_launcher_pv != 0 and self._success_explicit_pv != 0:
            c1["_value"] = float('%.2f' % (self._success_explicit_pv / self._explicit_launcher_pv))
        else:
            c1["_value"] = 0
        rmodel.append(c1)

        c2 = {}
        c2["_name"] = "隐式更新率（成功pv/启动pv）"
        if self._implicit_launcher_pv != 0 and self._success_implicit_pv != 0:
            c2["_value"] = float('%.2f' % (self._success_implicit_pv / self._implicit_launcher_pv))
        else:
            c2["_value"] = 0
        rmodel.append(c2)

        self.rateChanged.emit(rmodel)
        pass


    #"PC客户端启动版本更新率数据.xlsx"
    def OpenExcel(self):
        if not os.path.exists(self._excel_path):
            self.print.emit("error", self._excel_path+" no exist!!!")
            return False

        try:
            self._excel_table = xlrd.open_workbook(self._excel_path)
            if self._excel_table != None and self._excel_table.nsheets > 3:
                return True

            self.print.emit("error", "sheet count = "+str(self._excel_table.nsheets))
        except Exception as e:
            self.print.emit("error", "UpdateRater.py:OpenExcel: TypeException: "+str(e))
        return False


    def ParseExcel(self):
        if self._excel_table == None:
            self.print.emit("error", "sheet 1 excel table is none")
            return False

        date_list = {}
        start_version_list = {}
        end_version_list = {}

        table = self._excel_table.sheets()[0]
        rows = table.nrows

        for row in range(rows):
            row_item = table.row_values(row)
            if  type(row_item[0]) == float:
                date = int(row_item[0])
                date_list[str(date)] = 1


            if type(row_item[2]) == float:
                start = int(row_item[2])
                if  len(str(start)) == 9:
                    start_version_list[str(start)] = 1

            if type(row_item[3]) == float:
                end = int(row_item[3])
                end_version_list[str(end)] = 1

        self._date_list =  list(date_list.keys())
        self._start_day_index = 0
        self._end_day_index = 0
        self._date_list.sort()
        self.startDateListChanged.emit(self._date_list, self._start_day_index)
        self.endDateListChanged.emit(self._date_list, self._end_day_index)

        self._start_version_list = []
        self._start_version_list.append("All")
        self._start_version_list += start_version_list.keys()
        self.startVersionListChanged.emit(self._start_version_list)

        self._end_version_list = []
        self._end_version_list.append("All")
        self._end_version_list += end_version_list.keys()
        self.endVersionListChanged.emit(self._end_version_list)
        return True