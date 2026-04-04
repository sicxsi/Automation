# name: 家园
# Author: sicxs
# Date: 2024-10-29
# export wy_hdhome="cookie" &,换行分割
# cron: 8 8 * * *
# new Env('家园');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []
env_name = "wy_hdhome"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

def get_header(cookie):
    header = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "host":"hdhome.org",
        "referer":"https://hdhome.org",
        "cookie":cookie
    }
    return header
def index(cookie, session):
    url = 'https://hdhome.org/index.php'
    header = get_header(cookie)
    try:
        response = session.get(url, headers=header)
        if not response:
            pr("本账号请求失败，跳过该账号。")
            return
        time.sleep(3)
        info = response.text
        if "签到" in info:
            pr("账号登陆成功")
            if "签到已得" in info:
                pr("您今天已经签到过了，请勿重复刷新。")
                torrents(cookie, session)
            else:
                attendance(cookie, session)
        else:
            pr("登录失败")
    except Exception as e:
        pr(e)
def attendance(cookie, session):
    url = 'https://hdhome.org/attendance.php'
    header = get_header(cookie)
    try:
        response = session.get(url, headers=header)
        if not response:
            pr("签到请求失败，跳过该账号。")
            return
        time.sleep(3)
        info = response.text
        if "签到已得" in info:
            pr("签到成功，请勿重复刷新。")
            torrents(cookie, session)
        else:
            pr("签到失败，已达到最大重试次数，跳过该账号。")
    except Exception as e:
        pr(e)
def torrents(cookie, session):
    url = 'https://hdhome.org/torrents.php'
    header = get_header(cookie)
    try:
        response = session.get(url=url, headers=header)
        time.sleep(3)
        pattern = re.compile(r"class='(.+?)'><b>(.+?)</b>")
        pattern2 = re.compile(r']: (.*)&nbsp;\(')
        pattern3 = re.compile(r'签到已得(.*?)\) ')
        pattern4 = re.compile(r'做种积分：</font>(.*?) ')
        matches = pattern.findall(response.text)
        matches1 = pattern2.findall(response.text)
        matches2 = pattern3.findall(response.text)
        matches3 = pattern4.findall(response.text)
        if not matches or not matches1 or not matches2 or not matches3:
            pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
            return
        pr("用户名：" + matches[0][1] + " 魔力值：" + matches1[0] + " 签到已得：" + matches2[0] + " 做种积分：" + matches3[0])
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
    """固定代码，获取变量"""
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
            send("家园", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()
