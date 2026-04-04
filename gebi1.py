# name: 隔壁网
# Author: sicxs
# Date: 2024-11-4
# export wy_gebi="cookie" 换行,& 分割
# cron: 25 8 * * *
# new Env('隔壁网');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []
env_name = "wy_gebi"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]

def get_header(cookie):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'cache-control': "max-age=0",
        'origin': "https://gebi1.com",
        'referer': "https://gebi1.com/portal.php",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'priority': "u=0, i",
        'cookie': cookie,
    }
    return headers

def index(cookie, session):  # 登录
    url = "https://www.gebi1.com"
    header = get_header(cookie)
    response = session.get(url, headers=header)
    if "登录后即可体验更多功能" in response.text:
        pr("cookie失效或错误")
    else:
        pattern = re.compile(r"discuz_uid = '(.*?)',")
        pattern1 = re.compile(r'访问我的空间" class="kmname">(.*?)</a>')
        pattern2 = re.compile(r'formhash=(.*?)&amp;')
        matches = pattern.findall(response.text)
        matches1 = pattern1.findall(response.text)
        matches2 = pattern2.findall(response.text)
        if not matches or not matches1 or not matches2:
            pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
            return
        pr(f"登录成功，用户名：{matches1[0]}")
        time.sleep(2)
        uid = matches[0]
        formhash = matches2[0]
        sign(uid, cookie, formhash, session)

def sign(uid, cookie, formhash, session):
    url = f"https://www.gebi1.com/plugin.php?id=k_misign:sign&operation=qiandao&format=button&formhash={formhash}&inajax=1&ajaxtarget=midaben_sign"
    header = get_header(cookie)
    try:
        response = session.get(url, headers=header)
        info = response.text
        if "签到成功" in info:
            pr("签到成功")
            time.sleep(5)
            my(uid, cookie, session)
        elif "今日已签" in info:
            pr("今日已签到过了")
            my(uid, cookie, session)
        elif "登录后" in info:
            pr("cookie失效或错误")
    except Exception as e:
        pr(e)

def my(uid, cookie, session):
    url = f"https://gebi1.com/home.php?mod=space&uid={uid}&do=profile&from=space"
    header = get_header(cookie)
    try:
        response = session.get(url, headers=header)
        info = response.text
        pattern = re.compile(r'<span>(.*?)</span>积分</a>')
        pattern1 = re.compile(r'kmicon1"><span>(.*?)</span>经验值</a>')
        pattern2 = re.compile(r'<span>(.*?)</span>丝瓜</a>')
        pattern3 = re.compile(r'<span>(.*?)</span>贡献</a>')

        matches = pattern.findall(info)
        matches1 = pattern1.findall(info)
        matches2 = pattern2.findall(info)
        matches3 = pattern3.findall(info)
        if not matches or not matches1 or not matches2 or not matches3:
            pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
            return
        pr(f"丝瓜：{matches2[0]},经验：{matches1[0]},贡献：{matches3[0]},积分：{matches[0]}")
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
            send("隔壁NAS网", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs()
