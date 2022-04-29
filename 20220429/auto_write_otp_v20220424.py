#!/usr/bin/env python3.5
import os
import shelve
import time

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


def get_count_from_db(db='serial_num_list'):
    """

    :param db:
    :return: int
    """
    with shelve.open(db) as serial_num_db:
        a = serial_num_db.keys()
        # print(list(a))
        # convert list(str) to list(int)
        list_int = list(map(int, list(a)))
        return max(list_int)


def get_db_info(db='serial_num_list'):
    with shelve.open(db) as serial_num_db:
        # print("The size of db is", len(serial_num_db))
        for key in serial_num_db:
            print('%-3s=> %s' % (key, serial_num_db[key]))
        return len(serial_num_db)

def get_newest_value(db='serial_num_list'):
    with shelve.open(db) as serial_num_db:
        return serial_num_db[str(get_count_from_db(db))]

def get_db_value(key, db = 'serial_num_list'):
    with shelve.open(db) as serial_num_db:
        return serial_num_db[str(key)]

def save_to_db(head_unit: str, db='serial_num_list'):
    """

    :param head_unit: give instance's name
    :param db: give shelve.file's name
    :return: show db's internal info.
    """
    with shelve.open(db) as serial_num_db:
        serial_num_db[head_unit.count] = head_unit
        print(greenFont("Save %s to %s successfully!!" % (head_unit, db)))


def main():
    date = get_current_date()
    test1 = serialNum(date[0], date[1], date[2])
    # test1 = serialNum(date[0], date[1], date[2], count='2')
    with shelve.open('otp_scripts/serial_num_list') as serial_num_db:
        serial_num_db[test1.count] = test1


def main2():
    with shelve.open('otp_scripts/serial_num_list') as serial_num_db:
        print(len(serial_num_db))
        for key in serial_num_db:
            # print('%-3s=>%s' % (key, db[key]))
            print("%-s=>%s" % (key, serial_num_db[key]))
        a = serial_num_db.keys()
        print(list(a))


def repr_message(message: str):
    padding_len = '%' + str(int(len(message) / 2) + 35) + 's'
    return "=" * 70 + "\n" + padding_len % message + "\n" + "=" * 70 + "\n"


def check_dir(*args):
    dir_name = args[0]
    file_name = args[1]
    if os.path.exists(dir_name):
        txt_file_name = dir_name + "/" + file_name + '.txt'
        try:
            with open(txt_file_name, 'a') as record_file:
                record_file.write(repr_message(time.asctime()))
            # time.sleep(5)
            # assert os.path.isfile(file_name), '\n' + redFont(repr_message(file_name + ' is not a existing file'))
            assert os.path.isfile(txt_file_name)
            # print(greenFont(repr_message("We are here")))
            return True
        except AssertionError:
            print(redFont(repr_message(txt_file_name + ' is not an existing file, ' + 'Position: check_dir')))
        except Exception as e:
            raise e
    else:
        # print(redFont(repr_message(dir_name + ' is not an existing path')))
        return False


def otp_pexpect(head_unit: str):
    """
    Do pexpect process
    :return:
    """
    global otp_status
    import pexpect, sys
    # sudo. /MQB_VW_CHN_Banma.sh 20220420B0001
    dir_path = 'record_data'
    if check_dir(dir_path, head_unit):
        with open(dir_path + '/' + head_unit + ".txt", 'a')as my_log_file:
            my_log_file.write(repr_message(time.asctime()))
            print(repr_message(time.asctime()))
            # my_log_file = '' if record_file == '' else sys.stdout
            p1 = pexpect.spawn("sudo ./MQB_VW_CHN_Banma.sh " + str(head_unit), timeout=None, logfile=my_log_file,
                               encoding="utf-8")
            # logfile = sys.stdout
            # logfile = my_log_file
            response = p1.expect(["password for jpcc", "This can be only done ONCE"], timeout=10)
            if response == 0:
                p1.sendline("jpcc")
            elif response == 1:
                pass
            # base_info = p1.expect(
            #     ["HW version: 100000", "HW variant: 65590", "System variant: 304001", "PCB serial number: " + str(head_unit),
            #      pexpect.TIMEOUT], timeout=10)
            # if base_info == 4:
            #     print(redFont(repr_message("There is no matched base_info")))
            issue_info = ''
            try:
                issue_info = "HW version"
                p1.expect("HW version: 18",timeout=5)
                # print("=>"+"HW version: 18")
                issue_info = 'HW variant'
                p1.expect("HW variant: 65590",timeout=5)
                # print("=>"+"HW variant: 65590")
                issue_info = 'System variant'
                p1.expect("System variant: 304001",timeout=5)
                # print("=>"+"System variant: 304001")
                issue_info = "PCB serial number"
                p1.expect("PCB serial number: " + str(head_unit),timeout=5)
                # print("=>"+"PCB serial number: " + str(head_unit))
            except pexpect.TIMEOUT:
                raise pexpect.TIMEOUT('\n' + repr_message("There is no matched base_info of " + issue_info))
                # p1.expect("Is this correct")
                # p1.sendline("no")
                # print(redFont('\n' + repr_message("There is no matched base_info of " + issue_info)))
            p1.expect("Is this correct")
            p1.sendline("yes")
            try:
                # p1.expect('otp cell \[1\]')
                # Have to add '\' (backslash) before '[' or ']'(bracket)
                p1.expect("otp cell \[2\] written", timeout=60)
                print(greenFont(repr_message("OTP has written done")))
                otp_status = True
                return otp_status
            except pexpect.EOF:
                print(redFont(repr_message("pexpect.EOF Error")))
                # print("We are here, Position 3")
                return otp_status
            except pexpect.TIMEOUT:
                print(redFont(repr_message("pexpect.TIMEOUT Error")))
                # print("We are here, Position 3")
                # p1.close()
                # pexpect.EOF
                return otp_status
    else:
        print(redFont(repr_message("record directory path is not found")))


def delete_hu_in_db(count: str, db='serial_num_list'):
    with shelve.open(db) as serial_num_db:
        if count in serial_num_db.keys():
            del serial_num_db[count]
            print(greenFont(count + " is deleted now!!!!"))
        else:
            print(redFont(count + " is not found, cannot be deleted!!!!"))
            # greenFont("Save %s to %s successfully!!" % (head_unit, db))


def test_value():  # Change global in module
    global otp_status
    otp_status = True


def get_latest_db_item(db='serial_num_list'):
    with shelve.open(db) as serial_num_db:
        latest = serial_num_db[max(list(serial_num_db.keys()))]
    return latest


if __name__ == '__main__':
    # print(get_current_date())
    # main()
    # main2()
    print(greenFont(repr_message("The newest db[value] is " + str(get_newest_value()))))
    print("Max count:", str(get_count_from_db()))
    print("type(Max count):", type(get_count_from_db()))
    get_db_info()
    date = get_current_date()
    print('str(get_count_from_db() + 1):', str(get_count_from_db() + 1))
    newHU = serialNum(date[0], date[1], date[2], count=str(get_count_from_db() + 1))
    # newHU = serialNum(date[0],date[1],day='22',count='7')
    # save_to_db(newHU)
    # print(str(newHU))
    print(greenFont(repr_message("Serial Num: " + str(newHU))))
    # save_to_db(newHU)
    # otp_pexpect(str(newHU))
    # delete_hu_in_db('0008')

    res = input(repr_message("Input \" correct \" to continue"))
    # res = 'correct'                             # test-only
    if res.lower() == 'correct':
        if otp_pexpect(str(newHU)):
            print(greenFont(repr_message(str(otp_status))))
            save_to_db(newHU)
            get_db_info()
        else:
            print(redFont(repr_message('otp status: ' + str(otp_status))))
    else:
        pass