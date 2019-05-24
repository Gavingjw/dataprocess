

import pandas as pd
import csv    #加载csv包便于读取csv文件
import os
import shutil


def main():

    datainpath = "./vin_5_01.csv"
    outpath1 = "./result1"
    outpath2 = "./result2"

    try:
        make_dir(outpath1)
        make_dir(outpath2)
    except:
        print("make dir fail, please make again")


    print('1,按照数据的vin码将数据进行分类')
    carvins = classy(datainpath, outpath1)

    print('2,对分好类的文件进行排序')

    sortdata(carvins, outpath1, outpath2)

    print("congratulations success!")


def make_dir(path):

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        print(path + " delete success")

    os.makedirs(path)
    print(path + " makedir success")


def classy(datapath, path):
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
                i=i+1
                continue
            else:
                carvin = one_line[1]
                if data.get(carvin):
                    data[carvin].append(one_line)
                else:
                    data[carvin] = [one_line]
                i = i+1

            if len(data[carvin]) > 500000:
                print("正在中途写入...")
                for car in data.keys():
                    csv_write(data, head, car, path)
                vinnums += list(data.keys())

                data.clear()
                del data
                data = {}

            if i%100000 == 0:
                print("运行次数：", i)

        # 最后将剩余的数据写入各自的文件中
        for car in data.keys():
            print("正在收尾写入...")
            csv_write(data, head, car, path)
        vinnums += list(data.keys())
        data.clear()
        del data


        print(" vinnums",  vinnums)
        carvins = list(set(vinnums))
        pd.DataFrame(carvins, columns=["VIN"]).to_csv('./VIN.csv',index=False, header=True)
        # print(data)
        #carvins = tuple(data.keys())

        print("carvins", carvins)
        return carvins

    except:
        print("分类错误")
        return False


def csv_write(data, head, vin, path):
    # 根据每个车辆vin进行对数据进行追加写入
    Mdata = pd.DataFrame(data[vin], columns=head)
    Mdata.to_csv(path+'/'+vin + '.csv', mode='a', index=False, header=True)
    print(path + '/' + vin + ".csv write success")


def sortdata(carvins, pathin, pathout):

    try:
        for carn in carvins:
            print("carn: ", carn)
            csv_sort_one(carn, pathin, pathout)
    except:
        print("后处理错误")


def csv_sort_one(carn, pathin, pathout):
    print("准备读取数据...")
    onecardata = pd.read_csv(pathin+'/'+carn+".csv")
    print(pathin + '/' + carn + ".csv read success")
    #print(onecardata)

    print("begin to write...")
    onecardata.sort_values(by=["DATA_DATE"]).to_csv(pathout+'/'+carn+".csv", index=False)
    print(pathout+'/'+carn+".csv write success")

    del onecardata



if __name__ == '__main__':

    main()
