# name: 名创优品
# Author: sicxs
# Date: 2024-11-25 # 2025-06-11
# export wx_mcyp="uid#skey" 
# &,@换行分割 
# 功能:签到，浏览任务
# 账号mini币只有90天有效期,过期自动失效
# cron: 20 8 * * *
# new Env('名创优品');

import requests
import re,time
import os,sys,json
from notify import send
def pr(message):
    msg.append(message + "\n" )
    print(message)

msg = []


def get_headers(uid,skey):
    return {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/13839",
    'Content-Type': "application/json",
    'content-longitude': "121.5440902709961",
    'content-latitude': "31.221139907836914",
    'tenant': "MINISO",
    'content-uid': uid,
    'content-skey': skey,
    'Referer': "https://servicewechat.com/wx2a212470bade49bf/982/page-frame.html",
    'Accept-Language': "zh-CN,zh;q=0.9"
    }
def index(uid,skey):
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/signInTask/award/receive"
    header = get_headers(uid, skey)
    data = {"activityId":"18","taskId":79}

    response = requests.post(url=url,headers=header,data=json.dumps(data))
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 200 == info['code']:
        pr("初始化签到")
        time.sleep(3)
        index(uid,skey)
    elif 500 == info['code']:
        pattern = re.compile(r'当前手机号(.*?)今日')
        matches = pattern.findall(info['message'])
        pr(f"用户名：{matches[0]}")
        pr("签到成功")
        time.sleep(3)
        task_liulan(uid,skey)
        time.sleep(3)
        wx_info(uid,skey)
    else:
        pr(info['message'])
def sicxs_id(): #任务远程接口
    url = "https://api.sicxs.cn/i/mcyp.php"
    response = requests.get(url=url)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    return info['msg']



def task_liulan(uid,skey):#浏览任务
    pr("正在开始浏览任务") 
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/task/uvClick"
    header = get_headers(uid, skey)
    taskId = sicxs_id()
    for i in taskId:
     data = {"activityId":"18","taskId":i,"taskType":5}
     response = requests.post(url=url,headers=header,data=json.dumps(data))
     time.sleep(10)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     if 200 == info['code']:
         task_wc(uid,skey,i)
         task_lq(uid,skey,i)
     else:
        pr(info['message']) 
def task_wc(uid,skey,id):#完成浏览任务
    url = "https://api.multibrands.miniso.com/multi-configure-platform/api/activity/task/browse/finish"
    header = get_headers(uid, skey)
    data = {"activityId":"18","taskId":id}
    response = requests.post(url=url,headers=header,data=json.dumps(data))
    time.sleep(30)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 200 == info['code']:
        pr("浏览任务成功") 
    else:
        pr("浏览任务失败")
def task_lq(uid,skey,id):#领取奖励
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/periodTask/award/receive"
    header = get_headers(uid, skey)
    data = {"activityId":"18","taskId":id,"taskType":5}
    response = requests.post(url=url,headers=header,data=json.dumps(data))
    time.sleep(30)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 200 == info['code']:
        pr("领取任务奖励成功") 
    else:
        pr(info['message'])    

def wx_info(uid,skey):
    url = "https://api-saas.miniso.com/task-manage-platform/api/virtualCoin/member"
    header = {
        "authority": "api-saas.miniso.com",
        "method": "GET",
        "content-latitude": "31.221139907836914",
        "content-longitude": "121.49022668457031",
        "tenant-code": "MINISO",
        "x-client-source": "MINISO_WX_MINI",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "tenant": "MINISO",
        "content-uid": uid,
        "content-type": "application/json",
        "content-skey": skey,
        "referer": "https://servicewechat.com/wx2a212470bade49bf/924/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    pr(f"当前mini币：{info['data']['quantity']}")


def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        pr("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('#可以在此文件中添加配置变量，例如：\nsfsy = ""\n')
    try:
        env_cookie = os.environ.get("wx_mcyp")
        si_cookie = getattr(config, 'wx_mcyp', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            pr("请设置变量 export wx_mcyp='' 或在 config.py 中设置 wx_mcyp =")
            sys.exit()
    except Exception as e:
        pr("请设置变量 export wx_mcyp='' 或在 config.py 中设置 wx_mcyp =")
        sys.exit()

    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            pr(f"账号【{i + 1}】开始执行：")
            list = list_cookie_i.split("#")
            index(list[0], list[1])
        except Exception as e:
            pr(f"账号【{i + 1}/{total_cookies}】执行出错")
        finally:
            send("名创优品小程序", ''.join(msg))
            msg.clear()        

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
 sicxs()

