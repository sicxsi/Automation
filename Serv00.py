# name: Serv00
# Author: sicxs
# Date: 2024-12-22
# export Serv00=""
# 换行分割 
# 功能：登录保活
# cron: 0 0 0 */7 * 
# new Env('Serv00 保活');

import paramiko
import re
import os
import sys
import config
from notify import send

def log_and_append(message):
    msg.append(message)
    print(message)

msg = []

def index(hostname, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        log_and_append("登录成功")
        
        stdin, stdout, stderr = ssh.exec_command('ls')
        log_and_append("\n查看目录")
        
        output = stdout.read().decode()
        log_and_append(output)
        
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        log_and_append("认证失败，用户名或密码错误")
        return False
    except paramiko.SSHException as ssh_ex:
        log_and_append(f"SSH连接失败: {ssh_ex}")
        return False
    except Exception as ex:
        log_and_append(f"发生错误: {ex}")
        return False

def get_cookies():
    env_cookie = os.environ.get("Serv00")
    si_cookie = getattr(config, 'Serv00', '')
    
    if env_cookie and si_cookie:
        return env_cookie + "\n" + si_cookie
    elif env_cookie:
        return env_cookie
    elif si_cookie:
        return si_cookie
    else:
        log_and_append("请设置变量 export Serv00='' 或在 config.py 中设置 Serv00 =")
        sys.exit()

def sicxs():
    cookies = get_cookies()
    list_cookies = re.split(r'\n|&', cookies)
    total_cookies = len(list_cookies)
    
    for i, cookie in enumerate(list_cookies):
        try:
            print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
            host, port, user, pwd = cookie.split("#")
            if index(host, int(port), user, pwd):
                log_and_append(f"{user} 执行保活任务成功")
            else:
                log_and_append(f"{user} 执行保活任务失败")
        except Exception as e:
            log_and_append(f"账号【{i + 1}/{total_cookies}】执行出错: {e}")
    
    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
    sicxs()
    send("Serv00 保活", ''.join(msg))