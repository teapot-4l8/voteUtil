import requests
import time
import random
import hashlib
import json
import datetime


headers = {
    'Host': 'www.annikj.com',
    'xweb_xhr': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b)XWEB/11065',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://servicewechat.com/wx240722134f6877b1/61/page-frame.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
}

def encrypt_param_new(e, n):
    t = list(e.keys())
    t.sort()
    a = ""
    for u in t:
        a += u + "=" + str(e[u]) + "&"
    if n:
        a += "key=" + n
    return hashlib.md5(a.encode()).hexdigest()


def encrypt_param(e):
    t = list(e.keys())
    t.sort()
    a = ""
    for u in t:
        a += u + "=" + str(e[u]) + "&"
    a += "key=" + "www.annikj.cn/vote/SECRET_KEY"
    return hashlib.md5(a.encode()).hexdigest()



def go_vote(userId, uk):
    anniTime = int(time.time() * 1000)
    random_str = int(1e9 * random.random())

    data = {
        'pId': '15656',  # 选手信息
        'userId': userId,  # 用户id 和uk相关联 必须对应上
        'isQQ': 'false',  # 固定的
        'aFrom': '5',  # 固定的
        'anniTime': str(anniTime),
        'randomStr': random_str,
    }

    headers["annikey"] = encrypt_param(data)
    headers["sk"] =  encrypt_param_new(data, uk)

    response = requests.post('https://www.annikj.com/vote/elect/goVote.do', headers=headers, data=data)
    print(response.text)
    resp = json.loads(response.text)
    code = resp['code']
    if code != 0:
        raise Exception("接口返回异常，请更新代码") 


def get_session_key():  
    data = {
        'code': '0b3wPuFa1nyiWH0cCtIa1x3oEg4wPuFV',
        'scene': '1001',
        'isQQ': 'false',
        'anniTime': str(int(time.time() * 1000)),
        'randomStr': int(1e9 * random.random()),
    }
    response = requests.post('https://www.annikj.com/vote/user/getSessionKey.do', headers=headers, data=data)
    # print(response.text)
    response_data = json.loads(response.text)
    f = open("用户记录.json", mode="a+", encoding="utf-8")
    json.dump(response_data, f)
    f.write('\n')
    f.close()
    userId = response_data['data']['id']
    uk = response_data['data']['uk']
    print(f"创建新用户 -*-{userId}-*-")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return userId, uk

# 24073
# 24601




if "__main__" == __name__:
    for fifty_times in range(99):  # 浅刷500票
        userId, uk = get_session_key()

        # print(userId, uk)
        for i in range(1,51):  # 一个用户有50票
            print(f"已刷{i + fifty_times*50}票")
            go_vote(userId, uk)



