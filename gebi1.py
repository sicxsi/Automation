
# name: 隔壁网
# Author: sicxs
# Date: 2024-11-5
# export wy_gebi="cookie" @,&分割
# cron: 20 8 * * *
# new Env('隔壁网');

import requests
import time,re,os,sys
import config


def index(cookie):#登录
    url = "https://www.gebi1.com/portal.php"
    headers = {
    "authority": "www.gebi1.com",
    "method": "GET",
    "path": "/portal.php",
    "scheme": "https",
    "cookie": cookie,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    }
    try:  
      response = requests.get(url, headers=headers)
      info = response.text
      pattern = re.compile(r'访问我的空间" class="(.*?)">(.*?)</a>')
      pattern1 = re.compile(r'formhash=(.*?)" ')
      matches = pattern.findall(info)
      matches1 = pattern1.findall(info)
      uid = matches1[0]
      print(f"登录成功 \n用户名：{matches[0][1]}")
      time.sleep(5)
      sign(cookie,uid)

    except Exception as e:
         print(e)

def sign(cookie,uid):
    url = f"https://www.gebi1.com/plugin.php?id=k_misign:sign&operation=qiandao&format=global_usernav_extra&formhash={uid}&inajax=1&ajaxtarget=k_misign_topb"
    headers = {
     "authority": "www.gebi1.com",
     "method": "GET",
     "path": f"/plugin.php?id=k_misign:sign&operation=qiandao&format=global_usernav_extra&formhash={uid}&inajax=1&ajaxtarget=k_misign_topb",
     "scheme": "https",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
     "Connection": "keep-alive",
     "Accept-Encoding": "gzip, deflate, br, zstd",
     "referer": "https://www.gebi1.com/home.php?mod=spacecp&ac=credit&showcredit=1",
     "cookie": cookie,
        }
    try:
      response = requests.get(url, headers=headers)
      info = response.text
      if "今日已签" in info:
        print("签到成功")
        time.sleep(5)
        my(cookie)
      else:
        print("签到失败")
    except Exception as e:       
         print(e)  
def my(cookie):
    url = "https://www.gebi1.com/home.php?mod=spacecp&ac=credit&showcredit=1"
    headers = {
     "authority": "www.gebi1.com",
     "method": "GET",
     "path": "/home.php?mod=spacecp&ac=credit&showcredit=1",
     "scheme": "https",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
     "Connection": "keep-alive",
     "Accept-Encoding": "gzip, deflate, br, zstd",
     "cookie": cookie,
        }
    try:
      response = requests.get(url, headers=headers)
      info = response.text
      pattern = re.compile(r'丝瓜: </em>(.*?) 条')
      pattern1 = re.compile(r'经验值: </em>(.*?) 点')
      pattern2 = re.compile(r'贡献: </em>(.*?) 点')
      pattern3 = re.compile(r'积分: </em>(.*?) ')

      matches = pattern.findall(info)
      matches1 = pattern1.findall(info)
      matches2 = pattern2.findall(info)
      matches3 = pattern3.findall(info)

      print(f"丝瓜：{matches[0]},经验：{matches1[0]},贡献：{matches2[0]},积分：{matches3[0]}")
      
    except Exception as e:       
         print(e)  


def sicxs():
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
            print("请设置变量 export wy_gebi='' 或在 config.py 中设置 wy_gebi")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_gebi='' 或在 config.py 中设置 wy_gebi")
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
