#!/usr/bin/env/python3.5
import binascii
import sys,pexpect,shelve


from otp_scripts.auto_write_otp import serialNum
write_status = False

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

def greenFont(str):
    return "\033[32m" + str + "\033[0m"


def redFont(str):
    return "\033[31m" + str + "\033[0m"

def get_serial_num(db:str = None):

    db = "/home/jpcc/Documents/37W_CL1/7100-rc5-37W/otp_scripts/serial_num_list"
    with shelve.open(db) as serial_num_db:
        serial_num = str(serial_num_db[max(list(serial_num_db))])
    return serial_num

def str_to_hexStr(str_info):
    return binascii.hexlify(str_info.encode('utf-8')).decode('utf-8')


# /home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.InitPersistence
# /home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.SetKey
def copy_file_to_HU(file_path:str):
    ip = '192.168.1.4'
    hu_zone = "/var/tmp/"
    dest_path = ' root@192.168.1.4:' + hu_zone
    # os.system('scp' + file_path + dest_path )
    p = pexpect.spawn("scp " + file_path + dest_path, timeout=60, logfile=sys.stdout, encoding='utf-8')
    p.expect("password")
    p.sendline("root")
    p.expect("100%")
    print(greenFont("*" * 70 + "\n" + "%35s\n" % ('copy file to HU') + "*" * 70 + "\n"))


def repr_message(message:str):
    padding_len = '%' + str(int(len(message) / 2) + 35) + 's'
    return "=" * 70 + "\n" + padding_len % message + "\n" + "=" * 70 + "\n"

def do_pexpect(**kwargs):
    ip = "192.168.1.4"
    global write_status
    assert 'serial_num' in kwargs, redFont("\n"+"?" * 70 + "\n" + "%35s%s\n" % ('serial_num' , ' is missing') + "?" * 70 + "\n")
    log_file = kwargs['serial_num'] + "_pers" + "_log_file" + '.txt'
    hu_zone = "/var/tmp/"
    with open(log_file, 'a') as my_log_file:
        p = pexpect.spawn("ssh root@" + ip, timeout=None,logfile=my_log_file, encoding='utf-8')
        # p.expect("login")
        # p.sendline("root")
        p.expect("password")
        p.sendline("root")
        print(repr_message(greenFont(serialNum)))
        p.sendline("mount-read-write.sh")
        p.sendline("chmod +x " + hu_zone + "tsd.persistence.client.mib3.app.SetKey")
        p.sendline(hu_zone + "tsd.persistence.client.mib3.app.SetKey --ns 0x80000008 --key 0x00  --val 0xe5")
        # If HU is brand new, have to InitPersistence script
        p.sendline("chmod +x " + hu_zone + "tsd.persistence.client.mib3.app.InitPersistence")
        p.sendline(hu_zone + "tsd.persistence.client.mib3.app.InitPersistence")
        # Set serial_num
        if 'serial_num'in kwargs:
            p.sendline(hu_zone + "tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF18C  --val 0x" + str_to_hexStr(kwargs['serial_num']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('serial_num' , ' no change') + "?" * 70 + "\n"))
        # Set Fazit-id
        if 'fazit' in kwargs:
            p.sendline(hu_zone + "tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF17C  --val 0x" + str_to_hexStr(kwargs['fazit']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%30s%s\n" % ('fazit' , ' no change') + "?" * 70 + "\n"))
        # Set Hardware version >> X13 (SOP1.5)/(37W_SOP1.0)
        if 'hw_version' in kwargs:
            p.sendline(hu_zone + "tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF1A3  --val 0x" + str_to_hexStr(kwargs['hw_version']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('hw_version' , ' no change') + "?" * 70 + "\n"))
        # Set Software version >> C420
        if 'sw_version' in kwargs:
            p.sendline(hu_zone + "tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF189  --val 0x" + str_to_hexStr(kwargs['sw_version']).upper())
            try:
                p.expect("key: 61833 slot: 0 status: 0", timeout=5)
                print(greenFont(repr_message("Key(61833) has written")))
                write_status = True
            except pexpect.TIMEOUT:
                write_status = False
                print(redFont(repr_message("Something is going wrong")))
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('sw_version' , ' no change') + "?" * 70 + "\n"))
        # Set PartNum >> 3GB035866A
        if 'part_num' in kwargs:
            # Oct   Dec   Hex   Char
            # 040   32    20    SPACE
            p.sendline(hu_zone + "tsd.persistence.client.mib3.app.SetKey --ns 0x03000000 --key 0xF187 --val 0x" + str_to_hexStr(kwargs['part_num']).upper())
            p.sendline(hu_zone + "tsd.persistence.client.mib3.app.SetKey --ns 0x03000000 --key 0xF191 --val 0x" + str_to_hexStr(kwargs['part_num']).upper())
            try:
                p.expect("key: 61841 slot: 0 status: 0", timeout=5)
                print(greenFont(repr_message("Key(61841) has written")))
                write_status = True
            except pexpect.TIMEOUT:
                write_status = False
                print(redFont(repr_message("Something is going wrong")))
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('part_num',' no change') + "?" * 70 + "\n"))
        pexpect.EOF


        p.sendline("sync")
        p.sendline("exit")
        p.expect("closed")
        # p.expect(pexpect.EOF)
        # print("\033[32m" + "PASS" + "\033[0m")  # print Green font



if __name__ == '__main__':
    # print(get_serial_num())
    copy_file_to_HU('/home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.InitPersistence')
    copy_file_to_HU('/home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.SetKey')
    # do_pexpect(serial_num ="20220420W0002",sw_version="C071",hw_version="X30",part_num="5HG035866F")
    serialNum = "20220420B0003"
    # do_pexpect(serial_num=serialNum, sw_version="C081", hw_version="X30", part_num="3GB035866D")
    do_pexpect(serial_num = serialNum, sw_version = 'C810')
    if write_status:
        print(greenFont("=" * 70 + "\n" + "%35s%s\n" % ('write_status:', write_status) + "=" * 70 + "\n"))
    else:
        print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('write_status:', write_status) + "?" * 70 + "\n"))