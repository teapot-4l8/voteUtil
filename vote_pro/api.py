import requests
import random
import time
import hashlib
import json
import datetime
import string
from typing import Dict

import config

def generate_code() -> str:
    # 定义字符集：大写字母、小写字母和数字
    characters = string.ascii_letters + string.digits
    # 使用random.choices从字符集中随机选择指定数量的字符
    random_string = ''.join(random.choices(characters, k=32))
    return random_string

def encrypt_param_new(e: Dict, n: str) -> str:
    t = list(e.keys())
    t.sort()
    a = ""
    for u in t:
        a += u + "=" + str(e[u]) + "&"
    if n:
        a += "key=" + n
    return hashlib.md5(a.encode()).hexdigest()

def encrypt_param(e: Dict) -> str:
    t = list(e.keys())
    t.sort()
    a = ""
    for u in t:
        a += u + "=" + str(e[u]) + "&"
    a += "key=" + "www.annikj.cn/vote/SECRET_KEY"
    return hashlib.md5(a.encode()).hexdigest()


def go_vote(userId:int, uk:str) -> int:
    """
    发起投票请求，返回状态码

    Args:
        userId (int): 用户ID
        uk (str): UK

    Returns:
        int: 状态码
        0: 成功
        -1：投票次数达到上限
        -12: 算法错误
    """
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

    anniTime = int(time.time() * 1000)
    random_str = int(1e9 * random.random())

    data = {
        'pId': config.PID,
        'userId': userId,
        'isQQ': 'false',
        'aFrom': '5',
        'anniTime': str(anniTime),
        'randomStr': random_str,
    }
    headers["annikey"] = encrypt_param(data)
    headers["sk"] = encrypt_param_new(data, uk)

    response = requests.post('https://www.annikj.com/vote/elect/goVote.do', headers=headers, data=data)
    print(response.text)
    resp = json.loads(response.text)
    code = resp['code']
    return code


def get_session_key() -> Dict:
    """
    创建新用户并返回用户ID和UK

    Returns:
        Dict: 包含用户ID和UK的字典
        {"code": 0, "data": {"id": 3523439, "userType": 0, "uk": "5fce6c95872a37fdbfa525367f035942"}}
    """
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 wechatdevtools/1.06.2209190 MicroMessenger/8.0.5 Language/zh_CN webview/',
        'content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx6b6da4e842c89b90/devtools/page-frame.html',
    }
    data = {
        'code': generate_code(),
        'scene': '1001',
        'isQQ': 'false',
        'anniTime': str(int(time.time() * 1000)),
        'randomStr': int(1e9 * random.random()),
    }
    response = requests.post('https://www.annikj.com/vote/user/getSessionKey.do', headers=headers, data=data)
    response_data = json.loads(response.text)
    return response_data
    # userId = str(response_data['data']['id'])
    # uk = response_data['data']['uk']
    #
    # # save_user_session_data(userId, uk)
    #
    # print(f"~~~~~~~~~~ Created new user -*-{userId}-*-")
    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # return userId, uk
