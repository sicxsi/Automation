# name: 精益论坛
# Author: sicxs
# Date: 2024-11-25
# export wy_jylt="cookie" &,换行分割
# cron: 20 8 * * *
# new Env('精益论坛');

import requests
import re,time
import os,sys,json
from notify import send

def pr(message):
    msg.append(message + "\n" )
    print(message)

msg = []
def index(cookie): #登录
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

    response = requests.get(url=url,headers=headers,params=params)
    response.encoding = "utf-8"
    info = response.text
    if "<em>登录</em></button></td>" in info:
        pr("cookie失效或错误")
    else:
        pr("账号登陆成功")  
        time.sleep(3)
        if "您今日已经签到" in info:
            url = "https://bbs.ijingyi.com/plugin.php"
            response = requests.get(url=url,headers=headers)
            response.encoding = "utf-8"
            info = response.text
            pattern = re.compile(r'uid=(.*?)" target="_blank" title="访问我的空间">(.*?)</a>')
            matches = pattern.findall(info) 
            if not matches :
               pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
               return
            id = matches[0][0]
            pr("今日已完成签到,无需重复签到")
            infoo(id,headers)
            return
        pattern = re.compile(r'uid=(.*?)" target="_blank" title="访问我的空间">(.*?)</a>')
        pattern1 = re.compile(r'formhash=(.*?)">退出</a>')
        matches = pattern.findall(info) 
        matches1 = pattern1.findall(info)
        if not matches or not matches1 :
          pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
          return
        pr(f"用户名: {matches[0][1]}")
        hash = matches1[0]
        id = matches[0][0]
        qiandao(hash, headers)
        time.sleep(3)
        infoo(id,headers)

def infoo(id,headers):#我的信息
    url = f"https://bbs.ijingyi.com/home.php?mod=space&uid={id}&do=profile&from=space"
    response = requests.get(url=url,headers=headers)
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

def qiandao(hash, headers):
    url = "https://bbs.ijingyi.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"
    data = {
        'formhash': hash,
        "submit": "1",
        "targerurl": "",
        "todaysay": "",
        "qdxq": "kx"
    }
    
    try:
        response = requests.post(url=url, headers=headers, data=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
  
        if info['status'] == 1:
            pr(f"签到成功,连续签到 {info['data']['mdays']} 天")
        else:
            pr(f"签到失败: {info}")  
    except Exception as e:
        pr(f"签到过程中发生未知错误: {str(e)}")   

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')
    try:
        env_cookie = os.environ.get("wy_jylt")
        si_cookie = getattr(config, 'wy_jylt', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wy_jylt='' 或在 config.py 中设置 wy_jylt")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wy_jylt='' 或在 config.py 中设置 wy_jylt")
        sys.exit()
    list_cookie = [c for c in re.split(r'\n|&', cookies) if c.strip()]
    total_cookies = len(list_cookie)
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        pr(f"账号【{i + 1}】开始执行：")
        try:
            index(list_cookie_i)
        except Exception as e:
            pr(f"执行账号【{i + 1}】时发生错误: {e}")
        finally:
          send("精益论坛", ''.join(msg))
          msg.clear()
    print(f'\n-----------  执 行  结 束 -----------')


if __name__ == '__main__':
  sicxs()
