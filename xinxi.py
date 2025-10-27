# name: 心喜
# Author: sicxs
# Date: 2024-11-9
# 微信小程序
# export wx_xx="sso" 
# 抓小程序 -> 我的 sso值  抓到后最好不要进小程序
# 多号 @,&分割 
# 加入星期判断 到时间运行任务，防止封号
# 可以自己更改发帖和评论接口。
# cron: 16 8 * * *
# new Env('心喜');
import requests
import json,os,sys,re
import time
def index(sso):#登录信息
    current_time = time.localtime()
    current_weekday = current_time.tm_wday
    url = "https://api.xinc818.com/mini/user"
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini/user",
        "scheme": "https",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
        print(f"登陆成功，用户名：{info['data']['nickname']},积分：{info['data']['integral']}")
        qx_gz_id = info['data']['id']
        print("开始签到")
        xy_qiandao(sso)
        time.sleep(3)
        if current_weekday == 0:  # 周一
         print("开始想要任务")
         time.sleep(3)
         xy_dj(sso)
        if current_weekday == 1:
          print("开始关注任务，随机关注3个幸运儿")
          time.sleep(3)
          xy_follow(sso)
        print("开始点赞任务，随机三篇文章")
        time.sleep(3)
        xy_dz(sso)
        time.sleep(3)
        if current_weekday == 2:
         print("开始分享任务")
         time.sleep(3)
         xy_fenxiang(sso)
         time.sleep(3)
         xy_fenxiang(sso)
        time.sleep(3)
        print("查看会员权益任务")
        time.sleep(3)
        xy_vip(sso)
        time.sleep(3)
        if current_weekday == 2:
         print("开始浏览商城任务")
         time.sleep(3)
         xy_sc_ll(sso)
         time.sleep(30)
         xy_sc_ll(sso)
         time.sleep(30)
        if current_weekday == 0:
         print("开始发帖任务")
         time.sleep(3)
         xy_fatie(sso)
         time.sleep(3)
        elif current_weekday == 3:
           print("开始发帖任务")
           time.sleep(3)
           xy_fatie(sso)
           time.sleep(3)
        elif current_weekday == 5:
           print("开始发帖任务")
           time.sleep(3)
           xy_fatie(sso)
           time.sleep(3)
        if current_weekday == 0:
         print("开始评论任务")
         time.sleep(3)
         xy_pinglun(sso)
         time.sleep(3)
        if current_weekday == 3:
         print("开始取消关注，随机取关3个幸运儿")
         time.sleep(3)
         qx_follow(sso,qx_gz_id)
         time.sleep(3)
        xy_info(sso)
    else:
       print(info['msg'])  
def xy_qiandao(sso):#签到
    url = "https://api.xinc818.com/mini/sign/in?dailyTaskId"
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini//sign/in?dailyTaskId",
        "scheme": "https",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
      print("签到成功")
    else:
      print(info['msg'])
def xy_sc_ll(sso):#商城浏览
    url = "https://api.xinc818.com/mini/dailyTask/browseGoods/22"
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini/dailyTask/browseGoods/22",
        "scheme": "https",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
      print("浏览成功")
    else:
      print(info['msg'])
def xy_vip(sso): #会员权益
    url = "https://api.xinc818.com/mini/dailyTask/benefits/2"
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini/dailyTask/benefits/2",
        "scheme": "https",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
      print("查看成功")
    else:
      print(info['msg'])
def xy_fenxiang(sso): #分享
    url = "https://api.xinc818.com/mini/dailyTask/share"
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini/dailyTask/share",
        "scheme": "https",
        "request_id": "u4po91maf-1731168359324",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
      print("分享成功")
    else:
      print(info['msg'])
def xy_dz(sso):#点赞
    url = "https://api.xinc818.com/mini/posts/like"
    xy_uid = []
    header = {
        "authority": "api.xinc818.com",
        "method": "PUT",
        "path": "/mini/posts/like",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    wx_dz_list = xy_dzlist(sso)
    for dz_id in wx_dz_list:
      data = {"postsId":dz_id,"decision":True}
      response = requests.put(url=url,headers=header,json=data)
      time.sleep(3)
      response.encoding = "utf-8"
      info = json.loads(response.text)
      if 0 == info['code']:
         xy_uid.append(dz_id)
      else:
         print(f"点赞 {xy_uid} 失败: {info['msg']}")
    print(f"点赞 {xy_uid}成功")
def xy_dzlist(sso):#获取点赞列表id
    url = "https://api.xinc818.com/mini/community/home/posts?pageNum=1&pageSize=10&queryType=1&position=2" 
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini/community/home/posts?pageNum=1&pageSize=10&queryType=1&position=2",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }   
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
       wx_list = []
       #文章ID
       wx_list.append(info['data']['list'][0]['id']) 
       wx_list.append(info['data']['list'][1]['id'])
       wx_list.append(info['data']['list'][2]['id'])
       return wx_list
    else:
       print(info['msg']) 
def xy_id(sso):#获取想要商品id列表
    url = "https://cdn-api.xinc818.com/mini/integralGoods?orderField=sort&orderScheme=DESC&pageSize=10&pageNum=1"
    xy_uid = []
    header = {
            "Host": "cdn-api.xinc818.com",
            "sso": sso,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 ==info['code']:
       #商品ID
       xy_uid.append(info['data']['list'][0]['id'])
       xy_uid.append(info['data']['list'][1]['id'])
       xy_uid.append(info['data']['list'][2]['id'])
       return xy_uid
    else:
       print(info['msg']) 
def xy_outerId(sso):#获取想要id
    wx_xy_id = xy_id(sso)
    outer_ids = [] 
    for xy_id_uid in wx_xy_id:
       url =f"https://api.xinc818.com/mini/integralGoods/{xy_id_uid}?type"
       header = {
             "authority": "api.xinc818.com",
            "method": "GET",
            "sso": sso,
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "content-type": "application/json",
            "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
            }
       response = requests.get(url=url,headers=header)
       time.sleep(3)
       response.encoding = "utf-8"
       info = json.loads(response.text)
       if 0 ==info['code']:
         outer_id = info['data']['outerId']
         outer_ids.append(outer_id) 
    return outer_ids
def xy_dj(sso):#点击想要
    url = "https://api.xinc818.com/mini/live/likeLiveItem"
    xy_ids = [] 
    header ={
            "authority": "api.xinc818.com",
            "method": "POST",
            "path": "/mini/live/likeLiveItem",
            "sso": sso,
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "content-type": "application/json",
            "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
            }
    wx_xy_id = xy_outerId(sso)
    for xy_id_uid in wx_xy_id:
       data = {"isLike":True,"dailyTaskId":20,"productId":xy_id_uid}
       time.sleep(3)
       response = requests.post(url=url,headers=header,json=data)
       time.sleep(3)
       response.encoding = "utf-8"
       info = json.loads(response.text)
       try:
            if 0 == info['code']:
                xy_ids.append(xy_id_uid)
            else:
              print(f"点击想要 {xy_id_uid} 失败: {info['msg']}")
       except json.JSONDecodeError:
            print(f"响应解析失败: {response.text}")
    print(f"点击想要 {xy_ids}成功")
def xy_follow(sso): #关注  
    url = "https://api.xinc818.com/mini/user/follow"
    xy_uid = []
    header = {
        "authority": "api.xinc818.com",
        "method": "PUT",
        "path": "/mini/user/follow",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    wx_list = xy_pageNum(sso)
    for user_id in wx_list:
      data = {
        "decision": True,
        "followUserId": user_id
         }
      response = requests.put(url=url,headers=header,json=data)
      time.sleep(3)
      response.encoding = "utf-8"
      info = json.loads(response.text)
      if 0 == info['code']:
         xy_uid.append(user_id)
      else:
         print(f"关注用户 {user_id} 失败: {info['msg']}")
    print(f"成功关注用户 {xy_uid}")
def xy_pageNum(sso): #关注任务ID
    url = "https://api.xinc818.com/mini/community/home/posts?pageNum=1&pageSize=10&queryType=1&position=2" 
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini/community/home/posts?pageNum=1&pageSize=10&queryType=1&position=2",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }   
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
       wx_list = []
       #用户ID
       wx_list.append(info['data']['list'][0]['publisherId'])
       wx_list.append(info['data']['list'][1]['publisherId'])
       wx_list.append(info['data']['list'][2]['publisherId'])
       return wx_list
    else:
       print(info['msg']) 
def qx_follow(sso,qx_gz_id):#取消关注
    url = "https://api.xinc818.com/mini/user/follow"
    qx_uid = []
    header = {
        "authority": "api.xinc818.com",
        "method": "PUT",
        "path": "/mini/user/follow",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    wx_list = qx_pageNum(sso,qx_gz_id)
    for user_id in wx_list:
        data = {
        "decision": False,
        "followUserId": user_id
         }
        response = requests.put(url=url,headers=header,json=data)
        time.sleep(3)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        try:
            info = json.loads(response.text)
            if 0 == info['code']:
                qx_uid.append(user_id)
            else:
                print(f"取消关注用户 {user_id} 失败: {info['msg']}")
        except json.JSONDecodeError:
            print(f"响应解析失败: {response.text}")
    print(f"成功取消关注用户 {qx_uid}")        
def qx_pageNum(sso,qx_gz_id): #获取消关注列表
    url = f"https://api.xinc818.com/mini/personalAuthor/home/follow?type=1&userId={qx_gz_id}&pageNum=1&pageSize=20" 
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": f"/mini/personalAuthor/home/follow?type=1&userId={qx_gz_id}&pageNum=1&pageSize=20",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }   
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
       wx_list = []
       #用户ID
       wx_list.append(info['data']['list'][0]['id'])
       wx_list.append(info['data']['list'][1]['id'])
       wx_list.append(info['data']['list'][2]['id'])
       return wx_list
    else:
       print(info['msg']) 
def xy_fatie(sso): #发帖
   timestamp = int(time.time() * 1000)
   yiyanurl = "https://api.sicxs.cn/wy/wenrou.php"
   response1 = requests.get(url=yiyanurl)
   yiyan = response1.text
   print(f"本次文章，{yiyan}")
   url = "https://api.xinc818.com/mini/posts"
   header = {
        "authority": "api.xinc818.com",
        "method": "POST",
        "path": "/mini/posts",
        "scheme": "https",
        "content-length": "189",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
   data = {
        "topicNames": [
            "心情树洞"
        ],
        "content": yiyan,
        "groupId": 0,
        "groupClassifyId": 0,
        "attachments": [],
        "voteType": 0,
        "commentType": "0",
        "platform": "windows",
        "sid": timestamp
        }
   response = requests.post(url=url,headers=header,json=data)
   time.sleep(3)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   if 0 == info['code']:
      print("提交成功，等待审核")
   else:
       print(info['msg']) 
def xy_pinglun(sso): #评论
    url = "https://api.xinc818.com/mini/postsComments"
    header = {
        "authority": "api.xinc818.com",
        "method": "POST",
        "path": "/mini/postsComments",
        "scheme": "https",
        "content-length": "189",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    xy_pl = []
    wx_dz_list = xy_dzlist(sso)
    for dz_id in wx_dz_list:
        yiyanurl = "https://api.sicxs.cn/wy/wenrou.php"
        response1 = requests.get(url=yiyanurl)
        yiyan = response1.text
        data = {"content":yiyan,"postsId":dz_id}
        response = requests.post(url=url,headers=header,json=data)
        time.sleep(3)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if 0 == info['code']:
           xy_pl.append(dz_id)
           xy_pl.append(yiyan)
        else:
            print(info['msg']) 
    print(f"评论{xy_pl} 成功，等待审核")       
def xy_info(sso): #积分
    url = "https://api.xinc818.com/mini/user"
    header = {
        "authority": "api.xinc818.com",
        "method": "GET",
        "path": "/mini/user",
        "scheme": "https",
        "sso": sso,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "content-type": "application/json",
        "referer": "https://servicewechat.com/wx673f827a4c2c94fa/291/page-frame.html",
        }
    response = requests.get(url=url,headers=header)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if 0 == info['code']:
        print(f"任务已完成，用户名：{info['data']['nickname']},积分：{info['data']['integral']}")
    else:
       print(info['msg'])  

def sicxs():
    config_path = 'config.py'
    if os.path.exists(config_path):
      import config  
    else:
      with open(config_path, 'w') as f: 
        print("首次运行，已创建配置文件 config.py，请按照说明填写相关变量后再次运行脚本。")
        f.write('可以在此文件中添加配置变量，例如：\n sfsy = ""\n')
    try:
        env_cookie = os.environ.get("wx_xx")
        si_cookie = getattr(config, 'wx_xx', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_xx='' 或在 config.py 中设置 wx_xx")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_xx='' 或在 config.py 中设置 wx_xx")
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