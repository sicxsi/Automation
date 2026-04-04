
# name: 音乐磁场
# Author: sicxs
# Date: 2024-11-2
# export wy_hifiti="cookie"  换行,&分割
# cron: 11 8 * * *
# new Env('音乐磁场');

import requests
import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wy_hifiti"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]


def get_header(cookie):
   header = {
        "authority":"www.hifiti.com",
        "method":"POST",
        "path":"/sg_sign.htm",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "referer":"https://www.hifiti.com/sg_sign.htm",
        "cookie":cookie
    }
   return header

def index(cookie,session): #验证登录
     url = 'https://www.hifiti.com/my.htm'
     header = get_header(cookie)
     try:
        response = session.get(url=url,headers=header)
        info = response.text
        if "用户登录" in info:
         pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
   
        else:
         pr("登录成功")
         sing(cookie,session)  
     except Exception as e:
          pr(e)
def sing(cookie,session):#验证是否签到
     url = 'https://www.hifiti.com/sg_sign.htm'
     header = get_header(cookie)
     time.sleep(3)
     try:
        response = session.get(url=url,headers=header)

        info = response.text

        if "已签" in info:
           pr("您今天已经签到过了，请勿重复签到。")
           my(cookie,session)
        elif "签到" in info:
         sing1(cookie,session)
         time.sleep(3)
         my(cookie,session)

        else :
          pr("签到失败")

     except Exception as e:
          pr(e)
def sing1(cookie,session):#签到
     url = 'https://www.hifiti.com/sg_sign.htm'
     header = get_header(cookie)
     time.sleep(3)
     try:
       response = session.post(url=url,headers=header)
       s1 = response.status_code 
       if s1 == 200 :
          pr("签到成功")
       
       else:
           pr("失败")
          
     except Exception as e:
         pr(e)
def my(cookie,session):#查询信息
    url = 'https://www.hifiti.com/my-credits.htm'
    header = get_header(cookie)
    try:
       response = session.get(url=url,headers=header)
       info = response.text
       time.sleep(3)
       if "用户组" in info:
         pattern = re.compile(r'<span class="hidden-lg">(.*?)</span>')
         pattern2 = re.compile(r'金币</span></div><input type="text" class="form-control" readonly style="background-color:white;" value="(.*?)">')
         matches = pattern.findall(info)
         matches1 = pattern2.findall(info)
         if not matches or not matches1:
          pr("解析用户信息失败，可能页面结构变化")
          return    
         
         pr( "用户名：" + matches[0] + " 金币:" + matches1[0])
       else:
         pr("解析用户信息失败，可能页面结构变化或 cookie 无效") 

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
            send("音乐磁场", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()