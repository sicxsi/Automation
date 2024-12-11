# name: 植物星球
# Author: sicxs
# Date: 2024-11-27
# export wx_zwxq="账号#密码" 
# &,@换行分割 
# 功能:签到，浏览任务
# cron: 20 8 * * *
# new Env('植物星球');

import requests
import re,time
import os,sys,json
import hashlib
import config

s = requests.session()
def index(useradmin,password):#登录
    url = 'https://api.pftp2012.com/api/Member/Login'
    header = {
        "Host": "api.pftp2012.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11477",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://servicewechat.com/wxd7296b6421fc974e/1/page-frame.html",
        } 

    data={
        "userName":useradmin,
        "userPwd": password,
        "channel": "40"
        }
    response = requests.post(url=url,headers=header,data=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)

    return(info['Data']['MemberInfo']['Token'])
def get_info(useradmin,password):#登录信息
    try:
     url = 'https://api.pftp2012.com/api/Member/GetMemberInfo?channel=40'
     Authorization = index(useradmin,password)
     header = {
        "Host": "api.pftp2012.com",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {Authorization}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11477",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://servicewechat.com/wxd7296b6421fc974e/1/page-frame.html",
        }
     response = s.get(url=url,headers=header)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     if info['Status']== 100:
        print(f"登陆成功,用户名:{info['Data']['MemberInfo']['MemberName']}")   
        get_qiandao(header)
        time.sleep(3)
        get_liulan(header)    
     else:
         print("登录失败")
    except: 
       print("登陆失败，请检查账号密码是否正确") 
def get_liulan(header):  #浏览任务
    print("正在开始浏览任务")
    url = 'https://api.pftp2012.com/api/Member/CompleteMemberMission'
    # 50 =实名认证给200
    # 60 =浏览任务2
    # 10 =浏览任务1
    type = ["10","60"]
    for i in type:
     data = {
        "type": i,
        "channel": "40"
        }
     response = s.post(url=url,headers=header,data=data)
     time.sleep(30)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     if info['Status']== 100:
        if  info['Data']==0.0:
          print("请勿重复浏览")
        else:  
         print(f"浏览成功，获得{info['Data']}绿星币")  
     else:
       print("浏览失败")

def get_qiandao(header):#签到任务
   url = "https://api.pftp2012.com/api/Member/SignIn"
   data ={
        "channel": "40"
        }
   response = s.post(url=url,headers=header,data=data)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   if info['Status']== 100:
       print(f"签到成功,获得{info['Data']['PollenNum']}绿星币,签到天数{info['Data']['ContinuouNum']}")  
   else:
       print("签到失败")

def sicxs():
    try:
        env_cookie = os.environ.get("wx_zwxq")
        si_cookie = getattr(config, 'wx_zwxq', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_zwxq='' 或在 config.py 中设置 wx_zwxq =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_zwxq='' 或在 config.py 中设置 wx_zwxq =")
        sys.exit()

    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
          print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
          params_list = re.split('#',list_cookie_i)
          useradmin = params_list[0]
          password = hashlib.md5(params_list[1].encode('utf-8')).hexdigest().lower()
          get_info(useradmin,password)
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错：账号密码错误，或者账号被封禁，请检查后重试！")    

    print(f'\n-----------  执 行  结 束 -----------')



if __name__ == '__main__':
  sicxs() 