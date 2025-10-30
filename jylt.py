# name: 精益论坛
# Author: sicxs
# Date: 2024-11-25
# export wy_jylt="cookie" &,@换行分割
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
    url = "https://bbs.ijingyi.com"
    header = {
        "authority": "bbs.ijingyi.com",
        "method": "GET",
        "path": "/",
        "scheme": "https",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "cookie": cookie,
        }
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = response.text
    if "<em>登录</em></button></td>" in info:
        pr("cookie失效或错误")
    else:
        pr("账号登陆成功")  
        time.sleep(3)
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
        qiandao(cookie,hash)
        time.sleep(3)
        infoo(cookie,id)

def infoo(cookie,id):#我的信息
    url = f"https://bbs.ijingyi.com/home.php?mod=space&uid={id}&do=profile&from=space"
    header = {
        "authority": "bbs.ijingyi.com",
        "method": "GET",
        "path": f"/home.php?mod=space&uid={id}&do=profile&from=space",
        "scheme": "https",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "cookie": cookie,
        }
    
    response = requests.get(url=url,headers=header)
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

def qiandao(cookie,hash):#签到
    url = f"https://bbs.ijingyi.com/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1"
    header = {
        "authority": "bbs.ijingyi.com",
        "method": "POST",
        "path": f"/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1",
        "scheme": "https",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "cookie": cookie,
        }
    data = {'formhash':hash,"submit": "1","targerurl": "","todaysay": "","qdxq": "kx"}
    response = requests.post(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    if "您今日已经签到" in response.text:
        pr("您今日已经签到过了")
    elif "签到成功" in response.text:
       pr("签到成功")
    else:
        pr(response.text)

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
    list_cookie = re.split(r'\n|&|@', cookies)
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
