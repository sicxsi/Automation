# name: 张拉拉牛肉面
# Author: sicxs
# Date: 2024-11-9
# 微信小程序
# export wx_zll="token"  多账户@,&分割 
# 签到得积分，和红包,建议修改一下小程序昵称
# token过期3-5天
# cron: 15 8 * * *
# new Env('张拉拉牛肉面');

import requests
import os,sys,time
import json,re
import config

def inde(token):#登录信息
     url = 'https://zllapi.zhanglala.cn/biz/weixin/wxuser/userInfo'
     header = {
            "authority": "zllapi.zhanglala.cn",
            "method": "GET",
            "path": "/biz/weixin/wxuser/userInfo",
            "scheme": "https",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "token": token,
            "referer": "https://servicewechat.com/wx2a7ce3726b24ff3c/97/page-frame.html",
            }

     response = requests.get(url=url,headers=header)
     info = json.loads(response.text)
     if 0 == info['code']:
        print(f"登陆成功,账号：{info['data']['wxNickName']}") 
        time.sleep(2) 
        qiandao1(token)
        time.sleep(2) 
        qiandao(token)
     else:
        print(f"登录失败,{info}")


def qiandao(token):#签到
     url = "https://zllapi.zhanglala.cn/biz/weixin/cdb/signin/get"
     header = {
            "authority": "zllapi.zhanglala.cn",
            "method": "GET",
            "path": "/biz/weixin/cdb/signin/get",
            "scheme": "https",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "token": token,
            "referer": "https://servicewechat.com/wx2a7ce3726b24ff3c/97/page-frame.html",
            }
     response = requests.get(url=url,headers=header)
     info = json.loads(response.text)
     if info['data']['signIn']:
        print(f"签到成功,你已签到：{info['data']['continuous']}天")  
     else:
        print("正在签到，请稍等。")
        time.sleep(3)
        qiandao1(token)
def qiandao1(token):#初始化签到
     url = "https://zllapi.zhanglala.cn/biz/weixin/cdb/signin"
     idem_tokens = idem_token(token)
     header = {
            "authority": "zllapi.zhanglala.cn",
            "method": "GET",
            "path": "/biz/weixin/cdb/signin",
            "scheme": "https",
            "idem_token":idem_tokens,
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "token": token,
            "referer": "https://servicewechat.com/wx2a7ce3726b24ff3c/97/page-frame.html",
            }
     response = requests.get(url=url,headers=header)
     info = json.loads(response.text)
     if 0 == info['code']:
        print("初始化签到")  
     else:
        print(info['msg'])

def idem_token(token):#获取idem_token
     url = "https://zllapi.zhanglala.cn/biz/base/get/token"
     header = {
            "authority": "zllapi.zhanglala.cn",
            "method": "GET",
            "path": "/biz/base/get/token",
            "scheme": "https",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "token": token,
            "referer": "https://servicewechat.com/wx2a7ce3726b24ff3c/97/page-frame.html",
            }
     response = requests.get(url=url,headers=header)
     info = json.loads(response.text)
     if 0 == info['code']:
        return info['data']
     else:
        print(f"失败{info['msg']}")

def sicxs():
    try:
        env_cookie = os.environ.get("wx_zll")
        si_cookie = getattr(config, 'wx_zll', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export wx_zll='' 或在 config.py 中设置 wx_zll")
            sys.exit()
    except Exception as e:
        print("请设置变量 export wx_zll='' 或在 config.py 中设置 wx_zll")
        sys.exit()
    list_cookie = re.split(r'\n|&|@', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        try:
            inde(list_cookie_i)
        except Exception as e:
            print(f"执行账号【{i + 1}】时发生错误: {e}")

    print(f'\n-----------  执 行  结 束 -----------')
if __name__ == '__main__':
  sicxs()