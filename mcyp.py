# name: 名创优品
# Author: sicxs
# Date: 2024-11-25
# export wx_mcyp="uid#skey" 
# &,@换行分割 
# 功能:签到，浏览任务
# cron: 20 8 * * *
# new Env('名创优品');

import requests
import re,time
import os,sys,json
import config

def get_headers(uid,skey):
    return {
        "authority": "api-saas.miniso.com",
        "method": "POST",
        "path": "/task-manage-platform/api/activity/signInTask/award/receive",
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
def index(uid,skey):
    qiandao(uid,skey)
    time.sleep(3)
    task_liulan(uid,skey)
def qiandao(uid,skey):#签到
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/signInTask/award/receive"
    header = get_headers(uid, skey)
    data = {"activityId":"18","taskId":79}
    response = requests.post(url=url,headers=header,json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 200 == info['code']:
        print("签到成功") 
    else:
        print(info['message']) 
def task_liulan(uid,skey):#浏览任务
    print("正在开始浏览任务") 
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/task/uvClick"
    header = get_headers(uid, skey)
    taskId = [176,175]
    for i in taskId:
     data = {"activityId":"18","taskId":i,"taskType":5}
     response = requests.post(url=url,headers=header,json=data)
     time.sleep(30)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     if 200 == info['code']:
         task_wc(uid,skey,i)
         task_lq(uid,skey,i)
     else:
        print(info['message']) 
def task_wc(uid,skey,id):#完成浏览任务
    url = "https://api.multibrands.miniso.com/multi-configure-platform/api/activity/task/browse/finish"
    header = get_headers(uid, skey)
    data = {"activityId":18,"taskId":id}
    response = requests.post(url=url,headers=header,json=data)
    time.sleep(30)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 200 == info['code']:
        print("浏览任务成功") 
    else:
        print(info['message'])
def task_lq(uid,skey,id):#领取奖励
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/periodTask/award/receive"
    header = get_headers(uid, skey)
    data = {"activityId":"18","taskId":id,"taskType":5}
    response = requests.post(url=url,headers=header,json=data)
    time.sleep(30)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 200 == info['code']:
        print("领取任务奖励成功") 
    else:
        print(info['message'])    


def sicxs():
    try:
        env_cookie = os.environ.get("wx_mcyq")
        si_cookie = getattr(config, 'wx_mcyq', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_mcyq='' 或在 config.py 中设置 wx_mcyq =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_mcyq='' 或在 config.py 中设置 wx_mcyq =")
        sys.exit()

    list_cookie = re.split(r'\n|&|@', cookies)
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
