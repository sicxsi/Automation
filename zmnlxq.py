# name: 战马能量星球
# Author: sicxs
# Date: 2024-11-1
# 微信小程序
# export wx_zmnlxq="safe"  多账户@,&分割 https://xxx/api/xxx.php?safe=xxxxx
# 公众号口令 有能量 当燃战马！ 自己做一下！
# 完善信息任务自己做一下！
# cron: 15 8 * * *
# new Env('战马能量星球');

import requests
import os,sys,time
import json,re

def index(safe): #登录信息
    url = f"https://wxx.ball.warhorsechina.com.cn/api/getuserinfo.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print(f"登陆成功，用户名：{info['nickname']}")
         infos(safe)
         print("签到")
         time.sleep(3)
         checkin(safe)
         print("加入排行榜")
         time.sleep(3)
         joinxcx(safe)
         print("点赞")
         time.sleep(3)
         subrank(safe)
         print("分享小程序")
         time.sleep(3)
         share(safe)
         time.sleep(3)
         print("摇一摇")
         sendbattle(safe)
         print("领马")
         time.sleep(3)
         starthorse(safe)
         print("登录游戏")
         time.sleep(3)
         horselogin(safe)
         print("抚摸小马")
         time.sleep(3)
         strokehorse(safe)
         print("领取签到任务")
         time.sleep(3)
         gethorsetaskcenter(safe)
         print("分享小游戏")
         time.sleep(3)
         sharehorse(safe)
         print("摇一摇信息")
         time.sleep(3)
         getbattlemsg(safe)   
         print("偷饲料")
         time.sleep(3)
         subhorseplayer(safe)               
         print("喂马")
         time.sleep(3)
         horseeat(safe)
         print("送饲料")
         time.sleep(3)
         subhorseplayer1(safe)
         print("查询题库")
         time.sleep(3)
         getquesbackstatus(safe)
         print("刷新题库")
         time.sleep(3)
         getques(safe)
         print("答题")
         time.sleep(3)
         getques1(safe)
         print("答题")
         time.sleep(3)
         getques2(safe)
         print("答题")
         time.sleep(3)
         getques3(safe)
         time.sleep(3)
         infos(safe)
    else:
        print("失败")  

def headers():#请求头
    header = {
            "Host": "wxx.ball.warhorsechina.com.cn",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://servicewechat.com/wx94dca6ef07a54c55/152/page-frame.html",
            }
    return header
def infos(safe): #积分，能量信息
    url = f"https://wxx.ball.warhorsechina.com.cn/api/getusercenter.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print(f"积分:{info['nowscore']}")       
    else:
        print("失败")  

def checkin(safe): #签到
    url = f"https://wxx.ball.warhorsechina.com.cn/api/checkin.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print(info["msg"])       
    else:
        print(info["msg"])  

def joinxcx(safe): #排行榜请求
    url = f"https://wxx.ball.warhorsechina.com.cn/api/joinxcx.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])  

def getranklist(safe): #好友列表
    url = f"https://wxx.ball.warhorsechina.com.cn/api/getranklist.php?safe={safe}&type=1&fromsafe"
    header = headers()
    wx_zm_uid = []
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
        listid = info['data']
        for rw_id in listid:
            wx_zm_uid.append(rw_id['id'])  
    else:
        print(info)  
    return wx_zm_uid

# def getotherhorseinfo(safe): #添加好友
#     wx_zm_tsl = sicxs_uid()
#     wx_zm = []
#     for wx_zm_id in wx_zm_tsl:
#         time.sleep(5)
#         url = f"https://wxx.ball.warhorsechina.com.cn/api/getranklist.php?safe={safe}&type=1&fromsafe={wx_zm_id}"
#         header = {
#             "Host": "wxx.ball.warhorsechina.com.cn",
#             "Connection": "keep-alive",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
#             "Content-Type": "application/x-www-form-urlencoded",
#             "Referer": "https://servicewechat.com/wx94dca6ef07a54c55/152/page-frame.html",
#             }
#         response = requests.get(url=url,headers=header)
#         time.sleep(3)
#         response.encoding = "utf-8"
#         info = json.loads(response.text)
#         if 1 == info['status']:
#             wx_zm.append(wx_zm_id)   
#         else:
#             print(f"添加好友{wx_zm_id} 失败: {info}")
#     print(f"添加{wx_zm}成功")  

def subrank(safe): #点赞互动
    wx_zm_tsl =getranklist(safe)
    for wx_zm_id in wx_zm_tsl:
        time.sleep(5)
        url = f"https://wxx.ball.warhorsechina.com.cn/api/subrank.php?safe={safe}&id={wx_zm_id}&type=1"
        header = headers()
        response = requests.get(url=url,headers=header)
        time.sleep(3)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if 1 == info['status']:
            print(f"点赞{wx_zm_id}成功")    
        else:
            print(f"点赞{wx_zm_id} 失败: {info['msg']}")     
def share(safe): #分享小程序
    url = f"https://wxx.ball.warhorsechina.com.cn/api/share.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])  

def saveuserinfo(safe,wx_zm_avatar,wx_zm_nickname,wx_zm_sex,wx_zm_birthday,wx_zm_tel): #完善信息任务
    url = f"https://wxx.ball.warhorsechina.com.cn/api/saveuserinfo.php?safe={safe}&avatar={wx_zm_avatar}&nickname={wx_zm_nickname}&uname={wx_zm_nickname}&sex={wx_zm_sex}&birthday={wx_zm_birthday}&tel={wx_zm_tel}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print(info)       
    else:
        print(info["msg"])  
def gzhkl(safe): #公众号口令
    msg = "有能量 当燃战马！"
    url = f"https://wxx.ball.warhorsechina.com.cn/api/gzhkl.php?safe={safe}&kl={msg}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print(info)       
    else:
        print(info["msg"])   
def starthorse(safe): #领养马
    url = f"https://wxx.ball.warhorsechina.com.cn/api/starthorse.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   
def horselogin(safe): #登录养马
    url = f"https://wxx.ball.warhorsechina.com.cn/api/horselogin.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   
def strokehorse(safe): #抚摸马儿
    url = f"https://wxx.ball.warhorsechina.com.cn/api/strokehorse.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   
def horseeat(safe): #喂马
    url = f"https://wxx.ball.warhorsechina.com.cn/api/horseeat.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])  
def subhorseplayer(safe): #偷饲料
    header = headers()
    wx_zm_tsl =getranklist(safe)
    for wx_zm_id in wx_zm_tsl:
        time.sleep(5)
        url = f"https://wxx.ball.warhorsechina.com.cn/api/subhorseplayer.php?safe={safe}&friendid={wx_zm_id}&type=1"

        response = requests.get(url=url,headers=header)
        time.sleep(3)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if 1 == info['status']:
            print(f"偷饲料{wx_zm_id}成功")    
        else:
           print(f"偷饲料{wx_zm_id} 失败: {info['msg']}")
def subhorseplayer1(safe): #送饲料
    wx_zm_ssl =getranklist(safe)
    for wx_zm_id in wx_zm_ssl:
        time.sleep(5)
        url = f"https://wxx.ball.warhorsechina.com.cn/api/subhorseplayer.php?safe={safe}&friendid={wx_zm_id}&type=2"
        header = headers()
        response = requests.get(url=url,headers=header)
        time.sleep(3)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if 1 == info['status']:
               print(f"送饲料{wx_zm_id}成功")
        else:
           print(f"送饲料{wx_zm_id} 失败: {info['msg']}")


def gethorsetaskcenter(safe): #领取饲料任务签到
    url = f"https://wxx.ball.warhorsechina.com.cn/api/gethorsetaskcenter.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print(f"领取饲料：{info['checkData']['feed']},领取天数：{info['checkData']['day']}")       
    else:
        print(info["msg"]) 
def checkslgift(safe): #领互助饲料
    url = f"https://wxx.ball.warhorsechina.com.cn/api/checkslgift.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   
def sharehorse(safe): #分享公众号
    url = f"https://wxx.ball.warhorsechina.com.cn/api/sharehorse.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"]) 

def getquesbackstatus(safe): #查询题库
    url = f"https://wxx.ball.warhorsechina.com.cn/api/getquesbackstatus.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         
         print("请求成功")       
    else:
        print(info["msg"])

def getques(safe): #刷新题库
    url = f"https://wxx.ball.warhorsechina.com.cn/api/getques.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         qid = info['qid']
         question =info['question']
         options =info['options']
         sicxs_tk_up(qid,question,options)
         print(info)       
    else:
        print(info["msg"])  
       
def getques1(safe): #答题1
    url = f"https://wxx.ball.warhorsechina.com.cn/api/subques.php?safe={safe}&qid=126&val=C"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   
def getques2(safe): #答题2
    url = f"https://wxx.ball.warhorsechina.com.cn/api/subques.php?safe={safe}&qid=138&val=C"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   

def getques3(safe): #答题3
    url = f"https://wxx.ball.warhorsechina.com.cn/api/subques.php?safe={safe}&qid=119&val=A"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   

def sendbattle(safe):  #摇一摇
    url = f"https://wxx.ball.warhorsechina.com.cn/api/sendbattle.php?safe={safe}&id=2"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"])   
def getbattlemsg(safe):  #摇一摇接收信息
    url = f"https://wxx.ball.warhorsechina.com.cn/api/getbattlemsg.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
         print("成功")       
    else:
        print(info["msg"]) 
def getmyhorseinfo(safe): #获取id
    url = f"https://wxx.ball.warhorsechina.com.cn/api/getmyhorseinfo.php?safe={safe}"
    header = headers()
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 1 == info['status']:
        return info['friendid']  
    else:
        print(info["msg"]) 


def sicxs_tk_up(qid,question,options): #上传题库
    response = requests.get(url=f"https://api.sicxs.cn/i/zm/tk/qs?qid={qid}&question={question}&options={options}")
    response.encoding = "utf-8"
    info = json.loads(response.text)


def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        print("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('可以在此文件中添加配置变量，例如：\n sfsy = ""\n')
    try:
        env_cookie = os.environ.get("wx_zmnlxq")
        si_cookie = getattr(config, 'wx_zmnlxq', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_zmnlxq='' 或在 config.py 中设置 wx_zmnlxq")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_zmnlxq='' 或在 config.py 中设置 wx_zmnlxq")
        sys.exit()
    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        index(list_cookie_i)
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'----------- 账号【{i + 1}/{total_cookies}】执行领取互助饲料 -----------')
        checkslgift(list_cookie_i)
    print(f'-----------  执 行  结 束 -----------')
if __name__ == '__main__':
  sicxs()