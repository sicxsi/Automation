# name: 恩山无线论坛
# Author: sicxs
# Date: 2024-11-3
# export wy_rigth="cookie" 换行,&分割
# 本地网络抓取cookie，请勿异地抓
# cron: 20 8 * * *
# new Env('恩山无线论坛');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wy_rigth"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

def get_header(cookie):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Windows\"",
        'X-Requested-With': "XMLHttpRequest",
        'sec-ch-ua': "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
        'sec-ch-ua-mobile': "?0",
        'Origin': "https://www.right.com.cn",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://www.right.com.cn/forum/erling_qd-sign_in.html",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'Cookie': cookie
    }
    return header

def index(cookie, session):
    url = 'https://www.right.com.cn/forum/'
    header = get_header(cookie)
    try:
        response = session.get(url=url, headers=header)
        info = response.text
        pattern = re.compile(r'name="formhash" value="(.*?)"')
        matches = pattern.findall(response.text)
        if "退出" in info:
            pr("登陆成功")
            time.sleep(3)
            sign(cookie, matches[0], session)
            time.sleep(3)
            my(cookie, session)
        else:
            pr("登录失败")
    except Exception as e:
        pr(e)

def sign(cookie, formhash, session):
    url = "https://www.right.com.cn/forum/plugin.php"
    params = {
        'id': "erling_qd:action",
        'action': "sign"
    }
    payload = {
        'formhash': formhash
    }
    try:
        header = get_header(cookie)
        response = session.post(url, params=params, data=payload, headers=header)
        info = json.loads(response.text)
        if info.get("success"):
            pr(f"签到成功，已签到{info.get('continuous_days')}天")
        else:
            pr("签到失败")
    except Exception as e:
        pr(e)

def my(cookie, session):
    url = "https://www.right.com.cn/forum/home.php"
    header = get_header(cookie)
    try:
        response = session.get(url=url, headers=header)
        pattern = re.compile(r'title="访问我的空间">(.*?)</a>')
        pattern2 = re.compile(r'<em>积分</em>(.*?)</li>')
        pattern3 = re.compile(r'<em>恩山币</em>(.*?) 币</li>')

        matches = pattern.findall(response.text)
        matches1 = pattern2.findall(response.text)
        matches2 = pattern3.findall(response.text)
        if not matches or not matches1 or not matches2:
            pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
            return

        pr("用户名：" + matches[0] + " 积分：" + matches1[0] + " 恩山币：" + matches2[0])
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
            send("恩山无线论坛", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()
