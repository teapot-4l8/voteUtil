import requests

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 wechatdevtools/1.06.2209190 MicroMessenger/8.0.5 Language/zh_CN webview/',
    'content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://servicewechat.com/wx6b6da4e842c89b90/devtools/page-frame.html',
}

data = {
    'code': '0b3wPuFa1nyiWH0cCtIa1x3oEg4wPuFV',
    'scene': '1001',
    'isQQ': 'false',
    'anniTime': '1723039876928',
    'randomStr': '432194664',
}

response = requests.post('https://www.annikj.com/vote/user/getSessionKey.do', headers=headers, data=data)
print(response.text)