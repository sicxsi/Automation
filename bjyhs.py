# name: 白鲸鱼回收
# Author: sicxs
# Date: 2024-11-6
# 微信小程序
# export wx_bjyhs="auth#username" 
# 抓小程序auth和username值
# 多号 换行,&分割 
# cron: 25 8 * * *
# new Env('白鲸鱼回收');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


env_name = "wx_bjyhs"

msg = []
# 请求配置
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

def get_header():
    header = {
        "authority": "www.52bjy.com",
        "method": "GET",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11437",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wxc525caf8e3a9e434/305/page-frame.html",
        }
    return header

def userinfo(auth,username,session): #登录信息
    url = f"https://www.52bjy.com/api/app/user.php?action=userinfo&auth={auth}&username={username}"
    header = get_header()
    data = {
        "action": "userinfo",
        "auth": auth,
        "username": username,
        }
    response = session.get(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = response.json()
    try:
       if  info['isSucess']:
            pr(f"用户名：{info['data']['truename']}")
            time.sleep(3)
            qiandao(auth,username,session)
            time.sleep(3)
            add_a(auth,username,session)
       else:
            pr("获取用户信息失败")
            pr(info)
    except Exception as e:

          pr("你的账号可能到期了")
def qiandao(auth,username,session): #签到
    url = f"https://www.52bjy.com/api/app/user.php?action=qiandao&auth={auth}&username={username}"
    header = get_header()
    data = {
        "action": "userinfo",
        "auth": auth,
        "username": username,
        }
    response = session.get(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = response.json()
    try:
       if  info['isSucess']:
            pr(f"签到成功")
       else:
            pr(info['message'])
    except Exception as e:

          pr("你的账号可能到期了")

def add_a(auth,username,session):

    url = "https://www.52bjy.com/api/app/club.php"

    yiyanurl = "https://api.sicxs.cn/wy/wenrou.php"
    response1 = session.get(url=yiyanurl)
    yiyan = response1.text
    data = {
    'action': "add",
    'gid': "293",
    'username': username,
    'title': "七嘴八舌",
    'content': yiyan,
    'thumb': "",
    'auth': auth,
    'appkey': "1f70a57fdf4061a7",
    'version': "2"
    }

    header = get_header()

    response = session.get(url=url,headers=header,params=data)
    response.encoding = "utf-8"
    info = response.json()
    if  info['isSucess']:
        pr(f"发帖成功，帖子ID：{yiyan} ")
    else:
        pr(info['message'])


# ====== 固定代码 ======
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
def pr(message):
    msg.append(message + "\n")
    print(message)
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
        try:
            print(f'\n----------- 账号【{i}/{total}】执行 -----------')
            parts = account.split("#")
            if len(parts) < 2:
                print("账号格式错误,请检查设置")
                continue
            session = create_session_with_retry()
            userinfo(parts[0], parts[1],session)
        except Exception as e:
            print(f"账号【{i}/{total}】执行出错：{e}")
        finally:
            send("白鲸鱼回收", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs() 
