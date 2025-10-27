# name: ikun vpn
# Author: sicxs
# Date: 2024-11-5
# export wy_ikun="账号#密码" & 换行分割 
# cron: 0 8 * * *
# new Env('ikun vpn');
import requests
import os,sys,re
import json,re
def index(wy_user,wy_pass):#账号密码登录

    url = "https://ikuuu.de/auth/login"
    header = {
        "authority": "ikuuu.de",
        "method": "POST",
        "path": "/auth/login",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://ikuuu.de",
        "referer": "https://ikuuu.de/auth/login",
    }
    data = {
        "host": "ikuuu.de",
        "email": wy_user, 
        "passwd": wy_pass,  #
        "code": ""
    }
    response = requests.post(url=url, headers=header, data=data)
    cookies = response.cookies
    if "1" in response.text:
        print("登录成功")
    qiandao(cookies)

def  qiandao(cookies): #签到

    url = "https://ikuuu.de/user/checkin"
    header ={
        "authority": "ikuuu.de",
        "method": "GET",
        "path": "/user/checkin",
        "scheme": "https",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "referer": "https://ikuuu.de/auth/login",
        }
    try:
        response = requests.post(url=url,headers=header,cookies=cookies)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if 1 == info['ret']:
         print(f"恭喜,{info['msg']}")
        else:
         print("请勿重复签到")  
    except Exception as e:
        print(e)
def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        print("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\n sfsy = ""\n')    
    try:
        env_cookie = os.environ.get("wy_ikun")
        si_cookie = getattr(config, 'wy_ikun', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_ikun='' 或在 config.py 中设置 wy_ikun =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_ikun='' 或在 config.py 中设置 wy_ikun =")
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