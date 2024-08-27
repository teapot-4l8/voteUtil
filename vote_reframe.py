import requests
import time
import sys
import random
import hashlib
import json
import datetime
import pymysql
from concurrent.futures import ThreadPoolExecutor

# Database configuration
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
    # 千万不能放全局
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
    return code

def save_user_session_data(userId, uk):
    # TODO 服务器可能会重置用户数据 造成主键重复
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    result = cursor.execute(f"INSERT INTO user_data (userId, uk) VALUES ('{userId}', '{uk}')")
    conn.commit()

def get_session_key():  # TODO 一旦走到了这里就是永远while下去直到服务器挂掉 有点危险 记得设置一个终值
    data = {
        'code': '0b3wPuFa1nyiWH0cCtIa1x3oEg4wPuFV',
        'scene': '1001',
        'isQQ': 'false',
        'anniTime': str(int(time.time() * 1000)),
        'randomStr': int(1e9 * random.random()),
    }
    response = requests.post('https://www.annikj.com/vote/user/getSessionKey.do', headers={}, data=data)
    response_data = json.loads(response.text)
    userId = str(response_data['data']['id'])
    uk = response_data['data']['uk']

    save_user_session_data(userId, uk)

    print(f"~~~~~~~~~~ Created new user -*-{userId}-*-")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return userId, uk

def read_data_from_database(thread_num):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE remain_votes > 0 ORDER BY RAND() LIMIT {thread_num}")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Refresh user votes
def refresh_user_votes():
    conn = pymysql.connect(**DB_CONFIG)
    conn.cursor().execute("UPDATE user_data SET remain_votes = 50")
    conn.commit()
    conn.close()

# Set user votes to zero
def set_user_votes_to_zero(userId, cursor, conn):
    try:
        cursor.execute(f"UPDATE user_data SET remain_votes = 0 WHERE userId = '{userId}'")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error updating user votes:", e)

def lets_fucking_go(userId, uk):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for i in range(10):  # Each user has 50 votes
        code = go_vote(userId, uk)
        if code == 0:
            print(f"User {userId} has voted {i + 1} times")
        elif code == -1:
            print(f"User {userId} has run out of votes")
            break
        else:
            print(f"{userId}接口异常:uk={uk}")
            # sys.exit()  # TODO 这个没用 换一种方案

    set_user_votes_to_zero(userId, cursor, conn)
    cursor.close()
    conn.close()

# Main function
def main():
    thread_num = 3
    remain_local_user = True  # Local users still have votes

    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        while True:
            if remain_local_user:
                user_data = read_data_from_database(thread_num)
                if not user_data:  # No more local users with votes
                    remain_local_user = False
                    # continue
                futures = [executor.submit(lets_fucking_go, userId, uk) for userId, uk, remain_vote_num in user_data]
            # else:
            #     print("No users left, creating new users...")
            #     futures = [executor.submit(lets_fucking_go, *get_session_key()) for _ in range(thread_num)]
            
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception caught in future: {e}")
                
    print("=========== Program finished ==============")


if __name__ == "__main__":
    # refresh_user_votes() # 每天执行一次 或者执行 exc_every_day.sh
    main()
