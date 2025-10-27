# name: 家园
# Author: sicxs
# Date: 2024-10-29
# export wy_hdhome="cookie" &,@分割
# cron: 8 8 * * *
# new Env('家园');
import requests
import re,time
import os,sys

s = requests.session()
def index(cookie):
     url = 'https://hdhome.org/index.php'
     header = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "host":"hdhome.org",
        "referer":"https://hdhome.org/torrents.php",
        "cookie":cookie
    }
     try:
        response = s.get(url=url,headers=header)
        time.sleep(3)
        info = response.text
        if "首页" in info:
         print("登陆成功")
        
         attendance(cookie)  
        else:
         print("登录失败")
     except Exception as e:
          print(e)
def attendance(cookie):
     url = 'https://hdhome.org/attendance.php'
     header = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "host":"hdhome.org",
        "referer":"https://hdhome.org/torrents.php",
        "cookie":cookie
    }
     try:
        response = s.get(url=url,headers=header)
        time.sleep(3)
        info = response.text
        if "签到已得" in info:
         print("签到成功，请勿重复刷新。")
         torrents(cookie)
        else :
          print("签到中...")
          attendance(cookie)
     except Exception as e:
          print(e)
def torrents(cookie):
    url = 'https://hdhome.org/torrents.php'
    header = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "host":"hdhome.org",
        "referer":"https://hdhome.org",
        "cookie":cookie
    }
    response = s.get(url=url,headers=header)
    time.sleep(3)
    pattern = re.compile(r"class='(.+?)'><b>(.+?)</b>")
    pattern2 = re.compile(r']: (.*)&nbsp;\(')
    pattern3 = re.compile(r'签到已得(.*?)\) ')
    pattern4 = re.compile(r'做种积分：</font>(.*?) ')
    

    matches = pattern.findall(response.text)
    matches1 = pattern2.findall(response.text)
    matches2 = pattern3.findall(response.text)
    matches3 = pattern4.findall(response.text)
       
       
    print( "用户名：" + matches[0][1] + " 魔力值：" + matches1[0] + " 签到已得：" + matches2[0]+ " 做种积分：" + matches3[0])


def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        print("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('可以在此文件中添加配置变量，例如：\n sfsy = ""\n')
    try:
        env_cookie = os.environ.get("wy_hdhome")
        si_cookie = getattr(config, 'wy_hdhome', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_hdhome='' 或在 config.py 中设置 wy_hdhome")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_hdhome='' 或在 config.py 中设置 wy_hdhome")
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
 