# name: 通信人家园
# Author: sicxs
# Date: 2024-11-25
# export wy_txrjy="账号#密码" &,换行分割 
# cron: 20 8 * * *
# new Env('通信人家园');

import requests
import re,time
import os,sys
from notify import send

def pr(message):
    msg.append(message + "\n" )
    print(message)

msg = []

s = requests.session()
def get_logn(name, password): #登录
    url = "https://www.txrjy.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes"
    header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Origin": "https://www.txrjy.com",
            "Referer": "https://www.txrjy.com/forum.php",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            }
    data = {
        "username": name,
        "password": password,
        "quickforward": "yes",
        "handlekey": "ls"
        }
    response = s.post(url=url,headers=header,data=data)
    info = response.text
    if "登录失败" in info:
     pr("登录失败")
    else:
     pr("登陆成功") 
     cookie = response.cookies
     index(cookie)
def index(cookie): #我的信息
     url = "https://www.txrjy.com/home.php?mod=spacecp&ac=credit&showcredit=1"
     header = {
        "Host": "www.txrjy.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.txrjy.com/forum.php",
        }
     response = s.get(url=url,headers=header,cookies=cookie)
     info = response.text
     time.sleep(3)
     pattern = re.compile(r'<em> 家园分:</em>(.*?)  &nbsp; </li>')
     pattern1 = re.compile(r'<li><em> 经验:</em>(.*?) </li>')
     pattern2 = re.compile(r'<em>积分:</em>(.*?) <span class="xg1">')
     pattern3 = re.compile(r'title="访问我的空间">(.*?)</a></strong>')
     matches = pattern.findall(info) 
     matches1 = pattern1.findall(info) 
     matches2 = pattern2.findall(info) 
     matches3 = pattern3.findall(info) 
     if not matches or not matches1 or not matches2 or not matches3:
          pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
          return
     pr(f"用户名: {matches3[0]} 积分: {matches2[0]} 经验: {matches1[0]} 家园分: {matches[0]}")


def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')
    try:
        env_cookie = os.environ.get("wy_txrjy")
        si_cookie = getattr(config, 'wy_txrjy', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wy_txrjy='' 或在 config.py 中设置 wy_txrjy =")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wy_txrjy='' 或在 config.py 中设置 wy_txrjy =")
        sys.exit()

    list_cookie = [c for c in re.split(r'\n|&', cookies) if c.strip()]
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            pr(f"账号【{i + 1}】开始执行：")
            list = list_cookie_i.split("#")
            get_logn(list[0], list[1])
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错：账号密码错误，或者账号被封禁，请检查后重试！")    
        finally:   
           send("通信人家园", ''.join(msg))
           msg.clear()  
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':   
   sicxs() 