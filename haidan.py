# name: 海胆
# Author: sicxs
# Date: 2024-11-2
# export wy_haidan="cookie"  换行,&分割
# cron: 10 9 * * *
# new Env('海胆');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []
env_name = "wy_haidan"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

def get_header(cookie):
    header = {
        "authority": "www.haidan.cc",
        "method": "GET",
        "path": "/index.php",
        "referer":"https://www.haidan.cc/torrents.php",
        "User-Agent": "Mozilla/5.0",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie":cookie
    }
    return header
def index(cookie, session):
    url = 'https://www.haidan.cc/index.php'
    header = get_header(cookie)
    try:
        response = session.get(url, headers=header)
        if not response:
            pr("账号登录失败，跳过该账号。")
            return
        time.sleep(3)
        info = response.text
        if "打卡" in info:
            pr("账号登陆成功")
            signin(cookie, session)
        else:
            pr("登录失败, 请检查cookie是否正确")
    except Exception as e:
        pr(e)

def signin(cookie, session):
    url = 'https://www.haidan.cc/signin.php'
    header = get_header(cookie)
    try:
        response = session.get(url, headers=header)
        if response.status_code == 200:
            pr("打卡成功，请勿重复刷新。")
            torrents(cookie, session)
        else:
            pr("打卡失败，已达到最大重试次数，跳过该账号。")
    except Exception as e:
        pr(e)


def user_stats(html): 
    stats = {}
    html = html.replace('&nbsp;', ' ')
    patterns = {
        'username': r"class=['\"]\w*User_Name['\"]><b>(.*?)</b>",
        'bonus': r'id=["\']magic_num["\']>([^<]+)</span>',
        'share_ratio': r"分享率[：:][\s\S]*?</font>\s*([\d.]+)",
        'uploaded': r"上传量[：:][\s\S]*?</font>\s*([\d.]+\s*[PTGMK]?B)",
        'downloaded': r"下载量[：:][\s\S]*?</font>\s*([\d.]+\s*[PTGMK]?B)",
        'm_level_bonus': r"等级积分[\s\S]*?<span>\s*([\d,.]+)\s*</span>",
    }
    for key, pattern in patterns.items():
        try:
            match = re.search(pattern, html)
            if match:
                value = match.group(1).strip()
                value = re.sub(r'\s+', ' ', value)
                stats[key] = value
            else:
                stats[key] = "未找到"
        except Exception as e:
            stats[key] = f"解析错误({e})"
    return stats



def torrents(cookie, session):
    url = 'https://www.haidan.cc/torrents.php'
    header = get_header(cookie)
    try:
        response = session.get(url=url, headers=header)
        requests = response.text
        stats = user_stats(requests)
        if stats['username'] == "未找到":
          print("页面解析失败，未找到用户名。")
          return
        pr(f"用户名: {stats['username']}, 魔力值: {stats['bonus']}, 上传量: {stats['uploaded']}, 下载量: {stats['downloaded']}, 分享率: {stats['share_ratio']}, 等级积分: {stats['m_level_bonus']}")
    except Exception as e:
        pr("登陆失败")

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
            send("海胆", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()
