# name: 通信人家园
# Author: sicxs
# Date: 2024-11-25
# export wy_txrjy="账号#密码" &,换行分割 
# cron: 20 8 * * *
# new Env('通信人家园');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wy_txrjy"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]


def get_header(cookie=None):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Cache-Control': "max-age=0",
        'sec-ch-ua': "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'Origin': "https://www.txrjy.com",
        'Upgrade-Insecure-Requests': "1",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-User': "?1",
        'Sec-Fetch-Dest': "document",
        'Referer': "https://www.txrjy.com/forum.php",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            }
    if cookie:
        header["Cookie"] = cookie
    return header

def get_logn(name, password, session):  # 登录
    url = "https://www.txrjy.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes"
    header = get_header()
    data = {
        "username": name,
        "password": password,
        "quickforward": "yes",
        "handlekey": "ls"
    }
    response = session.post(url=url, headers=header, data=data)
    info = response.text
    if "登录失败" in info:
        pr("登录失败")
        return None
    else:
        pr("登陆成功")
        # 优先使用会话中的 cookies（包含重定向后设置的所有 cookie）
        cookie_dict = session.cookies.get_dict()
        if not cookie_dict:
            # 尝试从响应头取 Set-Cookie 作为回退并记录调试信息
            sc = response.headers.get('Set-Cookie')
            if sc:
                pr(f"未从 session 获取到 cookie，响应 Set-Cookie: {sc}")
                cookie_str = sc
            else:
                pr(f"未获取到 cookie，响应头: {response.headers}")
                return None
        else:
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
        index(cookie_str, session)
        return cookie_str

def index(cookie, session):  # 我的信息
    url = "https://www.txrjy.com/home.php?mod=spacecp&ac=credit&showcredit=1"
    header = get_header(cookie)
    response = session.get(url=url, headers=header)
    info = response.text
    time.sleep(3)
    pattern = re.compile(r'<em> 家园分:</em>(.*?)  &nbsp; </li>')
    pattern1 = re.compile(r'<li><em> 经验:</em>(.*?) </li>')
    pattern2 = re.compile(r'<em>积分:</em>(.*?) <span class="xg1">')
    pattern3 = re.compile(r'title="访问我的空间">(.*?)</a></strong>')
    matches = pattern.findall(info)
    matches1 = pattern1.findall(info)
    matches2 = pattern2.findall(info)
    matches3 = pattern3.findall(info)
    if not matches or not matches1 or not matches2 or not matches3:
        pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
        return
    pr(f"用户名: {matches3[0]} 积分: {matches2[0]} 经验: {matches1[0]} 家园分: {matches[0]}")

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
            parts = account.split("#")
            if len(parts) < 2:
                print("账号格式错误,请检查设置")
                continue
            get_logn(parts[0], parts[1], session)
        except Exception as e:
            print(f"账号【{i}/{total}】执行出错：{e}")
        finally:
            send("通信人家园", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()