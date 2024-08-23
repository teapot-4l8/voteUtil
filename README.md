前言：`app.json`文件不存在，有没有大佬有更好的解决办法？欢迎师傅们在评论区指点江山 :P

# 注册账号

注册了之后没有地方注销，挺烦的。

![image-20240807215328561](README.assets/image-20240807215328561.png)

看来是从微信缓存里获取登录信息的。

也就是说，清除微信缓存就可以啦！

![image-20240807220020724](README.assets/image-20240807220020724.png)

清除完后重新编译，就又需要登录了，方便调试。

![image-20240807220502457](README.assets/image-20240807220502457.png)

从`getSessionKey`里获取到`uk`。

触发注册接口，但是没有`getSessionKey`的包，只有`updateUserInfo`。猜测这个请求应该是在这之前完成的。

打断点，清除缓存，重新编译，果然断到了这里

![image-20240807221051925](README.assets/image-20240807221051925.png)

![image-20240807221310208](README.assets/image-20240807221310208.png)

就是它了，有了它，我们就可以无限生成用户去投票了，桀桀桀桀桀桀桀桀桀桀桀（反派笑）

定睛一看，还有个code需要处理。

搜一搜这是什么，以下内容来自微信官方文档

> ## 功能描述
>
> 调用接口获取登录凭证（code）。通过凭证进而换取用户登录态信息，包括用户在当前小程序的唯一标识（openid）、微信开放平台账号下的唯一标识（unionid，若当前小程序已绑定到微信开放平台账号）及本次登录的会话密钥（session_key）等。用户数据的加解密通讯需要依赖会话密钥完成。

看来是开发者要考虑的事，如果想伪造应该可以试试这个方法 https://www.cnblogs.com/du-jun/p/12720945.html

我就懒得去弄了，直接发送请求试下

![image-20240807223201595](README.assets/image-20240807223201595.png)

这个请求是复制curl的，我发现它请求头里居然有sk!

可是要获得sk不是要先向这个接口发送请求吗？

于是我猜测应该是什么缓存问题吧，于是把headers里的`annikey`和`sk`删掉，发现果然依旧可以获得数据


# 投票接口逆向

https://www.annikj.com/vote/elect/goVote.do

## `annikey`

不要在开发工具搜索，要在控制台那里搜，打断点也是！

![image-20240806231651371](README.assets/image-20240806231651371.png)

目测是md5。逆向过程略，太简单。抠出来运行的结果和前端对比下，是正确的！

![image-20240806234408466](README.assets/image-20240806234408466.png)

![image-20240806234518315](README.assets/image-20240806234518315.png)

## `sk`

前面略，找到`uk`

![image-20240806235256035](README.assets/image-20240806235256035.png)

`uk`是从请求里获得的

![image-20240806235540949](README.assets/image-20240806235540949.png)

大概率是用户凭证一样的东西，一个用户一个样。

多投几次，在这里断下来，发现是定值，啊吧啊吧，固定下来就行。

update: 用注册账号的接口获取

## js->python

把js写成python也行的，或者用`execjs`

```python
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
```

# 微信开发者工具动态调试问题

## `app.json`不存在

手动创建，除了pages，其它人和代码有一个能跑就行。pages看报错，缺啥补啥

```json
{
  "pages":[
    "pages/index/index",
    "pages/user/user",
    "pages/elect/elect",
    "pages/elect/checkPlayer",
    "pages/elect/playerInfo/playerInfo",
    "pages/login/loginNew"
  ],
  "tabBar": {
    "list": [{
      "pagePath": "pages/index/index",
      "text": "首页",
      "iconPath": "image/home.png"
    },{
      "pagePath": "pages/user/user",
      "text":"我的",
      "iconPath": "image/sex.png"
    }]
  }

}
```

## 白屏

检查一下本地设置，把勾取消，把勾勾上

![image-20240806225628246](README.assets/image-20240806225628246.png)



## 投票详情点不进去

在`pages`里添加相应页面

```json
  "pages":[
    "pages/index/index",
    "pages/user/user",
    "pages/elect/elect",
    "pages/elect/checkPlayer",
    "pages/elect/playerInfo/playerInfo",
    "pages/login/loginNew"
  ],
```

## 点不了同意

点了没反应，如果有大佬知道问题在哪，或者更方便的办法，欢迎在评论区指点 :D

![image-20240806225825307](README.assets/image-20240806225825307.png)

搜关键词`同意并继续` 看是哪个坑爹玩意

![image-20240806230244372](README.assets/image-20240806230244372.png)

搜索`privacyPopup` ， 把`usingComponents`那行全删了

![image-20240806230356167](README.assets/image-20240806230356167.png)

那几个js里的都要删

## 断点无效

要在控制台那里打断点

![image-20240806233611705](README.assets/image-20240806233611705.png)


# 优化

## 上代理

略


## 数据库

新建的那么多用户，第二天想再次使用，不新建了。

数据库，启动！

```
net start mysql57
mysql -u root -p
6666
```

查看database

```sql
SHOW DATABASES;
```

使用 USE 命令选择你想查看的数据库

```sql
USE database_name;
```

要查看数据库中的所有表格，可以使用：
```sql
SHOW TABLES;
```

查看表格内容
```sql
SELECT * FROM user_data(表名)
```


增加数据
```python
    try:
        result = cursor.execute(f"INSERT INTO user_data (userId, uk) VALUES ('{userId}', '{uk}')")
        conn.commit()
    except:
        print("数据写入失败")
        conn.rollback()
```

修改数据
```python
def user_vote_minus_one(userId):
    try:
        cursor.execute(f"UPDATE user_data SET remain_votes = remain_votes - 1 WHERE userId = '{userId}'")
        conn.commit()
    except:
        conn.rollback()
```

查看数据
```python
def read_data_from_database():
    cursor.execute("SELECT * FROM user_data")
    result = cursor.fetchone()
    # print(result)
    return result
```



## 多线程

票数差得太多，就用多线程追一下吧。。。

在多线程环境下操作数据库时，有几个注意事项需要考虑：

1. **数据库连接池**: 每个线程都应该有自己的数据库连接，而不是共享一个连接。使用数据库连接池可以更好地管理连接，避免连接泄漏和性能问题。

2. **事务管理**: 确保在操作数据库时使用事务来维护数据的一致性。在多线程环境下，确保每个线程的操作都在一个事务内完成，以避免数据不一致的情况发生。

3. **线程安全性**: 确保数据库操作是线程安全的。某些数据库操作可能不是线程安全的，需要特别注意并采取措施来保证线程安全。

4. **异常处理**: 在操作数据库时要注意异常处理。确保在发生异常时能够正确地回滚事务并释放资源，以避免数据损坏或资源泄漏。

5. **性能考虑**: 在设计多线程数据库操作时，要考虑数据库的性能。并发操作可能会导致数据库性能瓶颈，需要合理设计和调整线程数量。

遵循这些注意事项可以帮助确保在多线程环境下操作数据库时的数据完整性和性能。


## 协程

这么快都不能满足你吗？别把服务器创死了 XD


