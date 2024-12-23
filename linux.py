# name: linux do
# Author: sicxs
# Date: 2024-11-25
# export wy_linux="账号#密码"
# 换行，# 分割 
# 功能:登录，浏览任务
# cron: 20 8 * * *
# new Env('linux do');

import json
import requests
import random
import time
import re
import os
import sys
import config


s = requests.session()

def csrf():  # csrf
    url = "https://linux.do/session/csrf"
    header = {
        "authority": "linux.do",
        "method": "GET",
        "path": "/session/csrf",
        "scheme": "https",
        "x-csrf-token": "undefined",
        "x-requested-with": "XMLHttpRequest",
        "sec-ch-ua-full-version": "\"131.0.2903.112\"",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "referer": "https://linux.do/login",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": "",
        "priority": "u=1, i"
        }
    response = s.get(url=url, headers=header)
    response.encoding = "utf-8"
    info = response.text
    pattern = re.compile(r'"csrf":"(.*?)"')
    matches = pattern.findall(info)
    return matches[0]

def headers():  # 登录请求头
    csrf_token = csrf()
    header = {
        "authority": "linux.do",
        "method": "POST",
        "path": "/session",
        "scheme": "https",
        "x-csrf-token": csrf_token,
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 Edg/131.0.0.0",
        "accept": "*/*",
        "discourse-present": "true",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://linux.do",
        "referer": "https://linux.do/",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }
    return header

def headers_a():  # 浏览帖子登录请求头
    csrf_token = csrf()
    header = {
        "authority": "linux.do",
        "method": "GET",
        "scheme": "https",
        "x-csrf-token": csrf_token,
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 Edg/131.0.0.0",
        "accept": "*/*",
        "discourse-present": "true",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://linux.do",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://linux.do/",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }
    return header

def list_info():  # 获取 帖子列表
    url = "https://linux.do/latest.rss"
    header = headers_a()
    response = s.get(url=url, headers=header)
    response.encoding = "utf-8"
    info = response.text
    pattern = re.compile(r'<source url="https://linux.do/t/topic/(.*?).rss">(.*?)</source>')
    matches = pattern.findall(info)
    post_list = []
    for i in matches:
        post_list.append((i[0], i[1]))
    return post_list
def wy_get():
    url = "https://linux.do"
    header = {
        "authority": "linux.do",
        "method": "GET",
        "path": "/login",
        "scheme": "https",
        "origin": "https://linux.do",
        "x-requested-with": "XMLHttpRequest",
        "content-type": "application/x-www-form-urlencoded",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "referer": "https://linux.do/login",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }
    response = s.get(url=url, headers=header)
    response.encoding = "utf-8"
def index(username, password):  # 登录
    url = "https://linux.do/session"
    header = headers()
    data = {
        "login": username,
        "password": password,
        "second_factor_method": "1",
        "timezone": "Asia/Shanghai"
    }
    
    response = s.post(url=url, headers=header, data=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    print(f"登录成功,用户名：{info['users'][0]['name']}")
    cookies = response.cookies
    list_info_a(cookies)
    zongjie(cookies)

def list_info_a(cookies):  # 浏览帖子
    posts = list_info()
    for i in posts:
        url = f"https://linux.do/t/topic/{i[0]}"
        header = headers_a()
        response = s.get(url=url, headers=header, cookies=cookies)
        response.encoding = "utf-8"
        print(f"浏览帖子：{i[1]}")
        time.sleep(random.randint(30, 50))
    print("浏览帖子任务完毕！")
    
def zongjie(cookies):
    url = "https://linux.do/u/sicxs/summary.json"
    header = headers_a()
    response = s.get(url=url, headers=header, cookies=cookies)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    a = info['user_summary']['time_read']
    b = int(a/60)
    print(f"访问天数：{info['user_summary']['days_visited']}天,阅读时间：{b}分钟,浏览话题：{info['user_summary']['topics_entered']},已读帖子：{info['user_summary']['posts_read_count']},已点赞：{info['user_summary']['likes_given']},已收到赞：{info['user_summary']['likes_received']}")

def sicxs():
    try:
        env_cookie = os.environ.get("wy_linux")
        si_cookie = getattr(config, 'wy_linux', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_linux='' 或在 config.py 中设置 wy_linux =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_linux='' 或在 config.py 中设置 wy_linux =")
        sys.exit()

    list_cookie = re.split(r'\n|&', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            list = list_cookie_i.split("#")
            wy_get()
            time.sleep(3)
            index(list[0], list[1])
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错")    

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
    sicxs()