# name: 铛铛回收
# Author: sicxs
# Date: 2025-1-12
# 微信小程序
# export wx_ddhs="token" 
# 抓小程序auth和username值
# 多号 @,&分割 
# cron: 25 8 * * *
# new Env('铛铛回收');


import requests
import os,json,sys,time,config,re

def index(tonken):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/8555',
        'xweb_xhr': '1',
        'token': tonken ,
        'content-type': 'application/json',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wxe378d2d7636c180e/630/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('https://vues.dd1x.cn/ali/getUserInfo', headers=headers).json()
    print(f"登陆成功，用户名：{response['data']['nickName']}")
    time.sleep(3)
    dd_qiandao(headers)
    try:
      for i in range(1,6):
         s1 = dd_cj(headers)
         print(s1)
         if s1 == "当前用户没有抽奖次数":
            break
    except:
      print("没有抽奖机会")
def dd_qiandao(headers):
    response = requests.get('https://vues.dd1x.cn/api/v2/sign_join', headers=headers).json()
    if response['code'] == 0:
        print("签到成功")
    else:
        print(response['msg'])    
def dd_cj(headers):
    response = requests.get('https://vues.dd1x.cn/front/activity/update_lottery_result?id=2669249', headers=headers).json()
    time.sleep(3)
    if response['code'] == 0:
        return f"获得：{response['data']['goodName']}"
    else:
        return response['msg']
def sicxs():
    try:
        env_cookie = os.environ.get("wx_ddhs")
        si_cookie = getattr(config, 'wx_ddhs', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_ddhs='' 或在 config.py 中设置 wx_ddhs =''")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_ddhs='' 或在 config.py 中设置 wx_ddhs =''")
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