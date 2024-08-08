import requests

headers = {
    'Referer': 'https://servicewechat.com/wx6b6da4e842c89b90/devtools/page-frame.html',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.3 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1 wechatdevtools/1.06.2209190 MicroMessenger/8.0.5 Language/zh_CN webview/',
}

response = requests.request('post', 'https://www.annikj.com/vote/user/updateUserInfoData.do', headers=headers)
print(response.text)