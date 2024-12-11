# name: 美的会员
# Author: sicxs
# Date: 2024-11-27
# export wx_md="cookie"  抓get请求的cookie
# 多账号用 &,@换行分割
# 功能：签到，早起打卡报名，早起打卡
# cron: 35 6,10 * * *
# new Env('美的会员');
import config

import requests
import re,time
import os,sys,json
def get_header(Cookie): #请求头
    headers = {
        "Host": "mvip.midea.cn",
        "Connection": "keep-alive",
        "xweb_xhr": "1",
        "Cookie": Cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11477",
        "Content-Type": "application/json",
        "Referer": "https://servicewechat.com/wx03925a39ca94b161/453/page-frame.html",
        }
    return headers
def index(Cookie):#登录信息
    url = "https://mvip.midea.cn/next/mucuserinfo/getmucuserinfo"
    header = get_header(Cookie)
    request = requests.get(url,headers=header)
    request.encoding = "utf-8"
    try:
     info = json.loads(request.text)
     if info['errcode'] == 0:
        print(f"登陆成功，用户名；{info['data']['userinfo']['NickName']}")
        qiandao(Cookie)
        daka_a(Cookie)
        daka_b(Cookie)
    except:
      print(request.text)
def qiandao(Cookie): #签到
    url = "https://mvip.midea.cn/my/score/create_daily_score"
    header = get_header(Cookie)
    request = requests.get(url,headers=header)
    time.sleep(3)
    request.encoding = "utf-8"
    try:
     info = json.loads(request.text)
     if info['errcode'] == 0:
        print("签到成功")
    except:
      print("签到失败")
def daka_a(Cookie): #打卡   
    print("执行早起打卡报名")
    url = "https://mvip.midea.cn/next/early_clock_r/applyforearlyclock"
    header = get_header(Cookie)
    request = requests.get(url,headers=header)
    time.sleep(3)
    request.encoding = "utf-8"
    try:
     info = json.loads(request.text)
     if info['errcode'] == 0:
        print("报名打卡成功")
     else:  
        print(f"报名打卡失败,{info['errmsg']}")   
    except:
      print("打卡失败")     

def daka_b(Cookie):#早起打卡
    print("执行早起打卡")
    url = "https://mvip.midea.cn/next/early_clock_r/clockforearlyclock"
    header = get_header(Cookie)
    request = requests.get(url,headers=header)
    time.sleep(3)
    request.encoding = "utf-8"
    try:
     info = json.loads(request.text)
     if info['errcode'] == 0:
        print("打卡成功")
     else:  
        print(f"打卡失败,{info['errmsg']}")   
    except:
      print("打卡失败")

def sicxs():
    try:
        env_cookie = os.environ.get("wx_md")
        si_cookie = getattr(config, 'wx_md', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_md='' 或在 config.py 中设置 wx_md")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_md='' 或在 config.py 中设置 wx_md")
        sys.exit()
    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        try:
            index(list_cookie_i)
        except Exception as e:
            print(f"执行账号【{i + 1}】时发生错误: {e}")

    print(f'\n-----------  执 行  结 束 -----------')
if __name__ == '__main__':
  sicxs()