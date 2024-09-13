""""
该模块负责完成免费代理IP的采集
"""
import requests
import re
import json
from lxml import etree
from proxy_redis import ProxyRedis
from threading import Thread
import time

# 基类, 给后面的类, 继承
# 直接让他继承Thread, 后面所有的子类就都是线程类了.
class IPAbstract(Thread):
    def __init__(self):
        super().__init__()   # 初始化父类
        self.pr = ProxyRedis()  # 创建对象

    def save_ip(self, ips):  # 保存数据的
        for ip in ips:
            self.pr.add_ip(ip)     # 执行新增功能


class KuaiIP(IPAbstract):
    def __init__(self):
        super().__init__()  # 初始化父类的.
        self.session = requests.session()
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "cookie": "channelid=0; sid=1724402323223731; _gcl_au=1.1.654194644.1724403811; _ss_s_uid=65ea3ce1aea84613c7b55ff79b8c264d; _gid=GA1.2.608596748.1724413823; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1724413823; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1724413823; HMACCOUNT=0BFAD8D83E97B549; _ga=GA1.1.1804515308.1724403811; _ga_DC1XM0P4JL=GS1.1.1724421451.4.1.1724421452.59.0.0",
            "dnt": "1",
            "host": "www.kuaidaili.cn",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }

    def run(self):  # start后, 启动线程
        data = self.get_one_page_ip(1)
        self.save_ip(data)

    def get_one_page_ip(self, page=1):  # 采集一页数据
        if page == 1:
            url = "https://www.kuaidaili.cn/free/intr/"
        else:
            url = f"https://www.kuaidaili.cn/free/intr/{page}/"
        resp = self.session.get(url)
        # print(resp.text)
        # 提取ip数据
        obj = re.compile(r"const fpsList = (?P<ip>.*?);", re.S)
        ips = obj.search(resp.text).group("ip")
        ips_list = json.loads(ips)
        results = []  # 封装返回数据
        for ip_dic in ips_list:
            proxy_ip = ip_dic['ip'] + ":" + ip_dic['port']
            # print(proxy_ip)
            # 装上ip数据
            results.append(proxy_ip)
        return results


class IP89(IPAbstract):
    def __init__(self):
        super().__init__()
        self.session = requests.session()
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "cookie": "Hm_lvt_f9e56acddd5155c92b9b5499ff966848=1724403815; HMACCOUNT=0BFAD8D83E97B549; https_waf_cookie=096d6e7b-5923-48e9020fb49d71b6d8725df40607a2301127; Hm_lpvt_f9e56acddd5155c92b9b5499ff966848=1724409794; https_ydclearance=dbcaccd8ab8983eff5f742d9-e727-4580-b3c7-9e03d1f78de0-1724429388",
            "dnt": "1",
            "host": "www.89ip.cn",
            "pragma": "no-cache",
            "referer": "https://www.89ip.cn/pvq/index_1.html",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }

    def run(self):  # 启动程序
        data = self.get_one_page_ip(1)
        self.save_ip(data)

    def get_one_page_ip(self, page=1):  # 采集一页数据
        url = f"https://www.89ip.cn/pvq/index_{page}.html"
        resp = self.session.get(url)
        tree = etree.HTML(resp.text)
        trs = tree.xpath("//table[@class='layui-table']/tbody/tr")
        results = []
        for tr in trs:
            ip = tr.xpath("./td[1]/text()")
            port = tr.xpath("./td[2]/text()")
            ip = "".join(ip).strip()
            port = "".join(port).strip()
            proxy_ip = ip + ":" + port
            results.append(proxy_ip)
        return results


def run():
    while 1:
        # 快代理的采集
        # 89代理的采集
        # ....   你可以自己想办法植入, 多线程的逻辑
        # KuaiIP().run()  # KuaiIP() => 该对象中有几个属性?
        # IP89().run()
        # 多线程
        kuai_thread = KuaiIP()
        ip89_thread = IP89()
        # 启动各自的线程
        kuai_thread.start()
        ip89_thread.start()
        time.sleep(3*60)


if __name__ == '__main__':
    run()
