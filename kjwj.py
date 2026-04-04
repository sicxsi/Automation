# name: 科技玩家
# Author: sicxs
# Date: 2024-11-4
# export wy_kjwj="账号#密码" 换行，&分割 
# cron: 15 8 * * *
# new Env('科技玩家');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wy_kjwj"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

def get_headers(authorization=None):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "origin": "https://www.kejiwanjia.net",
        "referer": "https://www.kejiwanjia.net/",
    }
    if authorization:
        headers["authorization"] = f"Bearer {authorization}"
    return headers
def logn(zhanghao, mima, session):
    url = "https://www.kejiwanjia.net/wp-json/jwt-auth/v1/token"
    header = get_headers()
    data = {
        "nickname": "",
        "username": zhanghao,
        "password": mima,
        "code": "",
        "img_code": "",
        "invitation_code": "",
        "token": "",
        "smsToken": "",
        "luoToken": "",
        "confirmPassword": "",
        "loginType": ""
    }
    try:
        r = session.post(url=url, headers=header, data=data, timeout=10)
        r.encoding = "utf-8"
        try:
            info = r.json()
        except Exception as e:
            body = r.text if hasattr(r, 'text') else ''
            pr(f"登录接口JSON解析失败: {e}，响应摘要: {body[:500]}")
            return None
        if isinstance(info, dict) and 'token' in info:
            return info['token']
        pr(f"登录失败: {info.get('message', info)}")
        return None
    except Exception as e:
        pr(f"登录请求异常: {e}")
        return None


def getUserInfo(authorization, session):  # 我的信息
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/getUserInfo"
    header = get_headers(authorization)
    try:
        r = session.post(url=url, headers=header, timeout=10)
        r.encoding = "utf-8"
        info = r.json()
        pr(f"用户名: {info.get('user_data', {}).get('name')}")
        time.sleep(3)
        getUserMission(authorization, session)
        time.sleep(5)
        userMission(authorization, session)
    except Exception as e:
        pr(f"获取用户信息异常: {e}")

def getGoldList(authorization, session):  # 积分查询
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/getGoldList"
    header = get_headers(authorization)
    try:
        r = session.post(url=url, headers=header, timeout=10)
        r.encoding = "utf-8"
        info = r.json()
        if info.get('data'):
            pr(f"最近一次签到：{info['data'][0]['date']},获得积分；{info['data'][0]['no']},总积分：{info['data'][0]['total']}")
    except Exception as e:
        pr(f"获取积分异常: {e}")

def getUserMission(authorization, session):  # 更新签到
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/getUserMission"
    header = get_headers(authorization)
    try:
        r = session.post(url=url, headers=header, timeout=10)
        if r.status_code == 200:
            pr("正在初始签到，请稍等。")
    except Exception as e:
        pr(f"检查签到状态异常: {e}")

def userMission(authorization, session):  # 签到
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/userMission"
    header = get_headers(authorization)
    try:
        r = session.post(url=url, headers=header, timeout=10)
        r.encoding = "utf-8"
        info = r.json()
        if isinstance(info, dict) and "message" in info:
            pr("你的authorization可能过期了，请检查。")
        elif isinstance(info, dict) and "credit" in info:
            pr(f"恭喜您，签到获得,{info['credit']}积分")
            time.sleep(5)
            getGoldList(authorization, session)
        else:
            pr("请勿重复签到")
            time.sleep(5)
            getGoldList(authorization, session)
    except Exception as e:
        pr(f"签到异常: {e}")

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
            token = logn(parts[0], parts[1], session)
            if not token:
                pr("登录失败，跳过该账号")
                continue
            getUserInfo(token, session)
        except Exception as e:
            print(f"账号【{i}/{total}】执行出错：{e}")
        finally:
            send("科技玩家", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
    sicxs()