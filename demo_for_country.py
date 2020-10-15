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

def parse_state(html):
    pattern2 = re.compile('<div.*?col-md-3 my-padding-6.*?href="(.*?)">(.*?)</a>',re.S)
    areas = re.findall(pattern2,html)
    for a in areas:
        print(a)



if __name__ == "__main__":
    url = 'https://www.nowmsg.com/findzip/de_postalcode.asp'
    html = getHTMl(url)
    # print(html)
    # write_to_file(html)
    parse_state(html)