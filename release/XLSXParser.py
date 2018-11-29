__author__ = 'shixuekai'


import xlrd
import xlwt


def OpenExcel(file = "PC客户端启动版本更新率数据.xlsx"):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


#分析启动总UV、PVsheet
def ParseExcel1Table(data, index = 0, min_hide_version = 201809262):
    table = data.sheets()[index]
    rows = table.nrows
    colums = table.ncols

    l_ver = {}
    r_ver = {}

    total_uv = 0
    total_pv = 0
    explict_total_uv = 0 # 显示
    explict_total_pv = 0
    implict_total_uv = 0
    implict_total_pv = 0


    for row in range(rows):
        row_item = table.row_values(row)
        if row_item:
            if l_ver.get(row_item[2], "null") == "null":
                l_ver[row_item[2]] = 1
            else:
                l_ver[row_item[2]] += 1

            if r_ver.get(row_item[3], "null") == "null":
                r_ver[row_item[3]] = 1
            else:
                r_ver[row_item[3]] += 1

            if type(row_item[2]) == float and row_item[2] > 0 and len(str(row_item[2])) > 9 and type(row_item[3]) == float and row_item[3] > 0 and len(str(row_item[3])) > 9 and row_item[3] > min_hide_version:
                total_uv += row_item[4]
                total_pv += row_item[5]

                if row_item[2] < min_hide_version and row_item[3] > min_hide_version:
                    explict_total_uv += row_item[4]
                    explict_total_pv += row_item[5]
                elif row_item[2] >= min_hide_version and row_item[3] > row_item[2]:
                    implict_total_uv += row_item[4]
                    implict_total_pv += row_item[5]

                else:
                    print("row="+str(row))

    print("l_ver="+str(l_ver))

    print("r_ver="+str(r_ver))

    print("total_uv="+str(total_uv))
    print("total_pv="+str(total_pv))
    print("explict_total_uv="+str(explict_total_uv))
    print("explict_total_pv="+str(explict_total_pv))
    print("implict_total_uv="+str(implict_total_uv))
    print("implict_total_pv="+str(implict_total_pv))


#更新成功与失败PV、UV
def ParseExcel2Table(data, index = 1, min_hide_version = 201809262):
    table = data.sheets()[index]
    rows = table.nrows
    colums = table.ncols

    l_ver = {}
    r_ver = {}

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
        if row_item:
            if l_ver.get(row_item[2], "null") == "null":
                l_ver[row_item[2]] = 1
            else:
                l_ver[row_item[2]] += 1

            if r_ver.get(row_item[3], "null") == "null":
                r_ver[row_item[3]] = 1
            else:
                r_ver[row_item[3]] += 1


            if type(row_item[2]) == float and row_item[2] > 0 and len(str(row_item[2])) > 9 and type(row_item[3]) == float and row_item[3] > 0 and len(str(row_item[3])) > 9  and row_item[3]!= row_item[2] and row_item[3] > min_hide_version:
                total_uv += row_item[8]
                total_pv += row_item[9]

                if row_item[2] < min_hide_version and row_item[3] > min_hide_version:
                    explict_total_uv += row_item[8]
                    explict_total_pv += row_item[9]
                    success_explict_total_uv += row_item[4]
                    success_explict_total_pv += row_item[6]
                    fail_explict_total_uv += row_item[5]
                    fail_explict_total_pv += row_item[7]

                elif row_item[2] >= min_hide_version and row_item[3] > row_item[2]:
                    implict_total_uv += row_item[8]
                    implict_total_pv += row_item[9]
                    success_implict_total_uv += row_item[4]
                    success_implict_total_pv += row_item[6]
                    fail_implict_total_uv += row_item[5]
                    fail_implict_total_pv += row_item[7]

                else:
                    print("row="+str(row))

    print("l_ver="+str(l_ver))

    print("r_ver="+str(r_ver))

    print("total_uv="+str(total_uv))
    print("total_pv="+str(total_pv))
    print("explict_total_uv="+str(explict_total_uv))
    print("explict_total_pv="+str(explict_total_pv))
    print("success_explict_total_uv="+str(success_explict_total_uv))
    print("success_explict_total_pv="+str(success_explict_total_pv))
    print("fail_explict_total_uv="+str(fail_explict_total_uv))
    print("fail_explict_total_pv="+str(fail_explict_total_pv))
    print("implict_total_uv="+str(implict_total_uv))
    print("implict_total_pv="+str(implict_total_pv))
    print("success_implict_total_uv="+str(success_implict_total_uv))
    print("success_implict_total_pv="+str(success_implict_total_pv))
    print("fail_implict_total_uv="+str(fail_implict_total_uv))
    print("fail_implict_total_pv="+str(fail_implict_total_pv))


#隐式拷贝成功失败PV、UV
def ParseExcel3Table(data, index = 2, min_hide_version = 201809262):
    table = data.sheets()[index]
    rows = table.nrows
    colums = table.ncols

    l_ver = {}
    r_ver = {}

    total_uv = 0
    total_pv = 0
    success_total_uv = 0 # 显示
    success_total_pv = 0
    fail_total_uv = 0
    fail_total_pv = 0


    for row in range(rows):
        row_item = table.row_values(row)
        if row_item:
            if l_ver.get(row_item[2], "null") == "null":
                l_ver[row_item[2]] = 1
            else:
                l_ver[row_item[2]] += 1

            if r_ver.get(row_item[3], "null") == "null":
                r_ver[row_item[3]] = 1
            else:
                r_ver[row_item[3]] += 1

            if type(row_item[2]) == float and row_item[2] > 0 and len(str(row_item[2])) > 9 and type(row_item[3]) == float and row_item[3] > 0 and len(str(row_item[3])) > 9 and row_item[2]>=min_hide_version and row_item[3] > row_item[2]:
                total_uv += row_item[8]
                total_pv += row_item[9]


                success_total_uv += row_item[4]
                success_total_pv += row_item[6]
                fail_total_uv += row_item[5]
                fail_total_pv += row_item[7]

            else:
                print("row="+str(row))

    print("l_ver="+str(l_ver))

    print("r_ver="+str(r_ver))

    print("total_uv="+str(total_uv))
    print("total_pv="+str(total_pv))
    print("success_total_uv="+str(success_total_uv))
    print("success_total_pv="+str(success_total_pv))
    print("fail_total_uv="+str(fail_total_uv))
    print("fail_total_pv="+str(fail_total_pv))



##data  = OpenExcel()
##ParseExcel1Table(data)
##print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -----------------------------------------------\n")
##ParseExcel2Table(data)
##print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -----------------------------------------------\n")
##ParseExcel3Table(data)
import pefile
def IsSigned():
    pe = pefile.PE("D:\\dy_pcclient\\final-qt5.10.1\\dy_PCClient.exe")
    for section in pe.sections:
        print( section)


IsSigned()


