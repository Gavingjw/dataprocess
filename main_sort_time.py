import pandas as pd
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
    unsorted_path = './unsorted_data/'
    time_sorted_path = './sorted_time_data/'

    make_dir(time_sorted_path)
    vins = os.listdir(unsorted_path)

    for vin in vins:
        vin = vin[:vin.find('.csv')]
        try:
            try:  # reading
                print("ready reading vin {}".format(vin))
                onecardata = pd.read_csv(unsorted_path + vin + '.csv')
            except StopIteration:
                print(' csv_reading error')
                print('vin:{} reading error'.format(vin))
                continue

            try:  # writing
                print("ready sorting ...")
                onecardata.sort_values(by=['DATA_DATE']).to_csv(time_sorted_path + vin + '.csv', index=False)
                print('vin:{} is sorted and wrote success'.format(vin))

            except StopIteration:
                print(' csv_writing error')
                print('vin:{} writin error'.format(vin))
                continue

        except StopIteration:
            print("Iteration is stopped.")
            print('vin:{} sorted error'.format(vin))

        del onecardata



if __name__ == '__main__':

    main()




