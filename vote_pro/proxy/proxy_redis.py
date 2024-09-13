"""
该模块负责, 免费代理ip池数据存储方面的事儿
数据存储到redis
从redis中提取数据
"""
from redis import Redis
import random


class ProxyRedis:
    def __init__(self):
        self.red = Redis(
            host="localhost",
            port=6379,  # redis默认端口号6379
            db=0,   # 0-15  16个库
            password="123456",
            decode_responses=True  # 是否需要解码 if false, will show sth. like '\xx'
        )

    def add_ip(self, ip):
        # 判断是否已经存在该IP
        if not self.red.zrank("proxy_ip", ip):
            # zset存储数据, 初始ip50分
            self.red.zadd("proxy_ip", {ip: 50})
            print("采集到了一个新的ip, 已经存储到redis", ip)
        else:
            print("采集到了一个新的ip, 但是, 已经存在了. ", ip)

    def get_all_ip(self):
        return self.red.zrange("proxy_ip", 0, -1)

    def set_max_score(self, ip):
        self.red.zadd("proxy_ip", {ip: 100})  # 满分

    def desc_score(self, ip):
        # 抠10分
        self.red.zincrby("proxy_ip", -10, ip)
        # 如果分值已经没有了. 删掉它
        score = self.red.zscore("proxy_ip", ip)
        if score == 0:
            self.red.zrem("proxy_ip", ip)

    def get_ok_ip(self):
        # 首选, 满分的ip, 从100分, 到100分, 全拿
        ips = self.red.zrangebyscore("proxy_ip", 100, 100, 0, -1)
        if not ips:
            # 没有满分的. 随机拿一个就完了
            ips = self.red.zrangebyscore("proxy_ip", 1, 100, 0, -1)
        return random.choice(ips)
