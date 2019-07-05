

import pandas as pd
import csv    #加载csv包便于读取csv文件
import os
import shutil
import datetime
import time
# super parameter

TIME = datetime.datetime(2012, 1, 1, 0, 0, 0)

# model controller
MODEL1 = False
MODEL2 = False
MODEL_CLASSIFY = False
MODEL_SORT = False
MODEL_TEST = True

def main():

    datainpath = "./vin_5_01.csv"
    outpath1 = "./result1"
    outpath2 = "./result2"
    inpathvin = "./3f84d7be11993c0b.xlsx"

    if MODEL1:

        km60pathout = outpath2 + '/km60'
        km75pathout = outpath2 + '/km75'
        kmnopathout = outpath2 + '/kmno'

        writerows = 10000

        # make dir

        try:
            make_dir(outpath1)
            make_dir(outpath2)
            make_dir(km60pathout)
            make_dir(km75pathout)
            make_dir(kmnopathout)
        except:
            print("make dir fail, please make again")

        # 按照数据的vin码将数据进行分类
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('1,按照数据的vin码将数据进行分类')
        carvins = classify(datainpath, outpath1, writerows)

        # 对分好类的文件进行排序
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('2,对分好类的文件进行排序')
        km60, km75, kmno = excelread(inpathvin)
        select(list(km60), carvins, outpath1, km60pathout)
        select(list(km75), carvins, outpath1, km75pathout)
        select(list(kmno), carvins, outpath1, kmnopathout)
        print("congratulations success!")

    elif MODEL2:

        writerows = 10000

        # make dir

        try:
            make_dir(outpath1)
            make_dir(outpath2)

        except:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("make dir fail, please make again")

        # 按照数据的vin码将数据进行分类
        print('1,按照数据的vin码将数据进行分类')
        carvins = classify2(datainpath, outpath1, writerows)

        # 对分好类的文件进行排序
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('2,对分好类的文件进行排序')
        carvinss = list(set(carvins))
        for carvin in carvinss:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print('VIN {} is sorting ... '.format(carvin))
            afterprocess(pathout=outpath2, pathin=outpath1, vin=carvin)

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("congratulations success!")

    elif MODEL_CLASSIFY:
        #  afterprocess codes

        writerows = 10000

        # make dir

        try:
            make_dir(outpath1)
            make_dir(outpath2)

        except:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("make dir fail, please make again")

        # 按照数据的vin码将数据进行分类
        print('1,按照数据的vin码将数据进行分类')
        carvins = classify2(datainpath, outpath1, writerows)

        # csv文本写入函数

        pd.DataFrame(carvins).to_csv('result_vin.csv', index=False, header=False)
        print("congratulations success!")

    elif MODEL_SORT:
        #  afterprocess codes

        try:
            make_dir(outpath2)
        except:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("make dir fail, please make again")

        vins = os.listdir(outpath1)
        for carvin in vins:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print('VIN {} is sorting ... '.format(carvin))

            if carvin.find('.csv'):
                afterprocess(pathout=outpath2, pathin=outpath1, vin=carvin[:carvin.find('.csv')])
            else:
                afterprocess(pathout=outpath2, pathin=outpath1, vin=carvin)

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("congratulations success!")

    elif MODEL_TEST:
        #  afterprocess codes

        writerows = 10000

        # make dir

        try:
            make_dir(outpath1)
            make_dir(outpath2)

        except:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("make dir fail, please make again")

        # 按照数据的vin码将数据进行分类
        print('1,按照数据的vin码将数据进行分类')
        carvins = classify_test(datainpath, outpath1, writerows)

        # csv文本写入函数

        pd.DataFrame(carvins).to_csv('result_vin.csv', index=False, header=False)
        print("congratulations success!")

def make_dir(path):
    # 文件夹

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        print(path + " delete success")

    os.makedirs(path)
    print(path + " makedir success")


def classify(datapath, path, writerows):
    # 分类

    head =[]
    vinnums = []
    i = 0
    data = {}  # 创建列表准备接收csv各行数据
    try:
        csv_file = open(datapath)   #打开csv文件
        csv_reader_lines = csv.reader(csv_file)   #逐行读取csv文件

        for one_line in csv_reader_lines:
            if i == 0:
                # print(one_line)
                head = one_line  # columnls keywords
                i = i+1
                continue
            else:
                carvin = one_line[1]
                if data.get(carvin):
                    data[carvin].append(one_line)
                else:
                    data[carvin] = [one_line]
                i = i+1

            if i % writerows == 0:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print("正在中途写入...")
                print(" 运行次数：", i)
                vinnums = csvdifwrite(data, vinnums, carvin, head, path)
                data.clear()
                del data
                data = {}
                print("中途写入完成")

        # 最后将剩余的数据写入各自的文件中
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("正在收尾写入...")
        vinnums = csvdifwrite(data, vinnums, carvin, head, path)
        data.clear()
        del data

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("收尾写入完成")
        # print("vinnums",  vinnums)
        pd.DataFrame(vinnums, columns=["VIN"]).to_csv('./VIN.csv',index=False, header=True)

        # print("carvins", vinnums)
        return vinnums

    except:
        print("分类错误")
        return False


def classify2(datapath, path, writerows):
    # 分类
    # 20190628 增加功能：将时间2012年1月1日之前的数据全部删掉


    head =[]
    vinnums = []
    i = 0
    data = {}  # 创建列表准备接收csv各行数据
    try:
        csv_file = open(datapath)   #打开csv文件
        csv_reader_lines = csv.reader(csv_file)   #逐行读取csv文件

        for one_line in csv_reader_lines:

            if i == 0:
                # print(one_line)
                head = one_line  # columnls keywords
                i = i+1
                continue
            elif datetime.datetime.strptime(one_line[0], '%Y-%m-%d %H:%M:%S') > TIME:
                carvin = one_line[1]
                if data.get(carvin):
                    data[carvin].append(one_line)
                else:
                    data[carvin] = [one_line]
                i = i + 1
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print("time is not right!")

            if i % writerows == 0:

                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print(" 正在中途写入...")
                print(" 运行次数：", i)
                vinnums = csvdifwrite(data, vinnums, carvin, head, path)
                data.clear()
                del data
                data = {}
                print(" 中途写入完成")

        # 最后将剩余的数据写入各自的文件中
        print("正在收尾写入...")
        vinnums = csvdifwrite(data, vinnums, carvin, head, path)
        data.clear()
        del data

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("收尾写入完成")

        # print(" vinnums",  vinnums)
        pd.DataFrame(vinnums, columns=["VIN"]).to_csv('./VIN.csv', index=False, header=True)

        # print("carvins", vinnums)
        return vinnums

    except:
        print("分类错误")
        return False


def classify_test(datapath, path, writerows):
    # 分类
    # 20190628 增加功能：将时间2012年1月1日之前的数据全部删掉


    head =[]
    vinnums = []
    i = 0
    data = {}  # 创建列表准备接收csv各行数据
    try:
        csv_file = open(datapath)   #打开csv文件
        csv_reader_lines = csv.reader(csv_file)   #逐行读取csv文件

        for one_line in csv_reader_lines:

            if i == 0:
                # print(one_line)
                head = one_line  # columnls keywords
                i = i+1
                continue
            elif datetime.datetime.strptime(one_line[0], '%Y-%m-%d %H:%M:%S') > TIME:
                carvin = one_line[1]
                if carvin == 'LSH14J4CXGA162841':

                    print("发现目标")
                    if data.get(carvin) :
                        data[carvin].append(one_line)
                    else:
                        data[carvin] = [one_line]
                else:
                    # print("未发现目标")
                    pass

                i = i + 1
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print("time is not right!")

            if i % writerows == 0:

                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print(" 正在中途写入...")
                print(" 运行次数：", i)
                vinnums = csvdifwrite(data, vinnums, carvin, head, path)
                data.clear()
                del data
                data = {}
                print(" 中途写入完成")

        # 最后将剩余的数据写入各自的文件中
        print("正在收尾写入...")
        vinnums = csvdifwrite(data, vinnums, carvin, head, path)
        data.clear()
        del data

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("收尾写入完成")

        # print(" vinnums",  vinnums)
        pd.DataFrame(vinnums, columns=["VIN"]).to_csv('./VIN.csv', index=False, header=True)

        # print("carvins", vinnums)
        return vinnums

    except:
        print("分类错误")
        return False


def csvdifwrite(data, vinnums, carvin, head, path):
    # 文本数据追加

    nowkey = list(data.keys())
    # print('vinnums:', vinnums)
    for car in nowkey:
        print('car', car)
        if car in vinnums:
            print(car + "追加数据")
            csv_write(data, head, car, path, False)
        else:
            print(car + "新建数据")
            csv_write(data, head, car, path, True)

    vinnums += nowkey
    carvins = list(set(vinnums))

    return carvins


def csv_write(data, head, vin, path, headerbool):
    # 根据每个车辆vin进行对数据进行追加写入
    # csv文本写入函数
    print('开始写入格式...', 'vin = ', vin, 'data_len:', len(data))
    mdata = pd.DataFrame(data[vin], columns=head)
    print('开始写入...',  'mdata_len:', len(mdata))
    mdata.to_csv(path+'/'+vin + '.csv', mode='a', index=False, header=headerbool)
    print(path + '/' + vin + ".csv write success")


def sortdata(carvins, pathin, pathout):
    # 单个文本数据进行排序

    try:
        for carn in carvins:
            print("carn: ", carn)
            csv_sort_one(carn, pathin, pathout)
    except:
        print("后处理错误")


def csv_sort_one(carn, pathin, pathout):
    # 单个文本排序

    print("准备读取数据...")
    onecardata = pd.read_csv(pathin+'/'+carn+".csv")
    print(pathin + '/' + carn + ".csv read success")
    #print(onecardata)

    print("begin to write...")
    onecardata.sort_values(by=["DATA_DATE"]).to_csv(pathout+'/'+carn+".csv", index=False)
    print(pathout+'/'+carn+".csv write success")

    del onecardata


def excelread(path):
    # 分类文件读取

    km60 = pd.read_excel(path,"sheet60")
    km75 = pd.read_excel(path,"sheet75")
    kmno = pd.read_excel(path,"sheetno")
    return km60["VIN"], km75["VIN"], kmno["VIN"]


def select(vin, vins, pathindata, pathoutdata):
    # 查询，是否

    # vinnames = os.listdir(pathindata)
    findvinerro =[]
    for v in vin:
        #print(v+'.csv')

        if v in vins:
            print("数据库中已找到 vin: " + v)
            afterprocess(pathoutdata, pathindata, v)
        else:
            print("数据库中查找不到 vin: " + v)
            findvinerro.append(v)
    pd.DataFrame(findvinerro).to_csv((pathoutdata+'/findvinerro.csv'))


def afterprocess(pathout, pathin, vin):
    # 后处理文件

    print("准备读取数据...")
    onecardata = pd.read_csv(pathin + '/' + vin + '.csv')
    print(pathin + '/' + vin + " read success")

    outdata = onecardata.sort_values(by=["DATA_DATE"]).to_csv(pathout + '/' + vin + '.csv', index=False)
    print(pathout + '/' + vin + " write success")

    del onecardata, outdata


if __name__ == '__main__':

    main()
