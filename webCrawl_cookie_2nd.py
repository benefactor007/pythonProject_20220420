import re

import requests
import json

from bs4 import BeautifulSoup

def fetch_the_sw_list(website:str) -> list:
    import requests
    import json
    from bs4 import BeautifulSoup
    session = requests.session()
    data = {
        "os_username": "wu_j7",
        "os_password": "Tianyuan==xu",
        "login": "Log+in",
        "os_destination": ""
    }
    dic_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    url_svn = website
    if url_svn.endswith(".tgz") is True:
        # print(url_svn[:url_svn.rindex('/')])
        url_svn = url_svn[:url_svn.rindex('/')]
    resp = requests.get(url=url_svn)
    soup = BeautifulSoup(resp.text, 'lxml')
    sw_list = []
    for link in soup.find_all('a'):
        # if not link.get('href').startswith(('?', "/","UpdateContainer","main")):
        link_href = link.get('href')
        if link_href.startswith(("CNS3",'sha1sum','md5sum')) is True:
            print(link_href)
            if link_href:
                sw_list.append(url_svn + '/' + link_href)
    # print(sw_list)
    sw_filter_list = [i for i in sw_list if i.endswith("symbols.tgz") is not True ]
    resp.close()
    return sw_filter_list


if __name__ == '__main__':
    url_svn = input("Please input the SVN address:")
    svn_sw_list = fetch_the_sw_list(url_svn)
    # for i in svn_sw_list:
    #     if i.endswith("-symbols.tgz") is True:
    #         svn_sw_list.remove(i)
    print(svn_sw_list)




# if __name__ == '__main__':
#     # conversation
#     session = requests.session()
#     data = {
#             "os_username": "wu_j7",
#             "os_password": "Tianyuan==xu",
#             "login": "Log+in",
#             "os_destination": ""
#     }
#     dic_headers = {
#             # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#             # "Accept-Encoding": "gzip, deflate",
#             # "Accept-Language": "en-US,en;q=0.5",
#             # "Connection": "keep-alive",
#             # "Content-Length": "75",
#             # "Content-Type": "application/x-www-form-urlencoded",
#             # "Host": "cnninvmcnflnc01:8090",
#             # "Origin": "http://cnninvmcnflnc01:8090",
#             # "Referer": "http://cnninvmcnflnc01:8090/login.action?logout=true",
#             # "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
#     }
#
#     # ajs-remote-user
#     print(data)
#     # url_login = ""
#     # session.post(url=url_login, data=data, headers=dic_headers)
#     # url_SWRTPL = "http://cnninvmcnflnc01:8090/pages/viewpage.action"
#
#     url_svn = input("Please input the SVN address:")
#     # url_svn= "http://cnninvmlgcldc01:82/37w-c-sample/linux/signature_release/20220118.1_3110-rc5-37W/VW_TW_sec/CNS3.0_37W-VW_TW_sec-0311_RC5-MAIN-20220118.1-REL.tgz"
#     if url_svn.endswith(".tgz") is True:
#         # print(url_svn[:url_svn.rindex('/')])
#         url_svn = url_svn[:url_svn.rindex('/')]
#     """
#         Ref. as below:
#         http://cnninvmlgcldc01:82/37w-c-sample/linux/signature_release/20201127.2_9200-rc2-37W/zr3-navimap-TW_sec/CNS3.0_37W-zr3-navimap-TW_sec-0920_RC2-MAIN-20201127.2-REL.tgz
#         http://cnninvmlgcldc01:82/37w-c-sample/linux/signature_release/20220118.1_3110-rc5-37W/VW_TW_sec/CNS3.0_37W-VW_TW_sec-0311_RC5-MAIN-20220118.1-REL.tgz
#     """
#     resp = requests.get(url=url_svn)
#     soup = BeautifulSoup(resp.text, 'lxml')
#     sw_list = []
#     for link in soup.find_all('a'):
#         # if not link.get('href').startswith(('?', "/","UpdateContainer","main")):
#         link_href = link.get('href')
#         if link_href.startswith(("CNS3",'sha1sum','md5sum')) is True:
#             print(link_href)
#             if link_href:
#                 sw_list.append(url_svn + '/' + link_href)
#     # print(sw_list)
#     for i in sw_list:
#         print(i)
#
#     resp.close()

