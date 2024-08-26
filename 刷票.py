import requests
import time
import random
import hashlib
import json
import datetime
import sys
import pymysql


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
    flag = 0  # 成功获取或投票数达到最大
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
    headers["sk"] = encrypt_param_new(data, uk)

    response = requests.post('https://www.annikj.com/vote/elect/goVote.do', headers=headers, data=data)
    print(response.text)
    resp = json.loads(response.text)
    code = resp['code']
    if code == 0:
        return flag
    elif code == -1:
        raise Exception("投满了，下一个")
    else:
        flag = 1  # 接口返回异常，接口加密更新，程序需要终止更新
    return flag

def get_session_key():
    """
    获取新用户并保存到数据库
    """
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
    userId = str(response_data['data']['id'])
    uk = response_data['data']['uk']

    save_user_session_data(userId, uk)

    print(f"~~~~~~~~~~ 创建新用户 -*-{userId}-*-")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return userId, uk


def read_data_from_database():
    cursor.execute("SELECT * FROM user_data WHERE remain_votes > 0")
    result = cursor.fetchone()
    # print(result)
    return result


def user_vote_minus_one(userId):
    try:
        cursor.execute(f"UPDATE user_data SET remain_votes = remain_votes - 1 WHERE userId = '{userId}'")
        conn.commit()
    except:
        conn.rollback()


def refresh_user_votes():
    """
    新的一天，票数全为50
    """
    try:
        cursor.execute("UPDATE user_data SET remain_votes = 50")
        conn.commit()
    except:
        conn.rollback()
        print("fuck!")


def set_user_votes_to_zero(userId):
    try:
        cursor.execute(f"UPDATE user_data SET remain_votes = 0 WHERE userId = '{userId}'")
        conn.commit()
    except:
        conn.rollback()
        print("fuck!")


def save_user_session_data(userId, uk):
    # TODO 服务器可能会重置用户数据 造成主键重复
    # try:
    result = cursor.execute(f"INSERT INTO user_data (userId, uk) VALUES ('{userId}', '{uk}')")
    conn.commit()
    # except Exception as e:
    #     print(f"数据写入失败: {e}")
    #     conn.rollback()



if "__main__" == __name__:
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='6666', db='dnfisreal')
    cursor = conn.cursor()

    # refresh_user_votes()  # 每天运行一次

    for user_numbers in range(99):  # 
        try:
            userId, uk, remain_vote_num = read_data_from_database()
        except TypeError:
            print("哎呀，没人了，要去造人了")
            userId, uk = get_session_key()

        for i in range(1, remain_vote_num + 1):  # 一个用户有50票  
            print(f"已刷{i + user_numbers*50}票")

            try:
                flag = go_vote(userId, uk)
                if flag:  # 出现异常 投票失败
                    sys.exit()
                    
                user_vote_minus_one(userId)
            except:  # 投满，下一个用户 
                set_user_votes_to_zero(userId)
                print(f"将用户{userId}剩余票数置零")
                break

    print("===========程序执行完毕==============")
    cursor.close()
    conn.close()
