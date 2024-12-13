# name: MossFrp
# Author: sicxs
# Date: 2024-12-13
# export wy_frp=""
# 邮箱 密码登录
# 功能:签到
# cron: 20 8 * * *
# new Env('MossFrp');

import json
import hashlib
import requests
import time,re,os,sys
import config


def headerds():#请求头
  headerds =  {
  "Host": "https.ghs.wiki:7002",
  "Connection": "keep-alive",
  "Content-Length": "66",
  "access-control-max-age": "864000",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "Access-Control-Allow-Origin": "*",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Origin": "https://www.mossfrp.top",
  "Referer": "https://www.mossfrp.top/",
  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
}
  return headerds
def wy_info(useradmin,password): #登录
   url = "https://https.ghs.wiki:7002/API?void=post"
   headerd = headerds()
   password = hashlib.sha256(password.encode('utf-8')).hexdigest().lower()
   data = {
    "type": "login",
    "loginType": "email",
    "account": useradmin,
    "password": password,
    "encryption": "true"
    }
   response = requests.post(url, json=data, headers=headerd)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   if info['status'] == "404":
       print("账号或密码错误")
   elif info['status'] == "200":
        return info['token']
   else:
       print("登录失败")
def index(useradmin,password): #登录信息
    url = "https://https.ghs.wiki:7002/API?void=post"
    headerd = headerds()
    token = wy_info(useradmin,password)
    data = {
         "type": "userInfo",
         "token": token
            }
    response = requests.post(url, json=data, headers=headerd)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    print(f"用户名：{info['userInfo']['username']} 积分：{info['userInfo']['silver']}")
    if info['userInfo']['signIn'] == "true":
        print("今日已签到")
    else:
        qiandao(token)
def qiandao(token): #签到
    url = "https://https.ghs.wiki:7002/API?void=post"
    headerd = headerds()
    data = {
         "type": "signIn",
         "token": token
            }
    time.sleep(3)
    response = requests.post(url, json=data, headers=headerd)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    print(info["signInMessage"])
def sicxs():
    try:
        env_cookie = os.environ.get("wy_frp")
        si_cookie = getattr(config, 'wy_frp', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_frp='' 或在 config.py 中设置 wy_frp =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_frp='' 或在 config.py 中设置 wy_frp =")
        sys.exit()

    list_cookie = re.split(r'\n|&', cookies)
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