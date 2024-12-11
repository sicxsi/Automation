# name: 点点兼职
# Author: sicxs
# Date: 2024-11-7
# 微信小程序
# export wx_ddjz="api_auth_code#api_auth_uid"  多账户@,&分割 
# 微信抓api_auth_code和api_auth_uid的注意不要写反
# 请自己提现，秒到
# cron: 15 8 * * *
# new Env('点点兼职');

import requests
import os,sys,time
import json,re
import config

def index(api_auth_code,api_auth_uid):#登录信息
    
    url= f"https://mili.shensemiao.com/index.php?v=1&appid=4&appsecret=PHPCMF19F5DF41B263B&api_auth_code={api_auth_code}&api_auth_uid={api_auth_uid}&s=yhxcx&c=home&m=member_index"
    header = {
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
          "Content-Type": "application/x-www-form-urlencoded",
          "referer": "https://servicewechat.com/wxec97c88d99c5d385/5/page-frame.html",
        }
    response = requests.post(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 ==info['code']:
        print(f"用户名：{info['data']['member']['name']}")
        time.sleep(3)
        qiandaoinfo(api_auth_code,api_auth_uid)
        time.sleep(16)
        ddinfo(api_auth_code,api_auth_uid)
    else:
        print("登录失败")   

def qiandao(api_auth_code,api_auth_uid,id):#签到
    url = f"https://mili.shensemiao.com/index.php?v=1&appid=4&appsecret=PHPCMF19F5DF41B263B&api_auth_code={api_auth_code}&api_auth_uid={api_auth_uid}&s=member&app=Yhxcx&c=qd&m=sign_in"
    header = {
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
          "Content-Type": "application/x-www-form-urlencoded",
          "referer": "https://servicewechat.com/wxec97c88d99c5d385/5/page-frame.html",
        }

    data={
            "id": id,
            "fblx": "1",
            "wcs": "0",
            "theway": "signin",
            "search": "1"
          }
    
    response = requests.post(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 ==info['code']:
        print("看视频成功，看下一个")
    elif 0 ==info['code']:
        print("你已经签到过了，请勿重复签到。")  
    else:
        print("失败")   

def qiandao1(api_auth_code,api_auth_uid,id):#签到1
    url = f"https://mili.shensemiao.com/index.php?v=1&appid=4&appsecret=PHPCMF19F5DF41B263B&api_auth_code={api_auth_code}&api_auth_uid={api_auth_uid}&s=member&app=Yhxcx&c=qd&m=sign_in"
    header = {
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
          "Content-Type": "application/x-www-form-urlencoded",
          "referer": "https://servicewechat.com/wxec97c88d99c5d385/5/page-frame.html",
        }

    data={
            "id": id,
            "fblx": "1",
            "wcs": "1",
            "theway": "signin",
            "search": "1"
          }
    
    response = requests.post(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 ==info['code']:
        print("看视频成功，查询是否签到成功")
    elif 0 ==info['code']:
        print("你已经签到过了，请勿重复签到。")     
    else:
        print("失败")   

def qiandao2(api_auth_code,api_auth_uid,id):#签到成功判断
    
    url = f"https://mili.shensemiao.com/index.php?v=1&appid=4&appsecret=PHPCMF19F5DF41B263B&api_auth_code={api_auth_code}&api_auth_uid={api_auth_uid}&s=member&app=Yhxcx&c=qd&m=sign_in"
    header = {
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
          "Content-Type": "application/x-www-form-urlencoded",
          "referer": "https://servicewechat.com/wxec97c88d99c5d385/5/page-frame.html",
        }
    data = {
          "id": id,
          "fblx": "1",
          "wcs": "1",
          "theway": "signin",
          "search": "1"
        }
    response = requests.post(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 ==info['code']:
        print(info['msg'])
    else:
        print("失败")   
        print(info)

def qiandaoinfo(api_auth_code,api_auth_uid):#初始化签到
    url = f"https://mili.shensemiao.com/index.php?v=1&appid=4&appsecret=PHPCMF19F5DF41B263B&&api_auth_code={api_auth_code}&api_auth_uid={api_auth_uid}&&s=member&app=yhxcx&c=qd&m=sign_in"
    header = {
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
          "Content-Type": "application/x-www-form-urlencoded",
          "referer": "https://servicewechat.com/wxec97c88d99c5d385/5/page-frame.html",
        }

    response = requests.post(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)

    if 1 ==info['code']:
        if "llurl" in info['data']:
            wx_id = info['data']['llurl']
            pattern = re.compile(r"&id=(\d+)")
            matches = pattern.findall(str(wx_id))
            wx_iduid = matches[0]
        else:
            wx_iduid = "1010"
            print("你已经签到过了")
    else:
        print(info)   
    return wx_iduid
def ddinfo(api_auth_code,api_auth_uid):#获取兼职id


    
    url = f"https://mili.shensemiao.com/index.php?v=1&appid=4&appsecret=PHPCMF19F5DF41B263B&&api_auth_code={api_auth_code}&api_auth_uid={api_auth_uid}&&s=Yhxcx&c=home&m=fb_list"
    header = {
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
          "Content-Type": "application/x-www-form-urlencoded",
          "referer": "https://servicewechat.com/wxec97c88d99c5d385/5/page-frame.html",
        }

    response = requests.post(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)

    if 1 ==info['code']:
        id1 = qiandaoinfo(api_auth_code,api_auth_uid)
        print(f"本次浏览兼职的的ID是{id1}")
        qiandao(api_auth_code,api_auth_uid,id1)
        time.sleep(16) 
        id2 = qiandaoinfo(api_auth_code,api_auth_uid)
        print(f"本次浏览兼职的的ID是{id2}")
        qiandao1(api_auth_code,api_auth_uid,id2)
        time.sleep(16) 
        qiandao2(api_auth_code,api_auth_uid,id2)
    else:
        print(info)   



def sicxs():
    try:
        env_cookie = os.environ.get("wx_ddjz")
        si_cookie = getattr(config, 'wx_ddjz', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_ddjz='' 或在 config.py 中设置 wx_ddjz =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_ddjz='' 或在 config.py 中设置 wx_ddjz =")
        sys.exit()

    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            list = list_cookie_i.split("#")
            index(list[0], list[1])
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错")    

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
 sicxs()