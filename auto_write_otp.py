#!/usr/bin/env python3.5

import shelve

otp_status = False

def greenFont(str):
    return "\033[32m" + str + "\033[0m"


def redFont(str):
    return "\033[31m" + str + "\033[0m"


class AttrDisplay:
    """
    Provides an inheritable(inˈherədəb(ə)l) display overload method that shows instance with their class
    names and a name=value pair for each attribute stored on the instance itself (but not attrs inherited from its
    class). Can be mixed into any class, and will work on any instance
    """

    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('%s=%+3s' % (key, getattr(self, key)))
        return ', '.join(attrs)

    def __repr__(self):
        return '[%s: %s]' % (self.__class__.__name__, self.gatherAttrs())


def auto_fill_zero(count_num: str) -> str:
    """

    :param count: input str
    :return: str which format as "0001"
    """
    if len(count_num) == 4:
        return count_num
    else:
        count_num = "0" + count_num
        return auto_fill_zero(count_num)


class serialNum(AttrDisplay):
    def __init__(self, year, month, day, model='B', count='1'):
        self.year = year
        self.month = month
        self.day = day
        self.model = model
        self.count = count

    def __repr__(self):
        return self.year + self.month + self.day + self.model + auto_fill_zero(str(self.count))


def get_current_date():
    """

    :return: (str(year),str(month),str(day))
    """
    from time import localtime
    year = str(localtime().tm_year)
    if len(str(localtime().tm_mon)) == 1:
        month = "0" + str(localtime().tm_mon)
    else:
        month = str(localtime().tm_mon)
    if len(str(localtime().tm_mday)) == 1:
        day = "0" + str(localtime().tm_mday)
    else:
        day = str(localtime().tm_mday)

    # return year+month+day
    return (year, month, day)


def get_count_from_db(db = 'serial_num_list'):
    """

    :param db:
    :return: int
    """
    with shelve.open(db) as serial_num_db:
        a = serial_num_db.keys()
        return int(max(list(a)))


def get_db_info(db = 'serial_num_list'):
    with shelve.open('serial_num_list') as serial_num_db:
        print("The size of db is", len(serial_num_db))
        for key in serial_num_db:
            print('%-3s=> %s' % (key, serial_num_db[key]))


def save_to_db(head_unit:str, db = 'serial_num_list'):
    """

    :param head_unit: give instance's name
    :param db: give shelve.file's name
    :return: show db's internal info.
    """
    with shelve.open(db) as serial_num_db:
        serial_num_db[head_unit.count] = head_unit
        print(greenFont("Save %s to %s successfully!!" % (head_unit,db)))





def main():
    date = get_current_date()
    test1 = serialNum(date[0], date[1], date[2])
    # test1 = serialNum(date[0], date[1], date[2], count='2')
    with shelve.open('serial_num_list') as serial_num_db:
        serial_num_db[test1.count] = test1




def main2():
    with shelve.open('serial_num_list') as serial_num_db:
        print(len(serial_num_db))
        for key in serial_num_db:
            # print('%-3s=>%s' % (key, db[key]))
            print("%-s=>%s" % (key, serial_num_db[key]))
        a = serial_num_db.keys()
        print(list(a))



def otp_pexpect(head_unit:str):
    """
    Do pexpect process
    :return:
    """
    global otp_status
    # otp_status = False
    import pexpect,sys
    # sudo. /MQB_VW_CHN_Banma.sh 20220420B0001
    with open(head_unit,'a')as my_log_file:
        p1 = pexpect.spawn("sudo ./MQB_VW_CHN_Banma.sh " + str(head_unit), timeout=None, logfile=my_log_file, encoding="utf-8")
    # p1 = pexpect.spawn("sudo ./MQB_VW_CHN_Banma.sh " + str(head_unit), timeout=None,encoding="utf-8")
        response = p1.expect(["password for jpcc", "This can be only done ONCE"], timeout=5)
        if response == 0:
            p1.sendline("jpcc")
        elif response == 1:
            pass
        p1.expect("HW version: 18")
        print("=>"+"HW version: 18")
        p1.expect("HW variant: 65590")
        print("=>"+"HW variant: 65590")
        p1.expect("System variant: 304001")
        print("=>"+"System variant: 304001")
        p1.expect("PCB serial number: " + str(head_unit))
        print("=>"+"PCB serial number: " + str(head_unit))
        p1.expect("Is this correct")
        p1.sendline("yes")
        result = p1.expect(["otp cell [2] written",'error'], timeout = None)
        if result == 0:
            otp_status = True
            print("="*70+"\n" +"{:>43s}".format("OTP is finished\n") + "="*70+"\n")
            # p1.close()
        elif result == 1:
            print("?" * 70 + "\n" + "{:>37s}".format("Error\n") + "?" * 70 + "\n")
            # p1.close()
    print("Point is here!!!")


def delete_hu_in_db(count:str, db = 'serial_num_list'):
    with shelve.open(db) as serial_num_db:
        if count in serial_num_db.keys():
            del serial_num_db[count]
            print(greenFont(count + " is deleted now!!!!"))
        else:
            print(redFont(count + " is not found, cannot be deleted!!!!"))
            # greenFont("Save %s to %s successfully!!" % (head_unit, db))


def test_value():   # Change global in module
    global otp_status
    otp_status = True

def get_latest_db_item(db = 'serial_num_list' ):
    with shelve.open(db) as serial_num_db:
        latest = serial_num_db[max(list(serial_num_db.keys()))]
    return latest

if __name__ == '__main__':
    # print(get_current_date())
    # main()
    # main2()
    print("Max count:", str(get_count_from_db()))
    print("type(Max count):", type(get_count_from_db()))
    get_db_info()
    date = get_current_date()
    newHU = serialNum(date[0],date[1],date[2],count= str(get_count_from_db() + 1 ))
    print(str(newHU))
    # print(get_latest_db_item())
    # save_to_db(newHU)

    # delete_hu_in_db('3')
    # get_db_info()

    # main3("20220420B0002")

    # otp_pexpect(str(newHU))
    # if otp_status:
    #     save_to_db(newHU)
    # else:
    #     print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('otp_status:',otp_status) + "?" * 70 + "\n"))

    # save_to_db(newHU)