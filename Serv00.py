# name: Serv00
# Author: sicxs
# Date: 2024-12-22
# export Serv00=""
# 换行分割 
# 功能：登录保活
# cron: 0 0 7 * *
# new Env('Serv00 保活');

import paramiko
import time,re,os,sys
import config
from notify import send


msg = []
def index(hostname, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        time.sleep(3)
        msg.append("登录成功")
        stdin, stdout, stderr = ssh.exec_command('ls')
        msg.append("查看目录")
        time.sleep(3)
        print(stdout.read().decode())
        time.sleep(3)
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        msg.append("认证失败，用户名或密码错误")
        return False
    except paramiko.SSHException as ssh_ex:
        msg.append(f"SSH连接失败: {ssh_ex}")
        return False
    except Exception as ex:
        msg.append(f"发生错误: {ex}")
        return False


def sicxs():
    try:
        env_cookie = os.environ.get("Serv00")
        si_cookie = getattr(config, 'Serv00', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            msg.append("请设置变量 export Serv00='' 或在 config.py 中设置 Serv00 =")
            sys.exit()
    except Exception as e:
        msg.append("请设置变量 export Serv00='' 或在 config.py 中设置 Serv00 =")
        sys.exit()

    list_cookie = re.split(r'\n|&', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            list = list_cookie_i.split("#")
            if index(list[0], list[1],list[2],list[3]):
                msg.append(f"{list[2]} 执行保活任务成功")
            else:
                msg.append(f"{list[2]} 执行保活任务失败")    
        except Exception as e:
            msg.append(f"账号【{i + 1}/{total_cookies}】执行出错")    
        send("Serv00保号信息",msg)    
    print(f'\n-----------  执 行  结 束 -----------')


if __name__ == '__main__':
   sicxs()