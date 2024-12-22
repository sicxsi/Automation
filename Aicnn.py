# name: Aicnn
# Author: sicxs
# Date: 2024-12-22
# export wy_Aicnn="Authorization" 不需要 Bearer 使用抓包软件抓 https://api.aicnn.cn 任意 Authorization
# 换行  & 分割，免费GPT-plus | Claude-pro镜像站
# http://aicnn.cn/loginPage?aff=Vg3HwDomIt
# 功能:签到
# cron: 20 8 * * *
# new Env('Aicnn');

import json
import requests
import re,os,sys,time
import config


def header(Authorization):
    return {
        "Host": "api.aicnn.cn",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {Authorization}",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "application/json",
        "Origin": "https://aicnn.cn",
        "Referer": "https://aicnn.cn/",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        } 
def index(Authorization):
    url = "https://api.aicnn.cn/app-api/system/user/userinfo"
    headers = header(Authorization)
    response =  requests.get(url, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['code'] == 0:
        print(f"登陆成功，用户名{info['data']['username']}")
        time.sleep(3)
        qiandao(Authorization)
    else:
        print(f"登陆失败，{info['msg']}")


def qiandao(Authorization):
    url = "https://api.aicnn.cn/app-api/system/user/signin"
    headers = header(Authorization)
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['code'] == 0:
        print(info['data'])
    else:
        print(f"签到失败，{info['msg']}")

def sicxs():
    try:
        env_cookie = os.environ.get("wy_Aicnn")
        si_cookie = getattr(config, 'wy_Aicnn', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_Aicnn='' 或在 config.py 中设置 wy_Aicnn")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_Aicnn='' 或在 config.py 中设置 wy_Aicnn")
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