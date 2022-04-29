#!/usr/bin/env python3.5

import hashlib
import shelve

from main import confirm, create_serial_num, greenFont, get_current_date, get_db_info, redFont, repr_message
from auto_write_otp_v20220424 import AttrDisplay, auto_fill_zero, get_count_from_db
import hashlib
from timer3 import bestof, bestoftotal, total


class serial_to_sha256(AttrDisplay):
    def __init__(self, serial_num, serial_sha256='', sha256_slice=''):
        self.serial_num = serial_num
        self.sha256_slice = sha256_slice
        self.serial_sha256 = serial_sha256

    def to_sha256(self, encode='utf-8'):
        self.serial_sha256 = hashlib.sha256(self.serial_num.encode(encode)).hexdigest()

    def cut_sha256(self):
        self.sha256_slice = self.serial_sha256[:12]


def save_to_db(serial_num: str, db='serial_num_list'):
    """

    :param head_unit: give instance's name
    :param db: give shelve.file's name
    :return: show db's internal info.
    """
    with shelve.open(db) as serial_num_db:
        if serial_num.serial_num in serial_num_db.keys():
            pass
            # print(redFont(repr_message('duplicate')))
        else:
            serial_num_db[serial_num.serial_num] = serial_num
            # print(greenFont("Save %s to %s successfully!!" % (serial_num.serial_num, db)))


def fill_up_oh(arg: list):
    new_list = []
    str_list = [str(i) for i in arg]
    for i in str_list:
        while (len(i) != 4):
            i = '0' + i
        new_list.append(i)
    return new_list


def test_case():
    test_case_size = list(range(10000))
    new_list = []
    for i in fill_up_oh(test_case_size):
        i = "20220429S15" + i
        new_list.append(i)
    for i in new_list:
        instance = serial_to_sha256(i)
        instance.to_sha256()
        instance.cut_sha256()
        save_to_db(instance, db='testdb')
    with shelve.open('testdb') as db:
        # print(db[max(db.keys())].sha256_slice)
        # print([key for (key,value) in db.items() if value.sha256_slice == '73ade9a0aada'])
        res = [key for (key, value) in db.items() if value.sha256_slice == '73ade9a0aada']
        # print(db[res[0]])
        # return db[res[0]]


def get_db_keys(db):
    with shelve.open(db) as temp_db:
        keys_list = temp_db.keys()
        return max(temp_db.keys())


def create_serial_num(local_db: str = 'serial_list', model_v: str = 's15'):
    """
    create a serial num depend on local shelve db
    """
    print("get_db_info(db=local_db):", get_db_info(db=local_db))
    date = get_current_date()
    if get_db_info(db=local_db) == 0:
        newHU = serial_to_sha256(serial_num=date[0] + date[1] + date[2] + model_v + auto_fill_zero(str('1')))
        newHU.to_sha256()
        newHU.cut_sha256()
        print(repr_message(str(newHU.serial_num) + ": " + str(newHU.sha256_slice)))
        return confirm(save_to_db, newHU, db=local_db)
    else:
        count = get_db_keys(db=local_db)[-4:]
        newHU = serial_to_sha256(
            serial_num=date[0] + date[1] + date[2] + model_v + auto_fill_zero(str(int(count) + 1)))
        newHU.to_sha256()
        newHU.cut_sha256()
        print(repr_message(str(newHU.serial_num) + ": " + str(newHU.sha256_slice)))
        return confirm(save_to_db, newHU, db=local_db)
    # get_db_info(db=local_db)


if __name__ == '__main__':
    # with shelve.open("serial_db") as db:
    #     print(db.pop('202204290001','Not found'))
    create_serial_num(local_db='serial_db', model_v='s15')
    get_db_info(db='serial_db')
    with shelve.open("serial_db") as db:
        print(db[get_db_keys(db='serial_db')].sha256_slice)
    # test_case()
    # print(total(test_case,_reps=10)[0])
    # (best, ret) = bestoftotal(fill_up_oh, list(range(10000)), _reps1=5, _reps=1000)
    # print('%-9s:%.5f => [%s...%s]' % (fill_up_oh.__name__, best, ret[0], ret[-1]))
