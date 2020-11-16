import pymysql
import re
import subprocess as sp
import threading
import time
import pandas as pd
import requests
from fake_useragent import UserAgent
import os
import random

# 创建文件夹
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' create succss')
        return True
    else:
        return False

# 写入网页的源码
def write_html(path, html):
    (paths, filename) = os.path.split(path)
    with open(path, 'wb') as f:
        f.write(html)
    f.close()

# 从数据库获取ip列表
def post_sql(ht,pt,pw,db,us):
    # try:
    con = pymysql.connect(host=ht,port=pt,user=us,passwd=pw,database=db,charset="utf8") # 连接数据库
    cursor = con.cursor()
    sql = "select ip from proxy where 'check'=0 order by 'time' desc ;" # 查询语句
    cursor.execute(sql)
    results = cursor.fetchall() # 获取所有结果
    cursor.close()
    con.close()
    # print("ips : ",len(results)) # 获取到的ip的数量
    # result_l =  list(results)
    # print(result_l)
    # results_s = random.shuffle(result_l)
    # print(results_s)
    return results
    # except:
    #     print("error")
    #     return []

def initpattern():
#匹配丢包数
    lose_time = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
#匹配平均时间
    waste_time = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
    return lose_time, waste_time

# 第一种检测ip的可用性，直接ping去访问ip
def check_ip_1(ip, lose_time, waste_time):
    # print("check : ",ip)
#命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd = "ping -n 3 -w 3 %s"
    # print(cmd)
    #执行命令
    p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    # print(ip)
    #获得返回结果并解码
    out = p.stdout.read().decode("gbk")
    # print(out)
    average = waste_time.findall(out)#平均时间
    # print(average)
    #丢包数
    lose_time = lose_time.findall(out)
    # print(lose_time)
    #当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
    if len(lose_time) == 0:
        lose = 3
    else:
        lose = int(lose_time[0])
    # print(lose)
#如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
    if lose > 2:
        #返回False
        # print(ip," unable")
        return 1000
#如果丢包数目小于等于2个,获取平均耗时的时间
    else:
#当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
        if len(average) == 0:
            # print(ip," unable")
            return 1000
        else:
            average_time = int(average[0])
            # print(ip," able")
#返回平均耗时
            return average_time

# 第二种检测ip可用性，使用访问网站的方式
def check_ip_2(proxies):
    proxies.pop('https')
    # print('proxies')
    # print(proxies)
    headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}
    url = "https://www.baidu.com"

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=5)  # 使用代理来访问百度，测试ip代理可用性
        if response.status_code == 200:
            return 1
        else:
            return 0 
    except:
        print('连接超时')
        return 0


# 获取代理
def get_proxy(ht,pt,pw,db,us,use=1):
    # print("get proxy")
    while(1):
        ips = post_sql(ht,pt,pw,db,us)
        for n in range(200): # 随机抽取200次，200次后还是没有可用的ip，直接重新获取代理池
            i = random.choice(ips) # 随机抽取 ip
            # for i in ips:
            proxies = {'http': "http://"+i[0]} # , 'https': "https://"+i[0]
            ip = i[0].split(":")[0]
            lose_time, waste_time = initpattern()
            if(use == 1):
                average_time = check_ip_1(ip, lose_time, waste_time)
                if average_time < 60: 
                    # print(proxies," ok")
                    return i[0]
            else:
                num = check_ip_2(proxies)
                if(num==1):
                    # print(proxies," ok")
                    return i[0]

# test 代码
# ht = "10.34.7.141"
# pt = 3306
# pw = "123456"
# db = "ip_proxy"
# us = "crawl"
# pr = get_proxy(ht,pt,pw,db,us,use=1)
# proxies = {'http': "http://"+pr}
# num = check_ip_2(proxies)
# print(num)



# Using Example !!!
# # 使用代理包的代码
# import get_proxy
# #数据库连接的ip和密码
# ht = "10.34.7.141"
# pt = 3306
# pw = "123456"
# db = "ip_proxy"
# us = "crawl"
# pr = get_proxy.get_proxy(ht,pt,pw,db,us) # 获取代理
# proxies = {'http': "http://"+pr}
# 下面部分是自定义的爬虫
#  headers = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
# }
# url = "https://www.baidu.com"
# try:
#     response = requests.get(url, headers=headers, proxies=proxies, timeout=10)  # 使用代理来访问百度，测试ip代理可用性
#     if response.status_code == 200:
#         print("success")
#     else:
#         print("error")
# except:
#     print("requests error")

