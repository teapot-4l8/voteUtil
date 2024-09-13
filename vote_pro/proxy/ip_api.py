"""

api接口:让用户可以通过http协议访问到我们代理ip池中的ip
http://xxxx.xxx.xxx/get_ip

pip install sanic
pip install sanic_cors
"""
import time
from proxy_redis import ProxyRedis
from sanic import Sanic, text
from sanic_cors import CORS  # 解决跨域问题. 让你的api可以直接访问

# 创建一个web应用程序
app = Sanic("ip")
CORS(app)  # 解除跨域限制

red = ProxyRedis()

# 挂路由, 当有人访问该url的时候. 执行xxxx操作
# http://127.0.0.1:10086/get_ip
@app.route("/get_ip")
def erlingqi(req):
    # 拿到一个可以使用的ip
    ip = red.get_ok_ip()
    # 返回该ip
    return text(ip)  # 返回给浏览器的内容.


def run():
    time.sleep(20)
    # 启动web应用程序
    # http://127.0.0.1:10086
    app.run(host='127.0.0.1', port=10086)


if __name__ == '__main__':
    run()
