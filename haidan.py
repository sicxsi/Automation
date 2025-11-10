# name: 海胆
# Author: sicxs
# Date: 2024-11-2
# export wy_haidan="cookie"  换行,&分割
# cron: 10 9 * * *
# new Env('海胆');
import requests, time
import re,os,sys
from notify import send

def pr(message):
    msg.append(message+ "\n")
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
                time.sleep(3)
                continue
            if resp.status_code != 200:
                pr(f"第{attempt}次 返回状态 {resp.status_code}，视为失败，重试中...")
                time.sleep(3)
                continue
            return resp
        except requests.exceptions.Timeout:
            pr(f"第{attempt}次 请求超时（>{timeout}s），重试中...")
            time.sleep(3)
        except requests.RequestException as e:
            pr(f"第{attempt}次 请求异常: {e}，重试中...")
            time.sleep(3)
    pr(f"请求超过最大重试次数 ({max_retries})，跳过当前账号。")
    return None

def index(cookie):
    url = 'https://www.haidan.video/index.php'
    header = {
        "authority": "www.haidan.video",
        "method": "GET",
        "path": "/index.php",
        "referer":"https://www.haidan.video/torrents.php",
        "User-Agent": "Mozilla/5.0",
        "content-type": "text/html; charset=utf-8; Cache-control:private",
        "cookie":cookie
    }
    try:
        response = get_with_retries(url, header, max_retries=3, timeout=5)
        if not response:
            pr("账号登录失败，跳过该账号。")
            return
        time.sleep(3)
        info = response.text
        if "打卡" in info:
            pr("账号登陆成功")
            signin(cookie)
        else:
            pr("登录失败, 请检查cookie是否正确")
    except Exception as e:
        pr(e)

def signin(cookie):
    url = 'https://www.haidan.video/signin.php'
    header = {
        "authority": "www.haidan.video",
        "method": "GET",
        "path": "/signin.php",
        "referer":"https://www.haidan.video/index.php",
        "User-Agent": "Mozilla/5.0",
        "cookie":cookie
    }
    try:
        response = get_with_retries(url, header, max_retries=3, timeout=5)
        if response.status_code == 200:
            pr("打卡成功，请勿重复刷新。")
            torrents(cookie)
        else:
            pr("打卡失败，已达到最大重试次数，跳过该账号。")
    except Exception as e:
        pr(e)
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

        if not matches or not matches1 or not matches2 or not matches3 or not matches4:
          pr("解析用户信息失败")
          return
        pr( "用户名：" + matches[0] + " 魔力值：" + matches2[0][1] + " 分享率" + matches1[0] +  " 上传量" + matches3[0] + " 下载量" + matches4[0])
     except Exception as e:
         pr("登陆失败")

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
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
            pr("请设置变量 export wy_haidan='' 或在 config.py 中设置 wy_haidan")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wy_haidan='' 或在 config.py 中设置 wy_haidan")
        sys.exit()
    list_cookie = [c for c in re.split(r'\n|&', cookies) if c.strip()]
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        pr(f"账号【{i + 1}】开始执行：")
        try:
            index(list_cookie_i)
        except Exception as e:
            pr(f"执行账号【{i + 1}】时发生错误: {e}")
        finally:
            send("海胆PT站", ''.join(msg))
            msg.clear()  
    print(f'\n-----------  执 行  结 束 -----------')


if __name__ == '__main__':
  sicxs()