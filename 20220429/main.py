#!/usr/bin/env python3.5
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import os, re, sys, time
import shelve

from auto_write_otp_v20220424 import serialNum, get_db_info, get_current_date, get_newest_value, repr_message, \
    save_to_db, get_count_from_db, redFont, greenFont


def greenFont(str):
    return "\033[32m" + str + "\033[0m"


def catFazitInfo(str):
    # p1 = re.search("2093[0-9]{4}",str)
    # X9G-101[0-9\.]{8}9[0-9]{3}[0-9]{4}
    # FAW-VW Fazit-ID Format
    # p1 = re.search("X9G-102[0-9\.]{8}9[0-9]{3}[0-9]{4}", str)
    """Change the format of record serial num as [month][date][year][countNum from 0001 to 9999]"""
    # p1 = re.search("[0-2]{1}[0-9]{1}[0-3]{1}[0-9]{1}20[2-9]{1}[0-9]{1}[0-9]{4}", str)
    # X9G-10226.11.2190020003
    # return p1.group()
    return str


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print("Hi, {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.

def setLogFile():
    scanQR = input("Please scan the QR image:")
    suffix = '.txt'
    current_location = os.popen("echo `pwd`")
    pwd = current_location.read()
    print("Print working directory:", pwd)
    filepath = pwd.strip() + '/' + catFazitInfo(scanQR) + suffix
    print('The serial num is', catFazitInfo(scanQR))
    print('File name is', filepath)
    """
    判断文件是否存在
        os.path.isfile(path)
    """
    if os.path.isfile(filepath):
        print(greenFont("Log file is created!!!"))
        return True
    else:
        return False


def setLogDirectory(dirName: str) -> bool:  # create the file, and return True when file created successfully.
    # if the pwd is exit, try to rename and create new one.
    n = 0
    while True:
        if os.path.isdir(getCurrentPWD() + "/" + dirName):
            n += 1
            dirName = dirName + str(n)
            # print("Change dirName to :", dirName)
        else:
            os.system("sudo mkdir " + dirName)
            return os.path.isdir(getCurrentPWD() + "/" + dirName)
            break


def get_num_of_same_files(fileName: str) -> list:
    p1 = re.findall()
    L = []
    return L


def getCurrentPWD() -> str:
    current_location = os.popen("echo `pwd`")
    pwd = current_location.read()
    return pwd.strip()


def confirm(func, *args, **kwargs):
    confirm_flag = 'y'
    res = input(repr_message("Input \"" + confirm_flag + "\" to Continue"))
    if res.lower() == confirm_flag:
        # func(*args, **kwargs)
        # print(str(*args))
        return func(*args, **kwargs)
    else:
        return redFont(repr_message('confirm error'))


def create_serial_num(local_db: str = 'serial_list', model_v: str = '0311'):
    """
    create a serial num depend on local shelve db
    """
    # print(get_current_date())
    # local_db = 'serial_list'
    print(get_db_info(db=local_db))
    date = get_current_date()
    if get_db_info(db=local_db) == 0:
        newHU = serialNum(date[0], date[1], date[2], model=model_v, count=str('1'))
        print(repr_message(str(newHU)))
        print(len(str(newHU)))
        return confirm(save_to_db, newHU, db=local_db)
    else:
        newHU = serialNum(date[0], date[1], date[2], model= model_v, count=str(get_count_from_db(db=local_db) + 1))
        print(repr_message(str(newHU)))
        return confirm(save_to_db, newHU, db=local_db)
    # get_db_info(db=local_db)


def main2():
    if len(sys.argv) <= 1:
        scanQR = input("Please scan the QR image:")
    else:
        # print(sys.argv[0]) --> return: main.py as sys.argv[0] cuz input is python3.5 main.py(sys.argv[0])
        scanQR = sys.argv[1]
    # New
    # if os.path.isdir(pwd.strip() + '/' + catFazitInfo(scanQR)):
    if setLogDirectory(catFazitInfo(scanQR)):
        print(greenFont("PASS"))
        os.system("sudo ./periscope -u serial:/dev/ttyUSB0 -l " + catFazitInfo(scanQR))
    else:
        print("Periscope Log directory is not created")


def create_FTDB():
    """
    create shelve db file in the first time.
    """
    # with shelve.open('serial_list') as serial_db:
    pass


if __name__ == '__main__':
    # print(confirm(len,'123'))

    scanQR = create_serial_num()
    # scanQR ='2022042703110071'
    # scanQR = str(get_newest_value(db='serial_list'))
    # print(repr_message("The newest part is " + str(scanQR)))

    if setLogDirectory(catFazitInfo(scanQR)):
        print(greenFont("PASS"))
        os.system("sudo ./periscope -u serial:/dev/ttyUSB0 -l " + catFazitInfo(scanQR))
    else:
        print("Periscope Log directory is not created")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
