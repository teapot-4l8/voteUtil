import requests
import time
import random
import hashlib
import json
import datetime
import sys
from concurrent.futures import ThreadPoolExecutor
import pymysql



# 数据库连接信息
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '6666',
    'db': 'dnfisreal'
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
        'pId': '21866',  # 选手信息
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
    cursor = pymysql.connect(**DB_CONFIG).cursor()
    cursor.execute("SELECT * FROM user_data WHERE remain_votes > 0 ORDER BY RAND() LIMIT 10")
    results = cursor.fetchall()
    
    user_data = []
    for result in results:
        userId = result['userId']
        uk = result['uk']
        user_data.append((userId, uk))
        
    return user_data

def user_vote_minus_one(userId, cursor):
    try:
        cursor.execute(f"UPDATE user_data SET remain_votes = remain_votes - 1 WHERE userId = '{userId}'")
        conn.commit()
    except:
        conn.rollback()

def refresh_user_votes():
    """
    新的一天，票数全为50
    """
    conn = pymysql.connect(**DB_CONFIG)
    conn.cursor().execute("UPDATE user_data SET remain_votes = 50")
    conn.commit()

def set_user_votes_to_zero(userId, cursor):
    try:
        cursor.execute(f"UPDATE user_data SET remain_votes = 0 WHERE userId = '{userId}'")
        conn.commit()
    except:
        conn.rollback()
        print("fuck!")
        
def lets_fucking_go(userId, uk):
    # 每个线程拥有自己的数据库连接
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    while True:  # 一个用户有50票 不管它了 一直投 投到投不了为止
        print(f"User {userId} has voted {i+1} times")
        try:
            flag = go_vote(userId, uk, cursor) 
            if flag:  # 出现异常，投票失败
                return
            user_vote_minus_one(userId, cursor) 
        except Exception as e:
            set_user_votes_to_zero(userId, cursor)  # 确保票数为0
            print(f"User {userId} has run out of votes")
            break

    # 关闭当前线程的数据库连接
    cursor.close()
    conn.close()




def main():
    remain_local_user = True  # 本地用户还有票数
    # 从数据库中取10个用户
    user_data = read_data_from_database()
    with ThreadPoolExecutor(max_workers=10) as executor:  # 创建一个最大容纳10个线程的线程池
        if remain_local_user:
            for userId, remain_vote_num in user_data:
                executor.submit(lets_fucking_go, userId, uk)
        else:
            print("哎呀，没人了，要去造人了")
            for _ in range(10):  # 创建10个用户线程
                userId, uk = get_session_key()
                executor.submit(lets_fucking_go, userId, uk)

    print("===========程序执行完毕==============")



if __name__ == "__main__":
    # refresh_user_votes()  # 每天运行一次
    main()
