# name: 葫芦侠三楼
# Author: sicxs
# Date: 2024-12-16
# export app_hlx="手机号#密码"
# 换行 & 分割 
# 功能:签到
# cron: 18 8 * * *
# new Env('葫芦侠三楼');

import requests
import os,json,sys
import time,re
import random,hashlib
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "app_hlx"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

def index(username, password, session): #登录信息
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    sign = "account" + username + "device_code[d]b305cc73-8db8-4a25-886f-e73c502b1e99password" + password_md5 + "voice_codefa1c28a5b62e79c3e63d9030b6142e4b"
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    url = "http://floor.huluxia.com/account/login/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.3.0.7.1&versioncode=367&market_id=tool_web&_key=&device_code=%5Bd%5Db305cc73-8db8-4a25-886f-e73c502b1e99&phone_brand_type=VO"
    data = {
        'account': username,
        'login_type': '2',
        'password': password_md5,
        'sign': sign
    }
    headers = {"User-Agent": "okhttp/3.8.1"}
    response = session.post(url=url, data=data, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    key = info['_key']
    pr(f"登陆成功，用户名：{info['user']['nick']}")
    app_qiandao(key, session)

def app_qiandao(key, session): #签到
    pr("开始执行签到任务...")
    id_list = app_list(session)
    for i in id_list:
        timestamp = int(time.time() * 1000)
        sign = "cat_id" + str(i[0]) + "time" + str(timestamp) + "fa1c28a5b62e79c3e63d9030b6142e4b"
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        url = f"http://floor.huluxia.com/user/signin/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.3.0.7.1&versioncode=20141475&market_id=floor_web&_key={key}&phone_brand_type=OP&cat_id={i[0]}&time={timestamp}"
        headers = {
            "Accept-Encoding": "identity",
            "Host": "floor.huluxia.com",
            'User-Agent': 'okhttp/3.8.1',
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "37"
        }
        data = {"sign": sign}
        time.sleep(random.randint(15, 20))
        response = session.post(url=url, headers=headers, data=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if 1 == info['status']:
            pr(f"{i[1]} 签到成功，获得{info['experienceVal']}点经验")
        else:
            pr(f"{i[1]},{info['msg']}")
    pr("签到完成")

def app_list(session): #板块列表
    result = []
    url = f"https://floor.huluxia.com/category/list/ANDROID/4.2.3?"
    headers = {
        "Host": "floor.huluxia.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    response = session.get(url=url, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['status'] == 1:
        for i in info['categories']:
            id = i['categoryID']
            title = i['title']
            result.append((id, title))
    else:
        pr("获取失败")
    return result

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
            send("葫芦侠三楼", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()