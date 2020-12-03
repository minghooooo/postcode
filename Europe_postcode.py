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


#测试链接使用的函数
def Code_getHTMl(url):
    ht = "10.34.7.141"
    pt = 3306
    pw = "123456"
    db = "ip_proxy"
    us = "crawl"
    pr = get_proxy.get_proxy(ht,pt,pw,db,us) 
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    proxies = {'http': "http://"+pr} 
    resp = requests.get(url,headers = headers,proxies=proxies,timeout = 10)
    if resp.status_code != 200:
        resp.encoding = 'UTF-8'
        write_to_file(resp.text)
        print(resp.status_code)
    print(200)

def parse_state(html,proxies):
    soup0 = BeautifulSoup(html,'lxml')
    countries = soup0.find_all(name = 'div',attrs = {'class':'col-xs-12'})#所有欧洲国家的集合
    countries = countries[3]
    countries = str(countries)
    pattern0 = re.compile('<a.*?href="(.*?)".*?>(.*?)</a',re.S)
    country = re.findall(pattern0,countries) #获取到具体国家的href和名称
    ht = "10.34.7.141"
    pt = 3306
    pw = "123456"
    db = "ip_proxy"
    us = "crawl"
    # print(country)
    for c in country:
        pr = get_proxy.get_proxy(ht,pt,pw,db,us) 
        proxies = {'http': "http://"+pr} 
        country_page = getHTMl(c[0],proxies)
        Code_getHTMl(c[0])
        soup1 = BeautifulSoup(country_page,'lxml')
        county = soup1.find_all(name = 'div',attrs = {'class':'col-md-3 col-xs-6 my-padding-6'})#国家分类的主要行政区
        # print(county)
        county = str(county)
        pattern1 = re.compile('<a.*?href="(.*?)".*?>(.*?)</a',re.S)
        city = re.findall(pattern1,county) #获取到具体国家的href和名称
        for ic in city:
            Code_getHTMl(c[0]+ic[0])
            
        # print(c)
    # country_page = getHTMl(country[0],proxies)
    # print(country[0])
    # soup1 = BeautifulSoup(country_page,'lxml')
    # county = soup1.find_all(name = 'div',attrs = {'class':'col-md-3 col-xs-6 my-padding-6'})#国家分类的主要行政区

  
    # countries = str(countries).replace('&quot;','\"').replace('\t','').replace('\n','').replace('\r','')
 


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