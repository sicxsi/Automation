# name: 回收猿回收
# Author: sicxs
# Date: 2024-11-8
# 微信小程序
# export wx_hsyhs="auth#username" 
# 抓小程序 -> 我的 auth和username值
# 多号 换行,&分割 
# cron: 16 8 * * *
# new Env('回收猿回收');

import requests
import os,json,sys
import time,re
import random,hashlib
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wx_hsyhs"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

# md5 = "action=user&appkey=1079fb245839e765&merchant_id=2&method=center&username={wx_username}UppwYkfBlk"
# md5_hash = hashlib.md5(md5.encode('utf-8')).hexdigest().upper().lower()
# print(md5_hash) 
# sign为固定值 
def index(wx_auth, wx_username, session): #登录信息
    url = f"https://www.52bjy.com/api/app/user.php?action=userinfo&app=hsywx&appkey=1079fb245839e765&auth={wx_auth}&merchant_id=2&username={wx_username}"
    header = {
        "authority": "www.52bjy.com",
        "method": "GET",
        "path": f"/api/app/user.php?action=userinfo&app=hsywx&appkey=1079fb245839e765&auth={wx_auth}&merchant_id=2&username={wx_username}",
        "scheme": "https",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wxadd84841bd31a665/91/page-frame.html"
    }
    response = session.get(url=url, headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['isSucess']:
        pr(f"登陆成功，用户名：{info['data']['nickname']}")
        md5 = f"action=user&app=hsywx&appkey=1079fb245839e765&merchant_id=2&method=qiandao&username={wx_username}&version=2UppwYkfBlk"
        wx_sign = hashlib.md5(md5.encode('utf-8')).hexdigest().upper().lower()
        qiandao(wx_username, wx_sign, session)
    else:
        pr(info['message'])

def qiandao(wx_username, wx_sign, session): #签到
    url = f"https://www.52bjy.com/api/app/hsy.php?action=user&app=hsywx&appkey=1079fb245839e765&merchant_id=2&method=qiandao&username={wx_username}&version=2&sign={wx_sign}"
    header = {
        "authority": "www.52bjy.com",
        "method": "POST",
        "path": f"/api/app/hsy.php?action=user&app=hsywx&appkey=1079fb245839e765&merchant_id=2&method=qiandao&username={wx_username}&version=2",
        "scheme": "https",
        "envconnection": "test",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11437",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wxadd84841bd31a665/91/page-frame.html",
    }
    response = session.post(url=url, headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    md5 = f"action=user&appkey=1079fb245839e765&merchant_id=2&method=center&username={wx_username}UppwYkfBlk"
    wx_sign_info = hashlib.md5(md5.encode('utf-8')).hexdigest().upper().lower()
    if info['isSucess']:
        pr(info['message'])
        pr(f"签到红包：{info['data']['qiandao_award']}元，签到天数：{info['data']['double_award_days']}")
        signinfo(wx_username, wx_sign_info, session)
    else:
        pr(info['message'])
        signinfo(wx_username, wx_sign_info, session)

def signinfo(wx_username, wx_sign_info, session): #红包
    url = f"https://www.52bjy.com/api/app/hsy.php?action=user&appkey=1079fb245839e765&merchant_id=2&method=center&username={wx_username}&sign={wx_sign_info}"
    header = {
        "authority": "www.52bjy.com",
        "method": "GET",
        "path": f"/api/app/hsy.php?action=user&appkey=1079fb245839e765&merchant_id=2&method=center&username={wx_username}&sign={wx_sign_info}",
        "scheme": "https",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wxadd84841bd31a665/91/page-frame.html"
    }
    response = session.get(url=url, headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['isSucess']:
        pr(f"红包总额：{info['data']['yuanbao']}元")
    else:
        pr(info)

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
            index(parts[0], parts[1], session)
        except Exception as e:
            print(f"账号【{i}/{total}】执行出错：{e}")
        finally:
            send("回收猿回收", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()
