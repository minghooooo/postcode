import requests
import re
import os
import csv
import get_proxy
import numpy as np
from bs4 import BeautifulSoup

def getHTMl(url,proxies):
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    resp = requests.get(url,headers = headers, proxies=proxies, timeout=10)
    if resp.status_code == 200:
        resp.encoding = 'UTF-8'
        return resp.text
    return 0

#测试链接使用的函数
def Code_getHTMl(url):
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    resp = requests.get(url,headers = headers)
    if resp.status_code != 200:
        resp.encoding = 'UTF-8'
        write_to_file(resp.text)
        print(resp.status_code)


def write_to_file(content):
    with open('D:\TMH\Global_postcode\Homepage.txt','a',encoding='UTF-8') as f:
        f.write(content)

#创建文件夹函数
def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path+'succ in making new path')
        return True
    else:
        return False

def parse_state(html,proxies):
    pattern0 = re.compile('<a.*?dropdown.*?href="#">(.*?)<span.*?caret(.*?)</ul>',re.S)#state's name&whole part of the countries in it.
    states = re.findall(pattern0,html)
    states_n = np.array(states)[0:5] #translate to nparray
    state_count = 0  #计算当前是第几个大洲
    soup0 = BeautifulSoup(html,'lxml')
    uls = soup0.find_all(name = 'ul',attrs ={'class':'dropdown-menu'}) #五个洲所有的li的集合
    uls = str(uls).replace('&quot;','\"').replace('\t','').replace('\n','').replace('\r','')
    #从五个大洲的ul里分割出每一个洲的国家
    pattern1 = re.compile('<ul.*?</ul>',re.S) #可以成功分开5个大洲的ul
    uls = re.findall(pattern1,uls)
    uls = uls[0:5] #最后一个是电话号码什么的，所以去掉
    for s in states_n:
        state_count = state_count +1 
        file_path_state='D:\TMH\Global_postcode\\'+ s[0]
        # print(file_path_state)
        # print(s[0])
        mkdir(file_path_state)
        # print(uls[state_count - 1])
        ul = uls[state_count - 1] #取出第x个洲的信息
        # print('++++++++++')
        #开始创建每个国家的文件夹！
        pattern1 = re.compile('<li><a.*?href="(.*?)">(.*?)</a></li>',re.S)
        countries = re.findall(pattern1,ul)
        for country in countries:
            country_name = country[1] #获取国家名
            country_name = str(country_name).replace('邮编','').replace('查询','') #去掉多余的字
            file_path_state_country = file_path_state + '\\' + country_name #创建国家相对应的文件夹
            mkdir(file_path_state_country)
            #测试链接情况
            Code_getHTMl(country[0])
            # print(country[0])
            #打开第x个国家的网站
            country_page = getHTMl(country[0],proxies)
            #分析要提取的网页的重要内容
            soup1 = BeautifulSoup(country_page,'lxml')
            divs = soup1.find_all(name = 'div',attrs ={'class':'row col-sm-12'}) #对应网页中的主要地区
            divs = str(divs).replace('&quot;','\"').replace('\t','').replace('\n','').replace('\r','') #去掉奇怪的字符
            #用正则取出第一个
            pattern2 = re.compile('<div.*?</div>')
            divs = re.findall(pattern2,divs)
            print('=====================')
            print(divs)
            print('=====================')
            for div in divs:
                soup3 = BeautifulSoup(div,'lxml')
                # county_url = soup3.find_all()
                # print(county_url)

        # os.startfile(file_path_state) #模拟打开文件夹操作
        



        #open the file of one state
        #into the file
        #use a method to new a file of one of the country in the state




  
    

if __name__ == "__main__":
    ht = "10.34.7.141"
    pt = 3306
    pw = "123456"
    db = "ip_proxy"
    us = "crawl"
    pr = get_proxy.get_proxy(ht,pt,pw,db,us) 
    proxies = {'http': "http://"+pr} 
    url = 'https://www.nowmsg.com/'
    html = getHTMl(url,proxies)
    parse_state(html,proxies)



    # state's name :<a.*?dropdown.*?href="#">(.*?)<span.*?caret
    # countries :<li><a.*?href="(.*?)">(.*?)</a></li>
    # state's name & the info of countries :<a.*?dropdown.*?href="#">(.*?)<span.*?caret(.*?)</ul>