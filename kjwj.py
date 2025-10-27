# name: 科技玩家
# Author: sicxs
# Date: 2024-11-4
# export wy_kjwj="账号#密码"&分割 
# cron: 15 8 * * *
# new Env('科技玩家');
import requests
import re,os,sys,json,time
from notify import send

def pr(message):
    msg.append(message + "\n")
    print(message)

msg = []
def logn(zhanghao,mima):
     url = "https://www.kejiwanjia.net/wp-json/jwt-auth/v1/token"
     header = {
        "authority": "www.kejiwanjia.net",
        "method": "POST",
        "path": "/wp-json/jwt-auth/v1/token",
        "scheme": "https",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "origin": "https://www.kejiwanjia.net",
        "referer": "https://www.kejiwanjia.net/",
        }
    
     data = {
        "nickname": "",
        "username": zhanghao,
        "password": mima,
        "code": "",
        "img_code": "",
        "invitation_code": "",
        "token": "",
        "smsToken": "",
        "luoToken": "",
        "confirmPassword": "",
        "loginType": ""
        }
     try:
        response = requests.post(url=url,headers=header,data=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        return info['token']
     except Exception as e:
          pr(e)


def getUserInfo(authorization):#我的信息
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/getUserInfo"
    header = {
     "authority": "www.kejiwanjia.net",
     "method": "POST",
     "path": "/wp-json/b2/v1/getUserInfo",
     "scheme": "https",
     "authorization": f"Bearer {authorization}",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
     "origin": "https://www.kejiwanjia.net",
     "referer": "https://www.kejiwanjia.net/",
       }
    try:
        response = requests.post(url=url,headers=header)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        pr(f"用户名: {info['user_data']['name']}")
        time.sleep(3)
        getUserMission(authorization)
        time.sleep(5)
        userMission(authorization)  
    except Exception as e:
          pr(e)
def getGoldList(authorization):#积分查询
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/getGoldList"
    header = {
     "authority": "www.kejiwanjia.net",
     "method": "POST",
     "path": "/wp-json/b2/v1/getGoldList",
     "scheme": "https",
     "authorization": f"Bearer {authorization}",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
     "origin": "https://www.kejiwanjia.net",
     "referer": "https://www.kejiwanjia.net/",
        }
    try:
        response = requests.post(url=url,headers=header)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        pr(f"最近一次签到：{info['data'][0]['date']},获得积分；{info['data'][0]['no']},总积分：{info['data'][0]['total']}")
    except Exception as e:
          pr(e)
def getUserMission(authorization):#更新签到
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/getUserMission"
    header = {
     "authority": "www.kejiwanjia.net",
     "method": "POST",
     "path": "/wp-json/b2/v1/getUserMission",
     "scheme": "https",
     "authorization": f"Bearer {authorization}",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
     "origin": "https://www.kejiwanjia.net",
     "referer": "https://www.kejiwanjia.net/",
        }
    try:
        response = requests.post(url=url,headers=header)
        s1 = response.status_code 
        if 200 ==s1:
            pr("正在初始签到，请稍等。")
    except Exception as e:
          pr(e)
def userMission(authorization): #签到
    url = "https://www.kejiwanjia.net/wp-json/b2/v1/userMission"
    header = {
     "authority": "www.kejiwanjia.net",
     "method": "POST",
     "path": "/wp-json/b2/v1/userMission",
     "scheme": "https",
     "authorization": f"Bearer {authorization}",
     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
     "origin": "https://www.kejiwanjia.net",
     "referer": "https://www.kejiwanjia.net/",
        }
    try:
        response = requests.post(url=url,headers=header)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if "message" in  info :
          pr("你的authorization可能过期了，请检查。")
        elif "credit" in info:
          pr(f"恭喜您，签到获得,{info['credit']}积分")
          time.sleep(5)
          getGoldList(authorization)
        else:
            pr("请勿重复签到")
            time.sleep(5)
            getGoldList(authorization)  
         #pr(f"最近一次签到：{info['data'][0]['date']},获得积分；{info['data'][0]['no']},总积分：{info['data'][0]['total']}")
    except Exception as e:
          pr(e)

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')    
    try:
        env_cookie = os.environ.get("wy_kjwj")
        si_cookie = getattr(config, 'wy_kjwj', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wy_kjwj='' 或在 config.py 中设置 wy_kjwj =")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wy_kjwj='' 或在 config.py 中设置 wy_kjwj =")
        sys.exit()

    list_cookie = re.split(r'\n|&', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            list = list_cookie_i.split("#")
            authorization = logn(list[0], list[1])
            getUserInfo(authorization)
        except Exception as e:
            pr(f"账号【{i + 1}/{total_cookies}】执行出错")    

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
 sicxs()