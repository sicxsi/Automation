# name: 隔壁网
# Author: sicxs
# Date: 2024-11-4
# export wy_gebi="cookie" @,& 分割
# cron: 25 8 * * *
# new Env('隔壁网');

import requests
import time
import re
import os
import sys
from notify import send

def pr(message):
    msg.append(message+ "\n")
    print(message)

msg = []

def index(username, password):  # 登录
    url = "https://gebi1.com/member.php"

    params = {
        'mod': "logging",
        'action': "login",
        'loginsubmit': "yes",
        'handlekey': "login",
        'loginhash': "LGugm",
        'inajax': "1"
    }

    payload = {
        'referer': "https://gebi1.com/portal.php",
        'username': username,
        'password': password,
        'questionid': "0",
        'answer': ""
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'cache-control': "max-age=0",
        'origin': "https://gebi1.com",
        'referer': "https://gebi1.com/portal.php",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        'priority': "u=0, i",
    }

    # 登录请求
    response = requests.post(url, params=params, data=payload, headers=headers)
    if "欢迎您回来" in response.text:
        pattern = re.compile(r"'username':'(.*?)','usergroup':'(.*?)','uid':'(.*?)','gr")
        matches = pattern.findall(response.text)
        if not matches:
          pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
          return
        cookies = response.cookies
        pr(f"登录成功，用户名：{matches[0][0]}")
        time.sleep(2)  
        sign(matches[0][2],cookies)
    else:
        pr("登录失败，请检查账号密码是否正确")
        sys.exit()

def formhash(cookies):
    url = "https://www.gebi1.cn/forum.php"
    try:
        response = requests.get(url, cookies=cookies)
        info = response.text
        pattern = re.compile(r'formhash=(.*?)&amp;')
        matches = pattern.findall(info)
        if not matches:
          pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
          return

        return matches[0]
    except Exception as e:
        pr(e)
def sign(uid,cookies):

    url = "https://www.gebi1.cn/plugin.php"
    formhash1 = formhash(cookies)
    params ={
        "id": "k_misign:sign",
        "operation": "qiandao",
        "format": "button",
        "formhash": f"{formhash1}",
        "inajax": "1",
        "ajaxtarget": "midaben_sign"
        }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        'referer': "https://www.gebi1.cn/forum.php",
        'priority': "u=0, i",
    }

   
    try:
        response = requests.get(url, params=params,headers=headers,cookies=cookies)
        info = response.text
        if "今日已签" in info:
            pr("签到成功")
            time.sleep(5)
            my(uid, headers)
        else:
            pr("签到失败")
    except Exception as e:
        pr(e)


def my(uid, headers,cookies):
    url = f"https://gebi1.com/home.php?mod=space&uid={uid}&do=profile&from=space"
    try:
        
        response = requests.get(url, headers=headers,cookies=cookies)
        info = response.text
        pattern = re.compile(r'<span>(.*?)</span>积分</a>')
        pattern1 = re.compile(r'<span>(.*?)</span>经验值</a>')
        pattern2 = re.compile(r'<span>(.*?)</span>丝瓜</a>')
        pattern3 = re.compile(r'<span>(.*?)</span>贡献</a>')

        matches = pattern.findall(info)
        matches1 = pattern1.findall(info)
        matches2 = pattern2.findall(info)
        matches3 = pattern3.findall(info)
        if not matches or not matches1 or not matches2 or not matches3:
          pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
          return
        pr(f"丝瓜：{matches2[0]},经验：{matches1[0]},贡献：{matches3[0]},积分：{matches[0]}")

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
        env_cookie = os.environ.get("wy_gebi")
        si_cookie = getattr(config, 'wy_gebi', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wy_gebi='' 或在 config.py 中设置 wy_gebi")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wy_gebi='' 或在 config.py 中设置 wy_gebi")
        sys.exit()
    
    list_cookie = re.split(r'\n|&', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        pr(f"账号【{i + 1}】开始执行：")
        try:
            list = list_cookie_i.split("#")
            index(list[0], list[1])
        except Exception as e:
            pr(f"执行账号【{i + 1}】时发生错误: {e}")
        finally:
            send("隔壁网", ''.join(msg))
            msg.clear()
    print(f'\n----------- 执 行 结 束 -----------')


if __name__ == '__main__':
    sicxs()
