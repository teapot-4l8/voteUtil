import requests
import time
import random
import hashlib
import json
import datetime
from concurrent.futures import ThreadPoolExecutor
import pymysql

# Database connection information
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '6666',
    'db': 'dnfisreal'
}

# Encryption functions
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

# Voting function
def go_vote(userId, uk):
    flag = 0  # Success or max votes reached
    anniTime = int(time.time() * 1000)
    random_str = int(1e9 * random.random())

    data = {
        'pId': '21866',  # Candidate information
        'userId': userId,  # User ID, must correspond with UK
        'isQQ': 'false',  # Fixed
        'aFrom': '5',  # Fixed
        'anniTime': str(anniTime),
        'randomStr': random_str,
    }

    headers = {}
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
        flag = 1  # Interface returns an error, the encryption has changed
    return flag

# Session key function
def get_session_key():
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

# Read data from database
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
def set_user_votes_to_zero(userId, cursor):
    try:
        cursor.execute(f"UPDATE user_data SET remain_votes = 0 WHERE userId = '{userId}'")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error updating user votes:", e)

# Voting function executed by each thread
def lets_fucking_go(userId, uk):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        for i in range(5):  # Each user has 50 votes
            print(f"User {userId} has voted {i + 1} times")
            try:
                flag = go_vote(userId, uk)
                if flag:  # If there's an error, stop voting
                    return
            except Exception as e:
                set_user_votes_to_zero(userId, cursor)
                print(f"User {userId} has run out of votes")
                break

    except Exception as e:
        print(f"Error in lets_fucking_go for user {userId}: {e}")
    finally:
        # Ensure resources are released properly
        set_user_votes_to_zero(userId, cursor)
        cursor.close()
        conn.close()

# Main function
def main():
    remain_local_user = True  # Local users still have votes
    thread_num = 3

    user_data = read_data_from_database(thread_num)
    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        if remain_local_user:
            futures = [executor.submit(lets_fucking_go, userId, uk) for userId, uk, remain_vote_num in user_data]
        else:
            remain_local_user = False
            print("No users left, creating new users...")
            futures = [executor.submit(lets_fucking_go, *get_session_key()) for _ in range(10)]
        
        # Optionally wait for all threads to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Exception caught in future: {e}")

    print("=========== Program finished ==============")

if __name__ == "__main__":
    main()