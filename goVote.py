import requests
import time
import random


def generate_sk():
    pass

def generate_annikey():
    pass


headers = {
    'Host': 'www.annikj.com',
    'xweb_xhr': '1',
    'annikey': 'e5b7b66f4dd473c326eef45d7f074737',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b)XWEB/11065',
    'sk': '5d3f1cf62cd0fbd6971f7406d620d496',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://servicewechat.com/wx240722134f6877b1/61/page-frame.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
}

anniTime = int(time.time() * 1000)


random_str = int(1e9 * random.random())

data = {
    'pId': '16221',  # 选手信息
    'userId': '3360485',  # 用户id
    'isQQ': 'false',  # 固定的
    'aFrom': '5',  # 固定的
    'anniTime': str(anniTime),
    'randomStr': random_str,
}
# 355733341
# 957235152
# 408663330
proxy = {
    "http": 'http://127.0.0.1:8889',
    "https": 'http://127.0.0.1:8889',
}

response = requests.post('https://www.annikj.com/vote/elect/goVote.do', headers=headers, data=data)
print(response.text)


# 1722759447056
# 1722759627.5271835


