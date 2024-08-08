import requests

headers = {
    'Connection': 'keep-alive',
    'annikey': '00ca9b6bc1acfc91da3baa9cbb85fde6',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 wechatdevtools/1.06.2209190 MicroMessenger/8.0.5 Language/zh_CN webview/',
    'sk': 'b734878d112e9d2ea338db816421a5d7',
    'content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://servicewechat.com/wx6b6da4e842c89b90/devtools/page-frame.html',
}

data = {
    'userStr': '{"id":3414092,"nickName":"456","avatarUrl":"https://qn-1253845026.cos.ap-shanghai.myqcloud.com/default/avatar.png"}',
    'anniTime': '1722866216443',
    'randomStr': '128915145',
    'userId': '3414092',
}

response = requests.post('https://www.annikj.com/vote/user/updateUserInfo.do', headers=headers, data=data)
print(response.text)