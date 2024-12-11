# name: 5E
# Author: sicxs
# Date: 2024-12-5
# export app_5e="账号#密码"
# 换行分割 
# 功能:签到，浏览任务,点赞
# cron: 20 8 * * *
# new Env('5E');

import json
import requests,random
import time,re,os,sys
import config 
s = requests.session()
def header(username,password):
    taken = app_info(username,password)
    headers = {
        "mobileModel": "{\"systemName\":\"Android\",\"mobileFactory\":\"samsung\",\"platform\":\"SM-N9700\",\"systermVersion\":\"9\"}",
        "version": "6.3.3",
        "scid": "{\"$identity_anonymous_id\":\"d6e8ef3f9ee89d6d\",\"$identity_android_id\":\"d6e8ef3f9ee89d6d\",\"identity_inid\":\"1733212415805_968f2771cd00f32c77931f134d76c8da\",\"identity_domain\":\"1114z9c5ssqq\"}",
        "equipment": "android",
        "token": taken,
        "channel": "offical",
        "dispmod": "0",
        "school": "false",
        "games": "",
        "Host": "app.5eplay.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.10.0"
        }
    headersi = {
        "mobileModel": "{\"systemName\":\"Android\",\"mobileFactory\":\"samsung\",\"platform\":\"SM-N9700\",\"systermVersion\":\"9\"}",
        "version": "6.3.3",
        "scid": "{\"$identity_anonymous_id\":\"d6e8ef3f9ee89d6d\",\"$identity_android_id\":\"d6e8ef3f9ee89d6d\",\"identity_inid\":\"1733212415805_968f2771cd00f32c77931f134d76c8da\",\"identity_domain\":\"1114z9c5ssqq\"}",
        "equipment": "android",
        "token": taken,
        "channel": "offical",
        "dispmod": "0",
        "school": "false",
        "games": "",
        "Host": "ya-api-app.5eplay.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.10.0"
        }
    headersb = {
        "mobileModel": "{\"systemName\":\"Android\",\"mobileFactory\":\"samsung\",\"platform\":\"SM-N9700\",\"systermVersion\":\"9\"}",
        "version": "6.3.3",
        "scid": "{\"$identity_anonymous_id\":\"d6e8ef3f9ee89d6d\",\"$identity_android_id\":\"d6e8ef3f9ee89d6d\",\"identity_inid\":\"1733212415805_968f2771cd00f32c77931f134d76c8da\",\"identity_domain\":\"1114z9c5ssqq\"}",
        "equipment": "android",
        "token": taken,
        "channel": "offical",
        "dispmod": "0",
        "school": "false",
        "games": "",
        "Host": "esports-data.5eplaycdn.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.10.0"
        }
    return headers,headersi,headersb
def app_info(username,password):  # 登录
    url = "https://app.5eplay.com/api/user/multi_login"
    header = {
        "mobileModel": "{\"systemName\":\"Android\",\"mobileFactory\":\"samsung\",\"platform\":\"SM-N9700\",\"systermVersion\":\"9\"}",
        "version": "6.3.3",
        "scid": "{\"$identity_anonymous_id\":\"d6e8ef3f9ee89d6d\",\"$identity_android_id\":\"d6e8ef3f9ee89d6d\",\"identity_inid\":\"1733212415805_968f2771cd00f32c77931f134d76c8da\",\"identity_domain\":\"1114z9c5ssqq\"}",
        "equipment": "android",
        "token": "",
        "channel": "offical",
        "dispmod": "0",
        "school": "false",
        "games": "",
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": "111",
        "Host": "app.5eplay.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.10.0"
        }
    data = {
        "account": username,
        "password": password,
        "reg_id": "65l2kfa3hsa3gg0", #固定值
        "token": "1733215057794", #固定值
        "type": "5"
        }
    response = requests.post(url, headers=header, json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
        return info['data']['user_token']
    else: 
        print(f"登录失败,{info['message']}")
def app_list(username,password): # 信息
    url = "https://app.5eplay.com/api/app/my_v2?deviceCode="
    headera = header(username,password)
    headers = headera[0] #通用请求头
    headeri = headera[1] #预约赛事请求头
    headerb = headera[2]#预约赛事请求头
    response = s.get(url, headers=headers)
    jifen = app_5e_d(headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if "user" in response.text:
     print(f"登录成功,用户名：{info['data']['user']['username']}")
     print(f"积分：{jifen}") #积
     app_5e_qiandao_a(headers) #签到
     app_5e_live(headers) #点赞
     app_5e_c(headers) #浏览帖子
     app_5e_c_b(headers) #浏览 资讯帖子
     app_5e_c_a(headers,headerb) #浏览赛事帖子
     app_5e_saishi(headers,headeri) #预约比赛赛事
     app_5e_a(headers)
    else:
     print(f"登录失败,{info}") 
def app_5e_qiandao_a(headers):#签到
    url = "https://app.5eplay.com/api/act_center/sign_in"
    time.sleep(3)
    response = s.post(url, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
        print("签到成功")
    else:
     print(f"失败,{info}")
def app_5e_liebiao(headers):#比赛列表
    url = "https://app.5eplay.com/api/tournament/session_list?game_status=1&limit=20&game_type=1&page=1"
    response = s.get(url, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    app_list_a = []
    matches =  info['data']['matches']
    for match in matches:
        a =  match['mc_info']['id']
        b = match['tt_info']['disp_name']
        c = match['tt_info']['id']
        app_list_a.append((a,b,c))  
    return app_list_a 
def app_5e_saishi(headers,headeri):#预约比赛赛事
    url = "https://ya-api-app.5eplay.com/v1/esport/match/sub"
    lisa_a = app_5e_liebiao(headers)
    count = 0  
    for id in lisa_a:
        count += 1
        if count == 2:
            break  
        data = {
            "game_type": "csgo",
            "mc_id": id[0],
            "switch_status": 1
        }
        response = s.post(url, headers=headeri, json=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if info['success']:
            print(f"预约比赛{id[1]}成功")
        else:
            print(f"{id[1]}失败,{info['message']}")
def app_5e_list_a(headers):#帖子列表
    url = "https://app.5eplay.com/api/forum/index?obj_sn&id=0&page=1"
    response = s.get(url, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    list_a = []
    if info['success']:
       a = info['data']['content']['list'][3]['cm_forum']['tid'],info['data']['content']['list'][3]['cm_forum']['title']
       b = info['data']['content']['list'][4]['cm_forum']['tid'],info['data']['content']['list'][4]['cm_forum']['title']
       c = info['data']['content']['list'][5]['cm_forum']['tid'],info['data']['content']['list'][5]['cm_forum']['title']
       list_a.append((a))
       list_a.append((b))
       list_a.append((c))
       return list_a
    else:
     print(f"失败,{info['message']}")

def app_5e_list_b(headers):#资讯帖子
    url = "https://app.5eplay.com/api/csgo/content/person?domain=csgo_c9xugb&page=1"
    response = s.get(url, headers=headers)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    app_list_a = []
    if info['success']:
        a = info['data']['list'][0]['alias'],info['data']['list'][0]['title']
        b = info['data']['list'][1]['alias'],info['data']['list'][1]['title']
        c = info['data']['list'][2]['alias'],info['data']['list'][2]['title']
        app_list_a.append((a))
        app_list_a.append((b))
        app_list_a.append((c)) 
        return app_list_a 
    else:
      print(f"失败,{info['message']}")

def app_5e_live(headers):#点赞
    url = "https://app.5eplay.com/api/csgo/likes"
    a = app_5e_list_a(headers)
    for i in a:
        data = {
            "from_type": "13",
            "from_id": i[0],
            "like_type": "0",
            "do_type": "1"
            }
        time.sleep(5)
        response = s.post(url, headers=headers,data=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if info['success']:
            print(f"点赞文章：{i[1]} ✅")
        else:
             print(f"点赞文章： {i[1]} ❎,{info['message']}")

def app_5e_a(headers):#领取奖励
    a = app_5e_b(headers)
    id = a[1]
    ic = a[0]
    for i in ic:
        if i[2]:
            url = f"https://app.5eplay.com/api/act_center/receive/app_task_center_rcrwnew"
            time.sleep(3)
            data = {
            "act_id": id[0],
            "task_id": i[0]
            }
            response = s.post(url, headers=headers,json=data)
            response.encoding = "utf-8"
            info = json.loads(response.text)
            if info['success']:
                print(f"{i[1]}领取成功✅")
            else:
                print(f"{i[1]},{info['message']} ❎")
        else:
            print(f"{i[1]},任务未完成❎")        

def app_5e_b(headers):#获取任务列表
   url = "https://app.5eplay.com/api/act_center/list/app_task_center_new"
   response = s.get(url, headers=headers)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   time.sleep(3)
   if info['success']:
      list_a = []
      for i in info['data']['task'][0]['task']:
         list_a.append((i['task_id'],i['desc'],i['is_finish'],i['title'],i['event']))
      a = []
      a.append((info['data']['task'][0]['act_id']))
      return list_a,a
   else:
       print("获取任务列表失败")

def app_5e_c(headers): #浏览帖子
    print("开始浏览帖子")
    a = app_5e_list_a(headers)
    for i in a:
        
        url = f"https://app.5eplay.com/api/csgo/forum/topic/{i[0]}"
        response = s.get(url, headers=headers)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        
        time.sleep(random.randint(60, 80))
        if info['success']:
         print(f"浏览：{i[1]} ✅")
        else:
         print(f"浏览：{i[1]} ❎ {info}")     
def app_5e_c_a(headers,headerb): #浏览赛事
    print("开始浏览赛事帖子")
    a = app_5e_liebiao(headers)
    count = 0
    for i in a:
     count += 1
     if count == 4:
        break  
     url = f"https://app.5eplay.com/api/csgo/tournament/csgo_event_list?is_follow=0&tt_ids={i[2]}&page=1&page_size=1"
     response = s.get(url, headers=headers)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     time.sleep(random.randint(60, 80))
     if info['success']:
         print(f"浏览：{i[1]} ✅")
     else:
         print(f"浏览：{i[1]} ❎ {info}")     
def app_5e_c_b(headers): #资讯浏览
    print("开始资讯帖子")
    a =  app_5e_list_b(headers)
    count = 0
    for i in a:
     count += 1
     if count == 4:
        break  
     url = f"https://app.5eplay.com/api/csgo/content/detail/{i[0]}"
     response = s.get(url, headers=headers)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     time.sleep(random.randint(60, 80))
     if info['success']:
         print(f"浏览：{i[1]} ✅")
     else:
         print(f"浏览：{i[1]} ❎ {info['message']}")     

def app_5e_d(headers): #积分
   url = "https://app.5eplay.com/api/mall/exchange_log?pageSize=20&page=1"
   response = s.get(url, headers=headers)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   if info['success']: 
    return info['data']['user_info']['can_use_score']
   else: 
    print('访问失败')


def sicxs():
    try:
        env_cookie = os.environ.get("app_5e")
        si_cookie = getattr(config, 'app_5e', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "&" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export app_5e='' 或在 config.py 中设置 app_5e =")
            sys.exit()
    except Exception as e:
        print("请设置变量 export app_5e='' 或在 config.py 中设置 app_5e =")
        sys.exit()

    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            list = list_cookie_i.split("#")
            app_list(list[0], list[1])
        except Exception as e:
            print(f"账号【{i + 1}/{total_cookies}】执行出错：账号密码错误，或者账号被封禁，请检查后重试！")    

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
    sicxs()