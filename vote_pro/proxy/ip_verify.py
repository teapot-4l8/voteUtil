"""
用来做ip校验的
拿到所有的ip地址. 发请求看看. 如果可以用, 就是ok的, 如果不能拿到结果(超时, 报错)
扣分就可以了
"""
from proxy_redis import ProxyRedis
import asyncio
import aiohttp
import time


async def check_one(ip, sem, pr):
    try:
        timeout = aiohttp.ClientTimeout(10)
        async with sem:
            async with aiohttp.ClientSession(timeout=timeout, headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9",
                "cache-control": "no-cache",
                "connection": "keep-alive",
                "cookie": "BIDUPSID=E12736861933E9F686BC7CCD97A21C19; PSTM=1724425568; H_PS_PSSID=60519_60628_60664_60678; BD_HOME=1; BAIDUID=E12736861933E9F686BC7CCD97A21C19:FG=1; BAIDUID_BFESS=E12736861933E9F686BC7CCD97A21C19:FG=1; BD_UPN=12314753; BA_HECTOR=8h2104ah810haha52lag84al31r4ku1jch9b11v; ZFY=Ao0lKJId0oTYEWHVavwwOfTSk2lMbr:BVTcFYeat3FYI:C",
                "dnt": "1",
                "host": "www.baidu.com",
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
            }) as session:
                # aiohttp挂代理的逻辑: 直接给http/https://ip:port 就可以了
                async with session.get("http://www.baidu.com", proxy="http://"+ ip) as resp:
                    await resp.content.read()  # 随便接一下结果, 结果没用
                    if resp.status in [200, 302]:
                        # ip是可用的
                        # 好ip. 满分
                        pr.set_max_score(ip)
                        print("ip可用, 满分", ip)
                    else:
                        # ip是不可用的, 垃圾, 扣分
                        pr.desc_score(ip)
                        print("ip不可用, 垃圾, 扣分", ip)

    except Exception as e:
        # 如果全是正确, 全是错误, 看看报错信息
        # import traceback
        # print(traceback.format_exc())

        # ip是不可用的
        pr.desc_score(ip)
        print("ip不可用, 垃圾, 扣分", ip)


async def check_all(ips, pr):
    # 信号量,用来控制并发量的
    sem = asyncio.Semaphore(20)

    tasks = []
    for ip in ips:
        # 启动协程任务
        tk = asyncio.create_task(check_one(ip, sem, pr))
        tasks.append(tk)
    await asyncio.wait(tasks)


def run():
    # 让校验滞后, 保证IP池有数据
    time.sleep(10)
    pr = ProxyRedis()
    while 1:
        ips = pr.get_all_ip()
        asyncio.run(check_all(ips, pr))
        time.sleep(60*5)  # 每隔5分钟检测一次


if __name__ == '__main__':
    run()
