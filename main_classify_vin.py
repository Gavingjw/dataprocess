

import pandas as pd
import numpy as np
import os
import shutil

def make_dir(path):
    # 文件夹

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        print(path + " delete success")

    os.makedirs(path)
    print(path + " makedir success")


def main():

    # PATH
    datainpath = "./vin_5_01.csv"
    unsorted_path = './unsorted_data/'
    vin_name_path ='./vin_name_data/'

    # PARAMETER
    loop = True
    chunkSize = 1e5
    reader = pd.read_csv(datainpath, iterator=True)

    make_dir(unsorted_path)
    make_dir(vin_name_path)
    vin_names = np.array([])

    while loop:
        try:
            chunk = reader.get_chunk(chunkSize)
            datachunk = chunk[chunk.DATA_DATE > '2012-1-1 00:00:00']
            vinonly = datachunk['VIN'].unique()

            for vin in vinonly:
                if vin in vin_names:
                    try:  # append file
                        datachunk[datachunk.VIN == vin].to_csv(unsorted_path+vin+'.csv', mode='a', index=False, header=False)
                    except StopIteration:
                        print("write csv error.")
                else:
                    try:   # new file
                        datachunk[datachunk.VIN == vin].to_csv(unsorted_path + vin + '.csv', index=False, header=True)
                    except StopIteration:
                        print("write csv error.")
            print('vinonly', vinonly)
            print('vin_names', vin_names)
            vin_names = np.unique(np.append(vin_names, vinonly)) # del dup data in file
        except StopIteration:
            print("Iteration is stopped.")
            break
    try:
        pd.DataFrame(vin_names).to_csv(unsorted_path + 'unsort_data_vin.csv', index=False, header=False)
    except StopIteration:
        print("unsort_data_vin.csv write error .")


if __name__ == '__main__':

    main()
















