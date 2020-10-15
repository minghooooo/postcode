import requests
import re
import os
import numpy as np

def getHTMl(url):
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    resp = requests.get(url,headers = headers)
    if resp.status_code == 200:
        resp.encoding = 'UTF-8'
        return resp.text
    return 0

def write_to_file(content):
    with open('D:\TMH\g_postcode\Homepage.txt','a',encoding='UTF-8') as f:
        f.write(content)


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path+'succ in making new path')
        return True
    else:
        return False

def parse_state(html):
    pattern0 = re.compile('<a.*?dropdown.*?href="#">(.*?)<span.*?caret(.*?)</ul>',re.S)#state's name&whole part of the countries in it.
    states = re.findall(pattern0,html)
    states_n = np.array(states)[0:5]#translate to narray
    # states_n =states_n[0:5,:]#keep the important info
    for s in states_n:
        file_path_state='D:\TMH\g_postcode\\'+ s[0]
        print(file_path_state)
        # print(s[0])

        #open the file of one state
        #into the file
        #use a method to new a file of one of the country in the state
    pattern1 = re.compile('<li><a.*?href="(.*?)">(.*?)</a></li>',re.S)#countries and its urls.
    states_s =str(states)#to string
    countries = re.findall(pattern1,states_s)
    countries_n = np.array(countries)[:-9]
    # countries_n = np.delete(countries_n,[:-8],axis=0)#?
    for c in countries_n:
        print(c)
    # for s in states:
    #     yeild{
    #         'state_name':s[0],
    #         'country_url':s[1]
    #     }
    

if __name__ == "__main__":
    url = 'https://www.nowmsg.com/'
    html = getHTMl(url)
    # print(html)
    # write_to_file(html)
    parse_state(html)



    # state's name :<a.*?dropdown.*?href="#">(.*?)<span.*?caret
    # countries :<li><a.*?href="(.*?)">(.*?)</a></li>
    # state's name & the info of countries :<a.*?dropdown.*?href="#">(.*?)<span.*?caret(.*?)</ul>