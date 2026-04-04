# name: 全球主机论坛
# Author: sicxs
# Date: 2024-11-4
# export wy_hostloc="cookie" 换行,&分割
# cron: 0 8 * * *
# new Env('全球主机论坛');

import requests
import os,json,sys,random
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wy_hostloc"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]


def get_header(cookie):
    header = {
        "Connection":"keep-alive",
        "authority":"hostloc.com",
        "method":"GET",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "referer":"https://hostloc.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "content-type": "text/html; charset=utf-8",
        "cookie":cookie
    }
    return header
def index(cookie, session): #登录
    url = 'https://hostloc.com/forum.php'
    header = get_header(cookie)
    try:
        response = session.get(url=url, headers=header)
        if "积分" in response.text:
            pr("登陆成功")
            pattern = re.compile(r"discuz_uid = '(.*?)'")
            matches = pattern.findall(response.text)
            if not matches:
                pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
                return
            uid = str(matches[0])
            sicxs_task(cookie, session)
            time.sleep(5)
            my(cookie, uid, session)
        else:
            pr("登录失败")
    except Exception as e:
        pr(e)

def my(cookie, uid, session): #我的信息
    url = f'https://hostloc.com/home.php?mod=space&uid={uid}&do=profile'
    header = get_header(cookie)
    response = session.get(url=url, headers=header)
    pattern = re.compile(r'title="访问我的空间">(.*?)</a>')
    pattern2 = re.compile(r'<li><em>积分</em>(.*?)</li><li><em>威望</em>(.*?) </li>')
    pattern3 = re.compile(r'<li><em>金钱</em>(.*?) </li>')

    matches = pattern.findall(response.text)
    matches1 = pattern2.findall(response.text)
    matches2 = pattern3.findall(response.text)
    if not matches or not matches1 or not matches2:
        pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
        return

    pr("用户名：" + matches[0] + " 积分：" + matches1[0][0] + " 威望：" + matches1[0][1] + " 金钱：" + matches2[0])

def sicxs_task(cookie, session): #任务
    for i in range(10):
        uuid = random.randint(5000, 15000)
        time.sleep(5)
        url = f'https://hostloc.com/space-uid-{uuid}.html'
        header = get_header(cookie)
        response = session.get(url=url, headers=header)
        info = response.text
        if "个人资料" in info:
            pr(f"第{i}次访问{uuid}用户成功")
        elif "您指定的用户空间不存在" in info:
            pr("访问失败，重试中")
        else:
            pr("访问失败，重试中")

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
            send("全球主机论坛", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()

