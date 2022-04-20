#!/usr/bin/env python3.5
# coding="utf-8"

import os
import pexpect, sys

# class
#
#
# def create_a_serialNum(title = "37W_CL1_"):
#     """
#
#     :param title:
#     :return: A serial time as string type which depend on the localtime.
#     """
#     from time import localtime
#     str(localtime().tm_year) + \
#
#     if len(str(localtime().tm_mon)) == 1:


import shelve

import time

#
# class AttrDisplay:
#     """
#     Provides an inheritable(inˈherədəb(ə)l) display overload method that shows instance with their class
#     names and a name=value pair for each attribute stored on the instance itself (but not attrs inherited from its
#     class). Can be mixed into any class, and will work on any instance
#     """
#
#     def gatherAttrs(self):
#         attrs = []
#         for key in sorted(self.__dict__):
#             attrs.append('%s=%+3s' % (key, getattr(self, key)))
#         return ', '.join(attrs)
#
#     def __repr__(self):
#         return '[%s: %s]' % (self.__class__.__name__, self.gatherAttrs())
#
#
# def auto_fill_zero(count_num: str) -> str:
#     """
#
#     :param count: input str
#     :return: str which format as "0001"
#     """
#     if len(count_num) == 4:
#         return count_num
#     else:
#         count_num = "0" + count_num
#         return auto_fill_zero(count_num)
#
#
# class serialNum(AttrDisplay):
#     def __init__(self, year, month, day, model='B', count='1'):
#         self.year = year
#         self.month = month
#         self.day = day
#         self.model = model
#         self.count = count
#
#     def __repr__(self):
#         return self.year + self.month + self.day + self.model + auto_fill_zero(str(self.count))

"""
The from...import... command is very important, do not delete.
"""
import sys





if __name__ == '__main__':
    # print(type(create_a_serialNum()))
    # print(create_a_serialNum())
    sys.path.append('/home/jpcc/Documents/MQB_CL1/8100-rc2-MQB-GBT-CL1/otp_scripts')
    print(sys.path)
    from auto_write_otp import serialNum, auto_fill_zero, AttrDisplay, greenFont, redFont
    db = "/home/jpcc/Documents/MQB_CL1/8100-rc2-MQB-GBT-CL1/otp_scripts/serial_num_list"
    with shelve.open(db) as serial_num_db:
        serial_num = str(serial_num_db[max(list(serial_num_db))])

    status_of_SWDL = False
    print("*" * 70 + "\n" + "%35s%14s\n" % ('The current serial num:', serial_num) + "*" * 70 + "\n")
    # serial_num  = input("Please input the serial num:")
    with open(serial_num.strip() + ".txt", 'a') as my_log_file:
        # os.system("sudo ./boardupdater /dev/ttyUSB0 |tee -a " + create_a_serialNum() + ".txt")
        p1 = pexpect.spawn("sudo ./boardupdater /dev/ttyUSB0", timeout=None, logfile=my_log_file, encoding="utf-8")
        response = p1.expect(["password for jpcc", "Serialnumber"], timeout=5)
        if response == 0:
            p1.sendline("jpcc")
            print(greenFont("=" * 70 + '\n' + "{:>37s}".format("Log in!!!\n") + "=" * 70 + '\n'))
        elif response == 1:
            # p1.sendline("8")
            pass
        p1.expect("Please select the update:")
        p1.sendline("8")
        result = p1.expect(["system should run now", "Please select the update"], timeout=None)
        if result == 0:
            status_of_SWDL = True
            print("======================================================================\n" +
                  "{:>43s}".format("SWDL is finished\n") +
                  "======================================================================\n")
        elif result == 1:
            if not status_of_SWDL:
                print("======================================================================\n" +
                      "{:>42s}".format("SWDL is Failed!!!\n") +
                      "======================================================================\n")
                p1.sendline("q")
                # p1.close()
            else:
                p1.sendline("q")
                # p1.close()
        p1.expect("Please select the update", timeout=None)
        p1.sendline("q")
        exit_status = p1.expect(["Please select the update", "Cleanup"], timeout=None)
        if exit_status == 0:
            p1.sendline("q")
            # p1.close()
        elif exit_status == 1:
            print("=" * 70 + '\n' + "{:>37s}".format("Exit!!!\n") + "=" * 70 + '\n')
            # p1.close()
    print("Point is here!!!")
