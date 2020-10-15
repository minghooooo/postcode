import requests
import re
import numpy as np
#try to into province 1


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
    with open('D:\TMH\g_postcode\detail.txt','a',encoding='UTF-8') as f:
        f.write(content)



def parse_state(html):
    patten5 = re.compile('<td >(.*?)</td>',re.S)
    details = re.findall(patten5,html)[0:7]
    print(type(details))
    print(len(details))
    print(details)



if __name__ == "__main__":
    url = 'https://www.nowmsg.com/findzip/postal_code.asp?country=DE&state=Baden-W%C3%BCrttemberg&county=Freiburg%20Region&city=Aach'
    html = getHTMl(url)
    # print(html)
    write_to_file(html)
    parse_state(html)