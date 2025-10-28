"""
name: 全球主机论坛
Author: sicxs
Date: 2024-11-4
export hostloc="cookie" @,&分割
cron: 0 8 * * *
"""
import requests
import re,os,sys
import time
import random
from notify import send
def pr(message):
    msg.append(message + "\n" )
    print(message)

msg = []
def index(cookie): #登录
     url = 'https://hostloc.com/forum.php'
     header = {
        "authority": "hostloc.com",
        "method": "GET",
        "path": "/forum.php",
        "scheme": "https",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "referer": "https://hostloc.com/",
        "cookie":cookie
        }
     try:
        response = requests.get(url=url,headers=header )
        if "积分" in response.text:
         pr("登陆成功")  
         pattern = re.compile(r"discuz_uid = '(.*?)'")
         matches = pattern.findall(response.text)
         if not matches:
          pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
          return
         uid = str(matches[0])
         sicxs_task(cookie)
         time.sleep(5)
         my(cookie,uid)
        else:
         pr("登录失败")
     except Exception as e:
          pr(e)

def my(cookie,uid): #我的信息
     
     url = f'https://hostloc.com/home.php?mod=space&uid={uid}&do=profile'
     header = {
        "Connection":"keep-alive",
        "authority":"hostloc.com",
        "method":"GET",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "referer":"https://hostloc.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "content-type": "text/html; charset=utf-8",
        "cookie":cookie
    }
     
     response = requests.get(url=url,headers=header)
     pattern = re.compile(r'title="访问我的空间">(.*?)</a>')
     pattern2 = re.compile(r'<li><em>积分</em>(.*?)</li><li><em>威望</em>(.*?) </li>')
     pattern3 = re.compile(r'<li><em>金钱</em>(.*?) </li>')

    

     matches = pattern.findall(response.text)
     matches1 = pattern2.findall(response.text)
     matches2 = pattern3.findall(response.text)
     if not matches or not matches1 or not matches2:
         pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
         return

     pr( "用户名：" + matches[0] + " 积分：" + matches1[0][0] + " 威望：" + matches1[0][1] + " 金钱：" + matches2[0])
    

def sicxs_task(cookie):#任务
    
      for  i in range(10):
        uuid = random.randint(5000, 15000)
        time.sleep(5)
        url = f'https://hostloc.com/space-uid-{uuid}.html'
        header = {      
          "Connection":"keep-alive",
          "authority":"hostloc.com",
          "method":"GET",
          "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
          "content-type": "text/html; charset=utf-8",
          "cookie":cookie         
      } 
        response = requests.get(url=url,headers=header)
        info = response.text
        if "个人资料"in info:
            pr(f"第{i}次访问{uuid}用户成功")
        elif "您指定的用户空间不存在" in info:
            pr("访问失败，重试中")
        else:
            pr("访问失败，重试中")




def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')       
    try:
        env_cookie = os.environ.get("wy_hostloc")
        si_cookie = getattr(config, 'wy_hostloc', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wy_hostloc='' 或在 config.py 中设置 wy_hostloc")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wy_hostloc='' 或在 config.py 中设置 wy_hostloc")
        sys.exit()
    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        pr(f"账号【{i + 1}】开始执行：")
        try:
            index(list_cookie_i)
        except Exception as e:
            pr(f"执行账号【{i + 1}】时发生错误: {e}")
        finally:
          send("全球主机论坛", ''.join(msg))
          msg.clear()

               
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
  sicxs()
 