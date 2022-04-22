#!/usr/bin/env python3.5
# coding=utf-8
import os
import datetime
from time import sleep

dict = {}

fileInfoToList = []

#import webCrawl_cookie_2nd

def readFile():
    L = []
    f = open("packageName.txt", "r")
    while True:
        test = f.readline()
        # test = test.strip()
        print("test is", test)
        sleep(0.5)
        if test == "":  # if not line:
            break
        elif test.startswith('#') or test.isspace():
            continue
        # if test.startswith('#') or test.isspace():
        #     continue
        # elif test == "":  # if not line:
        #     break
        L.append(test)
        print("L", L)
    f.close
    return L


def getNowTime():
    return str(datetime.datetime.now())


def setMd5sum(str):
    os.system("md5sum " + str + "|tee -a md5sum.txt")
    os.system("echo " + getNowTime() + "|tee -a md5sum.txt")


def setSha1sum(str):
    os.system("sha1sum " + str + "|tee -a sha1sum.txt")
    os.system("echo " + getNowTime() + "|tee -a sha1sum.txt")


# for i in readFile():
#     print i


# print fOut[1]
# print type(fOut[1])
# lastBlank = fOut[1].rindex('/')
# firstBlank = fOut[1].index('/')
# print "Last Black is", lastBlank
# print "First Black is", firstBlank
# print fOut[1][lastBlank + 1:]
def getPackageNameList(fOut):
    # fOut = readFile()
    newL = []
    for i in range(len(fOut)):
        # if i == "\n":
        #     continue
        lastSlach = fOut[i].rindex('/')
        # packageName = fOut[i][lastSlach + 1:]
        lastNewLine = fOut[i].rindex("\n")
        packageName = fOut[i][lastSlach + 1:lastNewLine]
        # packageName = fOut[i][lastSlach + 1:]
        newL.append(packageName)
    return newL


# print getPackageNameList()[0]
# print getPackageNameList()[1]

# print readFile()[0]

print("\n current os.path is", os.path, "\n")


# import os
# os.path.exists(test_file.txt)
# #True
# os.path.exists(no_exist_file.txt)
# #False

def fileExist(str):
    return os.path.exists(str)


def packageDownload(L):
    # L = getPackageNameList()
    for i in range(len(L)):
        if not fileExist(L[i]):
            os.system("wget -c " + L[i])
            os.system("sync")
        else:
            print("Duplicate file")
            setMd5sum(L[i])


def fType():
    global dict
    L = getPackageNameList()
    for i in range(len(L)):
        lastComma = L[i].rindex(".")
        lastStr = L[i][lastComma + 1:]
        dict[L[i]] = lastStr


def cutLastComma(str):
    lastComma = str.rindex(".")
    lastStr = str[lastComma + 1:]
    return lastStr


def cutLastDash(str):
    lastComma = str.rindex("-")
    lastStr = str[lastComma + 1:]
    print("lastStr", lastStr)
    return lastStr


def tarFile(L):
    # L = getPackageNameList()
    for i in range(len(L)):
        try:
            if cutLastDash(L[i]) == "REL.tgz":
                if fileExist(L[i]):
                    if not fileExist("UpdateContainer"):
                        print("======================= Start to extract =======================")
                        os.system("tar xvf " + L[i])
                        os.system("sync")
                    else:
                        print('UpdateContainer already exist!!')
                        # raise ValueError('Duplicate extract file')
                else:
                    print("File does not exist!!!")
            elif cutLastDash(L[i]) == "flashcontainer.tgz":
                if fileExist(L[i]):
                    if not fileExist("FlashContainer"):
                        print("======================= Start to extract =======================")
                        os.system("tar xvf " + L[i])
                        os.system("sync")
                    else:
                        print
                        ('FlashContainer already exist!!')
                        # raise ValueError('Duplicate extract file')
                else:
                    print("File does not exist!!!")
        except ValueError:
            print("Sorry, it's not a Tar file")


def delFile(fileName):
    if fileExist(fileName):
        os.system("rm -rf " + fileName)
        print(fileName, "have been deleted")
    else:
        print("File is not exist!!!")


# packageDownload()
# tarFile()
# L = getPackageNameList()
# for i in range(len(L)):
#     setMd5sum(L[i])
# delFile('packageName.txt')
# delFile('test1.py')


def main():
    L = readFile()
    print("\n Step1 \n")
    packageDownload(L)
    print("\n Step2 \n")
    LName = getPackageNameList(L)
    for i in range(len(LName)):
        setMd5sum(LName[i])
        setSha1sum(LName[i])
    tarFile(LName)
    # delFile('packageName.txt')
    # delFile('test1.py')


def main2():
    L = readFile()
    LName = getPackageNameList(L)
    print(LName)
    # tarFile(LName)
    for i in LName:
        try:
            print(cutLastDash(i))
        except ValueError:
            print("Cannot be cut by last dash")


print("name1", __name__)

if __name__ == '__main__':
    main()
