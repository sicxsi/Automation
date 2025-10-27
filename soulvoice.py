
# name: 铃音
# Author: sicxs
# Date: 2024-11-1
# export wy_soulvoice="cookie" @,&分割
# cron: 10 9 * * *
# new Env('铃音');
import requests
import re,os,sys

def index(cookie):
     url = 'https://pt.soulvoice.club/index.php'
     header = {
        "Connection": "keep-alive",
        "authority": "pt.soulvoice.club",
        "method": "GET",
        "path": "/index.php",
        "referer":"https://pt.soulvoice.club/attendance.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie":cookie
    }
     try:
        response = requests.get(url=url,headers=header)
        info = response.text
        if "首页" in info:
         print("登陆成功")
         attendance(cookie)  
        else:
         print("登录失败")
     except Exception as e:
          print(e)
def attendance(cookie):
     url = 'https://pt.soulvoice.club/attendance.php'
     header = {
        "Connection": "keep-alive",
        "authority": "pt.soulvoice.club",
        "method": "GET",
        "path": "/attendance.php",
        "referer":"https://pt.soulvoice.club/index.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie":cookie
    }
     try:
        response = requests.get(url=url,headers=header)
        info = response.text
        if "签到成功" in info:
           
           print("签到成功")

           torrents(cookie)

        elif "您今天已经签到过了" in info:
         
         print("您今天已经签到过了，请勿重复刷新。")
        

         torrents(cookie)

        else :
         print("签到失败")
          
     except Exception as e:
          print(e)
def torrents(cookie):
     url = 'https://pt.soulvoice.club/torrents.php'
     header = {
        "Connection": "keep-alive",
        "authority": "pt.soulvoice.club",
        "method": "GET",
        "path": "/torrents.php",
        "referer":"https://pt.soulvoice.club/attendance.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie":cookie
    }
     try:
       response = requests.get(url=url,headers=header)
       pattern = re.compile(r"class='CrazyUser_Name'><b>(.+?)</b>")
       pattern2 = re.compile(r'>使用</a>]: (.*)                 <a')
       pattern3 = re.compile(r'签到已得(.*?)\]</a>')
    

       matches = pattern.findall(response.text)
       matches1 = pattern2.findall(response.text)
       matches2 = pattern3.findall(response.text)

       print( "用户名：" + matches[0] + " 魔力值：" + matches1[0] + " 签到已得：" + matches2[0])
      
     except Exception as e:
         print(e)

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        print("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('可以在此文件中添加配置变量，例如：\n sfsy = ""\n')
    try:
        env_cookie = os.environ.get("wy_soulvoice")
        si_cookie = getattr(config, 'wy_soulvoice', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_soulvoice='' 或在 config.py 中设置 wy_soulvoice")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_soulvoice='' 或在 config.py 中设置 wy_soulvoice")
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
 