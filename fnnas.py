# name: 飞牛nas
# Author: sicxs
# Date: 2024-11-4
# export wy_fnnas="cookie" 换行,& 分割
# cron: 20 8 * * *
# new Env('飞牛nas');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []
env_name = "wy_fnnas"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]


def index(cookie, session):
    url = 'https://club.fnnas.com/plugin.php?id=zqlj_sign'
    header = {
        "Connection": "keep-alive",
        "host": "club.fnnas.com",
        "method": "GET",
        "path": "/",
        "referer": "https://club.fnnas.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie": cookie
    }
    try:
        response = session.get(url=url, headers=header)
        info = response.text
        if "我的打卡动态" in info:
            pattern = re.compile(r'zqlj_sign&sign=(.*?)"')
            pr("开始签到")
            matches = pattern.findall(info)
            if not matches:
                pr("解析签到参数失败，可能页面结构变化或 cookie 无效")
                return
            sgin(cookie, matches[0], session)
        else:
            pr("登录失败,账户可能已过期")
    except Exception as e:
        pr(e)

def sgin(cookie, formhash, session):
    url = f'https://club.fnnas.com/plugin.php?id=zqlj_sign&sign={formhash}'
    header = {
        "Connection": "keep-alive",
        "host": "club.fnnas.com",
        "method": "GET",
        "path": f"/plugin.php?id=zqlj_sign&sign={formhash}",
        "referer": "https://club.fnnas.com/plugin.php?id=zqlj_sign",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie": cookie
    }
    try:
        response = session.get(url=url, headers=header)
        info = response.text
        if "您今天已经打过卡了，请勿重复操作！" in info:
            pr("您今天已经打过卡了，请勿重复操作！")
            my(cookie, session)
        elif "打卡成功" in info:
            pr("打卡成功")
            my(cookie, session)
    except Exception as e:
        pr(e)

def my(cookie, session):
    url = 'https://club.fnnas.com/home.php'
    header = {
        "Connection": "keep-alive",
        "host": "club.fnnas.com",
        "method": "GET",
        "path": "/home.php",
        "referer": "https://club.fnnas.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie": cookie
    }
    try:
        response = session.get(url=url, headers=header)
        pattern = re.compile(r"em>用户名</em>(.*?)<")
        pattern2 = re.compile(r'<em>飞牛币</em>(.*?) </li>')
        pattern3 = re.compile(r'<em>登陆天数</em>(.*?) </li>')
        pattern4 = re.compile(r'金钱<span>(.*?)</span>')

        matches = pattern.findall(response.text)
        matches1 = pattern2.findall(response.text)
        matches2 = pattern3.findall(response.text)
        matches3 = pattern4.findall(response.text)
        if not matches or not matches1 or not matches2 or not matches3:
            pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
            return

        pr("用户名：" + matches[0] + " 飞牛币：" + matches1[0] + " 登录天数：" + matches2[0] + " 金钱：" + matches3[0])

    except Exception as e:
        pr(e)

# ====== 固定代码 ======

def pr(message):
    msg.append(message + "\n")
    print(message)  

def create_session_with_retry():
    """创建带有重试机制的会话"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=STATUS_FORCE_LIST,
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def get_accounts():
    if not os.path.exists('config.py'):
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(f'#可以在此文件中添加配置变量，例如：\n{env_name} =""\n')
        print(f"未检测到环境变量，已创建配置文件config.py，请填写变量后重试。")
        sys.exit()

    import config

    env_cookie = os.environ.get(env_name, "")
    si_cookie = getattr(config, env_name, "")
    cookies = "\n".join(filter(None, [env_cookie, si_cookie]))
    if not cookies.strip():
        print(f"请设置变量 export {env_name}='' 或在 config.py 中设置 {env_name} =")
        sys.exit()

    items = [c.strip() for c in re.split(r'\n|&', cookies) if c.strip()]
    seen = set()
    accounts = []
    for c in items:
        if c not in seen:
            seen.add(c)
            accounts.append(c)
    return accounts

def sicxs():
    
    accounts = get_accounts()
    total = len(accounts)
    if total < 1:
        print("未检测到账号")
        return
    for i, account in enumerate(accounts, 1):
        session = create_session_with_retry()
        try:
            print(f'\n----------- 账号【{i}/{total}】执行 -----------')
            index(account, session)
        except Exception as e:
            print(f"账号【{i}/{total}】执行出错：{e}")
        finally:
            send("飞牛nas", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()
