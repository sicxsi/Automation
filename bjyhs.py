
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
from notify import send

def pr(message):
    msg.append(message + "\n")
    print(message)

msg = []


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
            pr(f"用户名：{info['data']['truename']}")
            time.sleep(3)
            qiandao(s_auth,s_username)
            time.sleep(3)
            add_a(s_auth,s_username)
       else:
            pr("获取用户信息失败")
            pr(info)
    except Exception as e:

          pr("你的账号可能到期了")
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
            pr(f"签到成功")
       else:
            pr(info['message'])
    except Exception as e:

          pr("你的账号可能到期了")

def add_a(s_auth,s_username):

    url = "https://www.52bjy.com/api/app/club.php"

    yiyanurl = "https://api.sicxs.cn/wy/wenrou.php"
    response1 = requests.get(url=yiyanurl)
    yiyan = response1.text
    data = {
    'action': "add",
    'gid': "293",
    'username': s_username,
    'title': "七嘴八舌",
    'content': yiyan,
    'thumb': "",
    'auth': s_auth,
    'appkey': "1f70a57fdf4061a7",
    'version': "2"
    }

    header = {
        "authority": "www.52bjy.com",
        "method": "GET",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11437",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wxc525caf8e3a9e434/305/page-frame.html",
        }

    response = requests.get(url=url,headers=header,params=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if  info['isSucess']:
        pr(f"发帖成功，帖子ID：{yiyan} ")
    else:
        pr(info['message'])

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')
    try:
        env_cookie = os.environ.get("wx_bjyhs")
        si_cookie = getattr(config, 'wx_bjyhs', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_bjyhs'' 或在 config.py 中设置  wx_bjyhs =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export  wx_bjyhs'' 或在 config.py 中设置  wx_bjyhs =")
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
