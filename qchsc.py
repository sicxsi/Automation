# name: 七彩虹商城
# Author: sicxs
# Date: 2024-11-10
# export wx_qch="Authorization#X-Authorization" &,@换行分割  不要填Bearer 
# export wx_qch_cj="true"  抽奖，默认不抽奖
# 测试ck 5天就过期，后续再看
# 完善信息自己做一下
# 发帖，回帖接口可以自行更换
# cron: 20 8 * * *
# new Env('七彩虹商城');

import requests
import re,time
import os,sys,json
import random
import config
s = requests.session()
def index(Authorization,Authorizationx,qch_cj): #登录信息
    url = "https://shop.skycolorful.com/api/User/GetUserInfo"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "User-from": "xcx",
        "source": "Wx",
        "Authorization": f"Bearer {Authorization}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
        }
    response = s.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    s1 = response.status_code
    if s1 == 200:
     if 0 == info['Code']:
        print(f"用户名: {info['Data']['NickName']},经验值：{info['Data']['Growth']},积分：{info['Data']['Point']}")  
        qc_Mobile = info['Data']['Mobile']
        time.sleep(3)
        rw_PostReply(Authorization,Authorizationx)
        print("开始签到任务")
        time.sleep(3)
        qiandao(Authorization,Authorizationx)
        time.sleep(3)
        #print("开始信息完善任务")
        #time.sleep(3)
        # DoEditInfo(Authorization,Authorizationx,qc_time,qc_name)
        time.sleep(3)
        print("开始发贴任务")
        time.sleep(3)
        GetBanner(Authorization,Authorizationx,qc_Mobile)
        time.sleep(15)
        print("开始回帖任务")
        time.sleep(3)
        PostReply(Authorization,Authorizationx)  #三次吧？
        time.sleep(30)
        PostReply(Authorization,Authorizationx)
        time.sleep(30)
        PostReply(Authorization,Authorizationx)
        print("开始点赞任务")
        time.sleep(5)
        Like(Authorization,Authorizationx)
        time.sleep(5)
        Like(Authorization,Authorizationx)
        time.sleep(5)
        Like(Authorization,Authorizationx)
        time.sleep(5)
        Like(Authorization,Authorizationx)
        time.sleep(5)
        Like(Authorization,Authorizationx)
        if True == qch_cj:
            print("开启抽奖抽奖")
            time.sleep(3)
            LuckyDraw(Authorization,Authorizationx)
            time.sleep(3)
            LuckyDraw(Authorization,Authorizationx)
        else:
            print("默认不抽奖")
        time.sleep(30)   
        userinfo(Authorization,Authorizationx)    
     else:
        print("登陆失败，请检查Authorization")  
    else:
        print("登陆失败，请检查Authorization")  
def qiandao(Authorization,Authorizationx): #签到任务
    url = "https://shop.skycolorful.com/api/User/SignV2"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "source": "Wx",
        "Authorization":f"Bearer {Authorization}",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        }

    response = s.post(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['Code']:
        print(info['Message'])  
    else:
        print(info['Message'])  
def DoEditInfo(Authorization,Authorizationx,qc_time,qc_name): #信息完善
    url = "https://shop.skycolorful.com/api/User/DoEditInfo"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "source": "Wx",
        "Authorization":f"Bearer {Authorization}",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        }
    data = {
        "Birthday": qc_time,
        "Nickname": qc_name,
        "Sex": 1
        }

    response = s.post(url=url,headers=header,json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['Code']:
        print(info['Message'])  
    else:
        print(info['Message'])  
def PostReply(Authorization,Authorizationx): #回帖任务
    url ="https://shop.skycolorful.com/api/Bbs/PostReply"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "source": "Wx",
        "Authorization":f"Bearer {Authorization}",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        }
    PostId = sicxs_uid()
    yiyanurl = "http://api.sicxs.cn/wy/du.php"
    response1 = s.get(url=yiyanurl)
    yiyan = response1.text
    data = {
        "PostId": PostId,
        "ReplyId": "",
        "ParentReplyId": "",
        "Content":yiyan,
        "Pictures": []
        }

    response = s.post(url=url,headers=header,json=data)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['Code']:
        print(f"回帖{PostId}{yiyan}")  
    else:
        print(info['Message'])      
def GetBanner(Authorization,Authorizationx,qc_Mobile):# 发帖任务
    url = "https://shop.skycolorful.com/api/Bbs/Posting"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "source": "Wx",
        "Authorization":f"Bearer {Authorization}",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        }
    yiyanurl = "http://api.sicxs.cn/wy/du.php"
    response1 = s.get(url=yiyanurl)
    yiyan = response1.text
    data = {
        "ModuleId":"09539c50-6de2-4a0c-adc8-535e488a419e", #暂定测试
        "Phone": qc_Mobile,
        "Title": "一言",
        "Content": yiyan,
        "Pictures": [],
        "Topic": "",
        "Source": 30
        }

    response = s.post(url=url,headers=header,json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['Code']:
        print("发帖成功")  
    else:
        print(info['Message'])    
def rw_PostReply(Authorization,Authorizationx): #获取回帖ID列表
    url ="https://shop.skycolorful.com/api/Bbs/GetUserPostingList?Page=1&Size=10"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "source": "Wx",
        "Authorization":f"Bearer {Authorization}",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        }

    response = s.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    try:
        if 0 == info['Code']:
         s1 = info['Data']['DataList'][0]['Id']
         sicxs_uid_up(s1)
        else:
            print(info['Message']) 
    except Exception as e:
          print("上传帖子id失败") 
def GetPageList(Authorization,Authorizationx): #获取活动ID列表
    wx_list = []
    url = "https://shop.skycolorful.com/api/Activity/GetPageList?Page=1&Limit=10"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "source": "Wx",
        "Authorization": f"Bearer {Authorization}",
         "X-Authorization": f"Bearer {Authorizationx}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
    }

    response = s.get(url=url, headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)

    if info['Code'] == 0:
        listid = info['Data']['DataList']
        for item in listid:
            wx_list.append(item['ActivityKey'])
    else: 
        print(info['Message']) 
    return wx_list
def LuckyDraw(Authorization,Authorizationx): #抽奖
    qc_cjhd = []
    url ="https://shop.skycolorful.com/api/LuckyDraw/Do"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "source": "Wx",
        "Authorization":f"Bearer {Authorization}",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        }
    qc_key = GetPageList(Authorization,Authorizationx) 
    for qc_key_i in qc_key:
        data = {"Key":qc_key_i}
        response = s.post(url=url,headers=header,json=data)
        time.sleep(3)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if 0 == info['Code']:
            qc_cjhd.append(qc_key_i)
            qc_cjhd.append(info['Data']['Name'])  
        else:
            print(info['Message'])
    print(qc_cjhd)    
def userinfo(Authorization,Authorizationx): #积分，经验住更新
    url = "https://shop.skycolorful.com/api/User/GetUserInfo"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "User-from": "xcx",
        "source": "Wx",
        "Authorization": f"Bearer {Authorization}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
        }
    response = s.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['Code']:
        print(f"任务结束,经验值: {info['Data']['Growth']},积分：{info['Data']['Point']}")  
    else:
       print("登陆失败,请检查Authorization")  
def Like(Authorization,Authorizationx): #点赞
    url = "https://shop.skycolorful.com/api/Bbs/Like"
    header = {
        "Host": "shop.skycolorful.com",
        "Connection": "keep-alive",
        "version": "2.0.0",
        "User-from": "xcx",
        "source": "Wx",
        "Authorization": f"Bearer {Authorization}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "X-Authorization": f"Bearer {Authorizationx}",
        "Referer": "https://servicewechat.com/wx49018277e65fc3e1/66/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
        }
    PostId = sicxs_uid()
    data = {
     "postId": f"{PostId}",
     "postReplyId": "0"
        }
    response = s.post(url=url,headers=header,json=data)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['Code']:
        print("成功")  
    else:
       print("登陆失败,请检查Authorization")  
def sicxs_uid_up(id): #上传到远程id库
    response = requests.get(url=f"http://api.sicxs.cn/i/qch/?id={id}")
    response.encoding = "utf-8"
    info = json.loads(response.text)
def sicxs_uid(): #获取远程id
    response = requests.get(url="http://api.sicxs.cn/i/qch/")
    time.sleep(3)
    listid = response.text
    return listid
    
def sicxs():
    try:
        env_cookie = os.environ.get("wx_qch")
        si_cookie = getattr(config, 'wx_qch', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_qch='' 或在 config.py 中设置 wx_qch =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export app_wx_qch5e='' 或在 config.py 中设置 wx_qch =")
        sys.exit()

    if os.environ.get("wx_qch_cj"):
        wx_qch_cj = os.environ.get("wx_qch_cj")
        if wx_qch_cj == "true" :
            print("执行抽奖任务。")
            wx_qch_cj = True
        elif wx_qch_cj  == "false":
            wx_qch_cj = False
        else:
            wx_qch_cj = False
            print("你输入的错误，执行默认设置")
    else:
        wx_qch_cj = False
        
    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            list = list_cookie_i.split("#")
            index(list[0], list[1],wx_qch_cj)
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错")    

    print(f'\n-----------  执 行  结 束 -----------')




if __name__ == '__main__':
       
 sicxs()
