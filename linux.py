# name: linux do
# Author: sicxs
# Date: 2024-11-25
# export wy_linux="cookie"
# 换行，# 分割 
# 功能:登录，浏览任务
# 请在ip常用地使用
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



def list_info(header):  # 获取 帖子列表
    url = "https://linux.do/latest.rss"
    response = s.get(url=url, headers=header)
    response.encoding = "utf-8"
    info = response.text
    pattern = re.compile(r'<source url="https://linux.do/t/topic/(.*?).rss">(.*?)</source>')
    matches = pattern.findall(info)
    post_list = []
    for i in matches:
        post_list.append((i[0], i[1]))
    return post_list
def index(cookies):
    cookie_pairs = cookies.split(';')
    cookies_dict = {}
    for pair in cookie_pairs:
        key, value = pair.split('=', 1)
        cookies_dict[key.strip()] = value.strip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://linux.do/login',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=0, i',
    }
    response = requests.get('https://linux.do', cookies=cookies_dict, headers=headers)
    time.sleep(random.randint(8, 12))
    response.encoding = "utf-8"
    if "csrf" in response.text:
        print("登录成功")
        pattern = re.compile(r'<meta name="csrf-token" content="(.*?)" />')
        matches = pattern.findall(response.text)
        csrf = matches[0]
        list_info_a(cookies_dict)
        wy_info(cookies_dict)

    else:
        print("登陆失败,请查看cookie 是否正确")    
def list_info_a(header):  # 浏览帖子
    posts = list_info(header)
    for i in posts:
        url = f"https://linux.do/t/topic/{i[0]}"
        response = s.get(url=url, headers=header)
        response.encoding = "utf-8"
        print(f"浏览帖子：{i[1]}")
        time.sleep(random.randint(30, 50))
    print("浏览帖子任务完毕！")
    
def wy_info(header):
    url = "https://linux.do/u/sicxs/summary.json"
    response = s.get(url=url, headers=header)
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
            print(f"正在初始化登录...")
            index(list_cookie_i)
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错")    

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
    sicxs()
