# name: 雨云
# Author: sicxs
# Date: 2024-12-4/
# export wy_yuyun="账号#密码"
# 换行 & 分割 
# 功能:签到
# cron: 20 8 * * *
# new Env('雨云');


import json
import hashlib
import requests,random
import time,re,os,sys
import config
s = requests.session()
def index(username,password):#登录信息
    url = "https://api.v2.rainyun.com/user/login"
    hederd = {
        "authority": "api.v2.rainyun.com",
        "method": "POST",
        "path": "/user/login",
        "scheme": "https",
        "content-length": "41",
        "sec-ch-ua-platform": "\"Windows\"",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://app.rainyun.com",
        "referer": "https://app.rainyun.com/",
        "accept-language": "zh-CN,zh;q=0.9",
        "priority": "u=1, i"
        }
    data = {
    "field": username,
    "password": password
    }
    response = s.post(url, headers=hederd, json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['code'] == 200:
        cookies = response.cookies
        Token = cookies['X-CSRF-Token']
        print(f"登录成功,用户名：{username}")
        qiadnao(cookies,Token)
    else:
        print(f"登录失败,{info['message']}")


def qiadnao(cookie,Token):
    url = "https://api.v2.rainyun.com/user/reward/tasks"
    header = {
            "authority": "api.v2.rainyun.com",
            "method": "POST",
            "path": "/user/reward/tasks",
            "scheme": "https",
            "content-length": "44",
            "sec-ch-ua-platform": "\"Windows\"",
            "x-csrf-token": Token,
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://app.rainyun.com",
            "referer": "https://app.rainyun.com/",
            }
    data = {
        "task_name": "每日签到",
        "verifyCode": ""
        }
    response = s.post(url, headers=header, json=data, cookies=cookie)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['code'] == 200:
        print("签到成功")
    elif info['code'] == 30011: 
        print("已签到") 
    else:
        print(info['message'])

def sicxs():
    try:
        env_cookie = os.environ.get("wy_yuyun")
        si_cookie = getattr(config, 'wy_yuyun', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_yuyun='' 或在 config.py 中设置 wy_yuyun =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_yuyun='' 或在 config.py 中设置 wy_yuyun =")
        sys.exit()

    list_cookie = re.split(r'\n|&', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            list = list_cookie_i.split("#")
            index(list[0], list[1])
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错")    

    print(f'\n-----------  执 行  结 束 -----------')






if __name__ == '__main__':
   sicxs()
