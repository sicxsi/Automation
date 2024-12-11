
# name: 白鲸鱼回收
# Author: sicxs
# Date: 2024-11-6
# 微信小程序
# export wx_bjyhs="auth#username" 
# 抓小程序auth和username值
# 多号 @,&分割 
# cron: 25 8 * * *
# new Env('白鲸鱼回收');
import requests
import os,json,sys
import time,re
import config

def userinfo(s_auth,s_username): #登录信息
    url = f"https://www.52bjy.com/api/app/user.php?action=userinfo&auth={s_auth}&username={s_username}"
    header = {
        "authority": "www.52bjy.com",
        "method": "GET",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11437",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wxc525caf8e3a9e434/305/page-frame.html",
        }
    data = {
        "action": "userinfo",
        "auth": s_auth,
        "username": s_username,
        }
    response = requests.get(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    try:
       if  info['isSucess']:
            print(f"用户名：{info['data']['truename']}")
            time.sleep(3)
            qiandao(s_auth,s_username)
       else:
            print("获取用户信息失败")
            print(info)
    except Exception as e:
          
          print("你的账号可能到期了")  
def qiandao(s_auth,s_username): #签到
    url = f"https://www.52bjy.com/api/app/user.php?action=qiandao&auth={s_auth}&username={s_username}"
    header = {
        "authority": "www.52bjy.com",
        "method": "GET",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11437",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wxc525caf8e3a9e434/305/page-frame.html",
        }
    data = {
        "action": "userinfo",
        "auth": s_auth,
        "username": s_username,
        }
    response = requests.get(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    try:
       if  info['isSucess']:
            print(f"签到成功")
       else:
            print(info['message'])
    except Exception as e:
          
          print("你的账号可能到期了")  

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
            userinfo(list[0], list[1])
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错")    

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
       
 sicxs()  
