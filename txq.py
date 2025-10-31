# name: 汤星球会员中心
# Author: sicxs
# Date: 2024-11-21
# export wx_txq="authorization"  换行,&分割
# cron: 11 8 * * *
# new Env('汤星球会员中心');

import requests
import re,os,sys,json
from notify import send

def pr(message):
    msg.append(message + "\n")
    print(message)

msg = []

def index(authorization):

    url = "https://vip.by-health.com/vip-api/sign/activity/detail"

    data = {}

    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541022) XWEB/16467",
    'Content-Type': "application/json",
    'content-type': "application/json;charset=utf-8",
    'authorization': authorization,
    'origin': "https://vip.by-health.com",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    try:

      if info['success']:
        pr(f"账号登陆成功\n用户名：{info['data']['result']['nickName']}")
        activityId = info['data']['result']['activityId']
        qiandao(headers,activityId)
      else:
         pr("账号登录失败")  
    except Exception as e:
       print("错误")
def qiandao(headers,activityId):
    url = "https://vip.by-health.com/vip-api/sign/daily/create"

    data = {
    "activityId": activityId
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    try:
      if "data" in info and 'data' in info['data']:
         if info['data']['rspCode'] == 00:
            pr(f"签到成功：\n已经签到{info['data']['result']['accumulateDay']}天，本次签到获得：{info['data']['result']['dailyPointReward']}积分")
         elif info['data']['rspCode'] == "SIGN_TODAY_ALREADY_DONE":
            pr("今日已完成签到")
         else:
            pr("签到失败，请稍后再试。")   
      else:
         pr(info['data']['rspMsg'])
    except Exception as e:
       print("错误")

   
def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')
    try:
        env_cookie = os.environ.get("wx_txq")
        si_cookie = getattr(config, 'wx_txq', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wx_txq='' 或在 config.py 中设置 wx_txq")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wx_txq='' 或在 config.py 中设置 wx_txq")
        sys.exit()
    list_cookie = [c for c in re.split(r'\n|&|@', cookies) if c.strip()]
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        pr(f"账号【{i + 1}】开始执行：")
        try:
            index(list_cookie_i)
        except Exception as e:
            pr(f"执行账号【{i + 1}】时发生错误: {e}")
        finally:
            send("汤星球会员中心", ''.join(msg))
            msg.clear()

    print(f'\n-----------  执 行  结 束 -----------')


if __name__ == '__main__':
  
  sicxs()       