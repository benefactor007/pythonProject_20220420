#!/usr/bin/env/python3.5
import binascii
import sys,pexpect,shelve

write_status = False

def greenFont(str):
    return "\033[32m" + str + "\033[0m"


def redFont(str):
    return "\033[31m" + str + "\033[0m"

def get_serial_num(db:str = None):
    db = "/home/jpcc/Documents/MQB_CL1/8100-rc2-MQB-GBT-CL1/otp_scripts/serial_num_list"
    with shelve.open(db) as serial_num_db:
        serial_num = str(serial_num_db[max(list(serial_num_db))])
    return serial_num

def str_to_hexStr(str_info):
    return binascii.hexlify(str_info.encode('utf-8')).decode('utf-8')


# /home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.InitPersistence
# /home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.SetKey
def copy_file_to_HU(file_path:str):
    ip = '192.168.1.4'
    dest_path = ' root@192.168.1.4:/tmp/'
    # os.system('scp' + file_path + dest_path )
    p = pexpect.spawn("scp " + file_path + dest_path, timeout=60, logfile=sys.stdout, encoding='utf-8')
    p.expect("password")
    p.sendline("root")
    p.expect("100%")
    print(greenFont("*" * 70 + "\n" + "%35s\n" % ('copy file to HU') + "*" * 70 + "\n"))



def do_pexpect(**kwargs):
    ip = "192.168.1.4"
    global write_status
    assert 'serial_num' in kwargs, redFont("\n"+"?" * 70 + "\n" + "%35s%s\n" % ('serial_num' , ' is missing') + "?" * 70 + "\n")
    log_file = kwargs['serial_num'] + "_pers" + "_log_file" + '.txt'
    with open(log_file, 'a') as my_log_file:
        p = pexpect.spawn("ssh root@" + ip, timeout=None,logfile=my_log_file, encoding='utf-8')
        # p.expect("login")
        # p.sendline("root")
        p.expect("password")
        p.sendline("root")
        p.sendline("mount-read-write.sh")
        p.sendline("chmod +x /tmp/tsd.persistence.client.mib3.app.SetKey")
        p.sendline("/tmp/tsd.persistence.client.mib3.app.SetKey --ns 0x80000008 --key 0x00  --val 0xe5")
        # If HU is brand new, have to InitPersistence script
        p.sendline("chmod +x /tmp/tsd.persistence.client.mib3.app.InitPersistence")
        p.sendline("/tmp/tsd.persistence.client.mib3.app.InitPersistence")
        # Set serial_num
        if 'serial_num'in kwargs:
            p.sendline("/tmp/tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF18C  --val 0x" + str_to_hexStr(kwargs['serial_num']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('serial_num' , ' no change') + "?" * 70 + "\n"))
        # Set Fazit-id
        if 'fazit' in kwargs:
            p.sendline("/tmp/tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF17C  --val 0x" + str_to_hexStr(kwargs['fazit']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%30s%s\n" % ('fazit' , ' no change') + "?" * 70 + "\n"))
        # Set Hardware version >> X13 (SOP1.5)/(37W_SOP1.0)
        if 'hw_version' in kwargs:
            p.sendline("/tmp/tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF1A3  --val 0x" + str_to_hexStr(kwargs['hw_version']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('hw_version' , ' no change') + "?" * 70 + "\n"))
        # Set Software version >> C420
        if 'sw_version' in kwargs:
            p.sendline("/tmp/tsd.persistence.client.mib3.app.SetKey --ns 0x3000000 --key 0xF189  --val 0x" + str_to_hexStr(kwargs['sw_version']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('sw_version' , ' no change') + "?" * 70 + "\n"))
        # Set PartNum >> 3GB035866A
        if 'part_num' in kwargs:
            # Oct   Dec   Hex   Char
            # 040   32    20    SPACE
            p.sendline("/tmp/tsd.persistence.client.mib3.app.SetKey --ns 0x03000000 --key 0xF187 --val 0x" + str_to_hexStr(kwargs['part_num']).upper())
            p.sendline("/tmp/tsd.persistence.client.mib3.app.SetKey --ns 0x03000000 --key 0xF191 --val 0x" + str_to_hexStr(kwargs['part_num']).upper())
        else:
            print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('part_num',' no change') + "?" * 70 + "\n"))
        p.sendline("sync")
        p.sendline("exit")
        p.expect("closed")
        # p.expect(pexpect.EOF)
        # print("\033[32m" + "PASS" + "\033[0m")  # print Green font
    write_status = True


if __name__ == '__main__':
    # print(get_serial_num())
    # copy_file_to_HU('/home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.InitPersistence')
    # copy_file_to_HU('/home/jpcc/Documents/modify_systeminfo/tsd.persistence.client.mib3.app.SetKey')
    do_pexpect(serial_num ="20220421B0002",sw_version="C081",hw_version="X99",part_num="3GB035866B")
    if write_status:
        print(greenFont("=" * 70 + "\n" + "%35s%s\n" % ('write_status:', write_status) + "=" * 70 + "\n"))
    else:
        print(redFont("?" * 70 + "\n" + "%35s%s\n" % ('write_status:', write_status) + "?" * 70 + "\n"))