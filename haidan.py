
# name: 海胆
# Author: sicxs
# Date: 2024-11-2
# export wy_haidan="cookie"  @,&分割
# cron: 10 9 * * *
# new Env('海胆');
import requests
import re,os,sys
import time

def index(cookie):
     url = 'https://www.haidan.video/index.php'
     header = {
        "authority": "www.haidan.video",
        "method": "GET",
        "path": "/index.php",
        "referer":"https://www.haidan.video/torrents.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie":cookie
    }
     try:
        response = requests.get(url=url,headers=header)
        time.sleep(3)
        info = response.text
        if "首页" in info:
         print("登陆成功")
        
         signin(cookie)  
        else:
         print("登录失败,等待10秒后重试")
         time.sleep(10)
         signin(cookie)  
     except Exception as e:
          print("登录失败,请检查cookie是否正确")
def signin(cookie):
     url = 'https://www.haidan.video/signin.php'
     header = {
        "authority": "www.haidan.video",
        "method": "GET",
        "path": "/signin.php",
        "referer":"https://www.haidan.video/index.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "cookie":cookie
    }
     try:
        response = requests.get(url=url,headers=header)
        time.sleep(3)
        if response.status_code == 200:
           
           torrents(cookie)
        else:
           print("打卡失败？")  
        
     except Exception as e:
          
          print("登录失败")
          
def torrents(cookie):
     url = 'https://www.haidan.video/torrents.php'
     header = {
        "authority": "www.haidan.video",
        "method": "GET",
        "path": "/torrents.php",
        "referer":"https://www.haidan.video/index.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie":cookie
    }
     try:
       response = requests.get(url=url,headers=header)
       info = response.text
       time.sleep(3)
       if "已经打卡" in info:
         
         pattern = re.compile(r"class='VeteranUser_Name'><b>(.+?)</b>")
         pattern2 = re.compile(r'分享率:             </font> (.*?)        ')
         pattern3 = re.compile(r'<span id="(.*)">(.*?)</span>')
         pattern4 = re.compile(r'上传量:             </font> (.*?)        ')
         pattern5 = re.compile(r'下载量:             </font> (.*?)        ')
    

         matches = pattern.findall(info)
         matches1 = pattern2.findall(info)
         matches2 = pattern3.findall(info)
         matches3 = pattern4.findall(info)
         matches4 = pattern5.findall(info)
         print( "用户名：" + matches[0] + " 魔力值：" + matches2[0][1] + " 分享率" + matches1[0] +  " 上传量" + matches3[0] + " 下载量" + matches4[0])
       else:
         print("查询失败")
     except Exception as e:
         print("登陆失败")

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        print("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')
    try:
        env_cookie = os.environ.get("wy_haidan")
        si_cookie = getattr(config, 'wy_haidan', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wy_haidan='' 或在 config.py 中设置 wy_haidan")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_haidan='' 或在 config.py 中设置 wy_haidan")
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