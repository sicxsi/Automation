# name: 袋鼠回收
# Author: sicxs
# Date: 2025-1-12
# 微信小程序
# export wx_dshs="token" 
# 抓小程序token值
# 多号 换行,&分割 
# cron: 25 8 * * *
# new Env('袋鼠回收');

import requests
import os,sys,time,re

def pr(message):
    msg.append(message + "\n")
    print(message)

msg = []

def index(tonken):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/8555',
        'xweb_xhr': '1',
        'token': tonken ,
        'content-type': 'application/json',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wxef20c241ccc93155/203/page-frame.html',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get('https://www.lvdhb.com/MiniProgramApiCore/api/v3/My/GetMyInfo2', headers=headers).json()
    pr(f"登陆成功，用户名：{response['NickName']} 当前积分：{response['loginScore']}")
    time.sleep(3)
    ds_qiandao(headers)
def ds_qiandao(headers):
    data = {}
    response = requests.post('https://www.lvdhb.com/MiniProgramApiCore/api/v3/Login/Sign', headers=headers,json=data).json()
    if response['Success']:
        pr("签到成功")
    else:
        pr("签到失败")

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')
    try:
        env_cookie = os.environ.get("wx_dshs")
        si_cookie = getattr(config, 'wx_dshs', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_dshs='' 或在 config.py 中设置 wx_dshs =''")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_dshs='' 或在 config.py 中设置 wx_dshs =''")
        sys.exit()
    list_cookie = [c for c in re.split(r'\n|&', cookies) if c.strip()]
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