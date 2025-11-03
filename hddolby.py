# name: 杜比
# Author: sicxs
# Date: 2024-11-04
# export wy_hddolby="cookie" &,换行分割
# 请不要异地签到，最起码在本地先登陆下
# cron: 10 8 * * *
# new Env('杜比');
import requests, time
import re,os,sys
from notify import send

def pr(message):
    msg.append(message + "\n")
    print(message)

msg = []

s = requests.session()

def get_with_retries(url, headers, max_retries=3, timeout=5):
    """请求超过 timeout 视为失败，最多重试 max_retries 次。三次失败返回 None（跳过当前账号）。"""
    for attempt in range(1, max_retries + 1):
        try:
            start = time.time()
            resp = s.get(url=url, headers=headers, timeout=timeout)
            elapsed = time.time() - start
            if elapsed > timeout:
                pr(f"第{attempt}次 请求耗时 {elapsed:.2f}s（>{timeout}s），视为失败，重试中...")
                time.sleep(1)
                continue
            if resp.status_code != 200:
                pr(f"第{attempt}次 返回状态 {resp.status_code}，视为失败，重试中...")
                time.sleep(1)
                continue
            return resp
        except requests.exceptions.Timeout:
            pr(f"第{attempt}次 请求超时（>{timeout}s），重试中...")
            time.sleep(1)
        except requests.RequestException as e:
            pr(f"第{attempt}次 请求异常: {e}，重试中...")
            time.sleep(1)
    pr(f"请求超过最大重试次数 ({max_retries})，跳过当前账号。")
    return None

def index(cookie):
    url = 'https://www.hddolby.com/index.php'
    header = {
        "authority": "www.hddolby.com",
        "method": "GET",
        "path": "/index.php",
        "User-Agent": "Mozilla/5.0",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "host":"www.hddolby.com",
        "referer":"https://www.hddolby.com/index.php",
        "cookie":cookie
    }
    try:
        response = get_with_retries(url, header, max_retries=3, timeout=5)
        if not response:
            pr("本账号请求失败，跳过该账号。")
            return
        time.sleep(3)
        info = response.text
        if "签到" in info:
            pr("账号登陆成功")
            if "签到已得" in info:
                pr("您今天已经签到过了，请勿重复刷新。")
                torrents(cookie)
            else:
                attendance(cookie)
        else:
            pr("登录失败")
    except Exception as e:
        pr(e)

def attendance(cookie):
    url = 'https://www.hddolby.com/attendance.php'
    header = {
        "authority": "www.hddolby.com",
        "method": "GET",
        "path": "/attendance.php",
        "User-Agent": "Mozilla/5.0",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "host":"www.hddolby.com",
        "referer":"https://www.hddolby.com/index.php",
        "cookie":cookie
    }
    try:
        response = get_with_retries(url, header, max_retries=3, timeout=5)
        if not response:
            pr("本账号签到请求失败，跳过该账号。")
            return
        time.sleep(3)
        info = response.text
        if "签到已得" in info:
            pr("签到成功，请勿重复刷新。")
            torrents(cookie)
        else:
            pr("签到失败，已达到最大重试次数，跳过该账号。")
    except Exception as e:
        pr(e)
def torrents(cookie):
     url = 'https://www.hddolby.com/torrents.php'
     header = {
        "authority": "www.hddolby.com",
        "method": "GET",
        "path": "/torrents.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "host":"www.hddolby.com",
        "referer":"https://www.hddolby.com/attendance.php",
        "cookie":cookie
    }
     try:
       response = s.get(url=url,headers=header)
       time.sleep(5)
       pattern = re.compile(r"class='UltimateUser_Name'><b>(.+?)</b>")
       pattern2 = re.compile(r']: (.*)&nbsp;\(')
       pattern3 = re.compile(r'签到已得(.*?)\) ')
       matches = pattern.findall(response.text)
       matches1 = pattern2.findall(response.text)
       matches2 = pattern3.findall(response.text)
       if not matches or not matches1 or not matches2:
          pr("解析用户信息失败，可能页面结构变化或 cookie 无效")
          return
       pr( "用户名：" + matches[0] + " 鲸币：" + matches1[0] + " 签到已得：" + matches2[0])

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
        env_cookie = os.environ.get("wy_hddolby")
        si_cookie = getattr(config, 'wy_hddolby', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wy_hddolby='' 或在 config.py 中设置 wy_hddolby")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wy_hddolby='' 或在 config.py 中设置 wy_hddolby")
        sys.exit()
    list_cookie = [c for c in re.split(r'\n|&', cookies) if c.strip()]
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        pr(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        pr(f"账号【{i + 1}】开始执行：")
        try:
            index(list_cookie_i)
        except Exception as e:
            pr(f"执行账号【{i + 1}】时发生错误: {e}")
        finally:
            send("杜比PT站", ''.join(msg))
            msg.clear() 
    print(f'\n-----------  执 行  结 束 -----------')


if __name__ == '__main__':
  sicxs()