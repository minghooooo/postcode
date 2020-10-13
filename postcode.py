import requests
import re

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

def parse_homepage(html):
    pattern = re.compile('<a.*?dropdown.*?href="#">(.*?)<span.*?caret',re.S)
    postcodes = re.findall(pattern,html)
    for pc in postcodes:
        print(pc)


if __name__ == "__main__":
    url = 'https://www.nowmsg.com/'
    html = getHTMl(url)
    # print(html)
    write_to_file(html)
    parse_homepage(html)