import json
import pymysql
# Assuming conn and cursor are already defined

def save_user_session_data(userId, uk):
    # TODO 服务器可能会重置用户数据 造成主键重复
    # try:
    result = cursor.execute(f"INSERT INTO user_data (userId, uk) VALUES ('{userId}', '{uk}')")
    conn.commit()
    print(f"已经写入{userId}")


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='6666', db='dnfisreal')
cursor = conn.cursor()


with open("用户记录.json", 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        userId = data['data']['id']
        uk = data['data']['uk']
        save_user_session_data(userId, uk)  # Assuming save_user_session_data function is defined

