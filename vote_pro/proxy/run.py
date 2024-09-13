
from multiprocessing import Process
from ip_api import run as api_run
from ip_collections import run as col_run
from ip_verify import run as verify_run




def run():
    # 1. 采集
    p1 = Process(target=col_run)
    # 2. 校验
    p2 = Process(target=verify_run)
    # 3. api
    p3 = Process(target=api_run)

    p1.start()
    p2.start()
    p3.start()


if __name__ == '__main__':
    run()
