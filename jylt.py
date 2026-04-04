# name: 精益论坛
# Author: sicxs
# Date: 2024-11-25
# export wy_jylt="cookie" &,换行分割
# cron: 20 8 * * *
# new Env('精益论坛');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wy_jylt"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]


def index(cookie, session): #登录
    url = "https://bbs.ijingyi.com/plugin.php"
    params = {
        'id': "dsu_paulsign:sign"
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'cache-control': "max-age=0",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'priority': "u=0, i",
        'Cookie': cookie,
    }
    response = session.get(url=url, headers=headers, params=params)
    response.encoding = "utf-8"
    info = response.text
    if "<em>登录</em></button></td>" in info:
        pr("cookie失效或错误")
    else:
        pr("账号登陆成功")  
        time.sleep(3)
        if "您今日已经签到" in info:
            url = "https://bbs.ijingyi.com/plugin.php"
            response = session.get(url=url, headers=headers)
            response.encoding = "utf-8"
            info = response.text
            pattern = re.compile(r'uid=(.*?)" target="_blank" title="访问我的空间">(.*?)</a>')
            matches = pattern.findall(info) 
            if not matches:
                pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
                return
            id = matches[0][0]
            pr("今日已完成签到,无需重复签到")
            infoo(id, headers, session)
            return
        pattern = re.compile(r'uid=(.*?)" target="_blank" title="访问我的空间">(.*?)</a>')
        pattern1 = re.compile(r'formhash=(.*?)">退出</a>')
        matches = pattern.findall(info) 
        matches1 = pattern1.findall(info)
        if not matches or not matches1:
            pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
            return
        pr(f"用户名: {matches[0][1]}")
        hash = matches1[0]
        id = matches[0][0]
        qiandao(hash, headers, session)
        time.sleep(3)
        infoo(id, headers, session)

def infoo(id, headers, session): #我的信息
    url = f"https://bbs.ijingyi.com/home.php?mod=space&uid={id}&do=profile&from=space"
    response = session.get(url=url, headers=headers)
    response.encoding = "utf-8"
    info = response.text
    pattern = re.compile(r'<li><em>积分</em>(.*?)</li>')
    pattern1 = re.compile(r'<li><em>精币</em>(.*?)</li>')
    pattern2 = re.compile(r'<li><em>荣誉</em>(.*?)</li>')
    pattern3 = re.compile(r'<h2>该会员签到详情</h2><p>累计签到总天数 : <b>(.*?)</b> 天</p><p>连续签到天数 : <b>(.*?)</b> 天</p><p>本月签到天数 : <b>(.*?)</b> 天')
    matches = pattern.findall(info) 
    matches1 = pattern1.findall(info) 
    matches2 = pattern2.findall(info) 
    matches3 = pattern3.findall(info) 
    if not matches or not matches1 or not matches2 or not matches3:
        pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
        return
    pr(f"积分: {matches[0]} 精币: {matches1[0]} 荣誉: {matches2[0]} 签到累计天数: {matches3[0][0]} 本月签到天数: {matches3[0][2]} 连续签到天数: {matches3[0][1]} ")

def qiandao(hash, headers, session):
    url = "https://bbs.ijingyi.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"
    data = {
        'formhash': hash,
        "submit": "1",
        "targerurl": "",
        "todaysay": "",
        "qdxq": "kx"
    }
    try:
        response = session.post(url=url, headers=headers, data=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if info['status'] == 1:
            pr(f"签到成功,连续签到 {info['data']['mdays']} 天")
        else:
            pr(f"签到失败: {info}")  
    except Exception as e:
        pr(f"签到过程中发生未知错误: {str(e)}")   
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
            send("精益论坛", ''.join(msg))
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
  sicxs()
