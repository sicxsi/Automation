# name: 名创优品
# Author: sicxs
# Date: 2024-11-4
# export wx_mcyp="uid#skey" 换行，&分割 
# 抓包完成后请勿再登录小程序
# cron: 15 6 * * *
# new Env('名创优品');

import requests
import os,json,sys
import time,re
from notify import send
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

msg = []

env_name = "wx_mcyp"
TIMEOUT = 15  # 秒
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
STATUS_FORCE_LIST = [429, 500, 502, 503, 504]


# 输出文件（JSON），用于存储每日日志：{date: {tasks: [...], points: N}}
output_file = 'mcyp_task_status.json'

# ====== JSON 状态管理 ======
def today_key(): #返回日期
    return time.strftime('%Y-%m-%d')


def load_status(): #加载状态文件
    old = 'mcyp_task_status.txt'
    if old != output_file and os.path.exists(old) and not os.path.exists(output_file):
        try:
            with open(old, 'r', encoding='utf-8') as fo:
                data = json.load(fo)
            with open(output_file, 'w', encoding='utf-8') as fn:
                json.dump(data, fn, ensure_ascii=False, indent=2)
            os.remove(old)
        except Exception:
            try:
                os.rename(old, output_file)
            except Exception:
                pass

    if not os.path.exists(output_file):
        return {}

    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return {}

    # 规范化：若存在按账号存储则移除顶级 tasks/points
    for day, entry in list(data.items()):
        if isinstance(entry, dict) and any(k.isdigit() for k in entry.keys()):
            entry.pop('tasks', None)
            entry.pop('points', None)
            data[day] = entry

    return data


def save_status(status): #保存状态到 JSON 文件
    dates = sorted(status.keys(), reverse=True)[:7]
    keep = {d: status[d] for d in dates}
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(keep, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pr(f"保存状态失败: {e}")


def is_task_done_today(task_id, uid): #判断指定账号（uid）今天是否已完成某个任务（task_id）
    s = load_status().get(today_key(), {})
    if uid in s:
        tasks = s.get(uid, {}).get('tasks', [])
    else:
        tasks = s.get('tasks', [])
    return str(task_id) in set(tasks)


def mark_task_done_today(task_id, uid): #标记指定账号今天已完成某个任务，并写入状态文件。
    s = load_status()
    day = today_key()
    day_entry = s.get(day, {})
    entry = day_entry.get(uid, {'tasks': [], 'points': 0})
    if str(task_id) not in entry['tasks']:
        entry['tasks'].append(str(task_id))
    day_entry[uid] = entry
    s[day] = day_entry
    save_status(s)


def update_points_today(points, uid): #更新指定账号今天的积分到状态文件。
    s = load_status()
    day = today_key()
    day_entry = s.get(day, {})
    entry = day_entry.get(uid, {'tasks': [], 'points': 0})
    entry['points'] = points
    day_entry[uid] = entry
    s[day] = day_entry
    save_status(s)

# ====== end 状态管理 ======

# ===================== 基础配置 =====================

def get_headers(uid, skey):
    return {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781 NetType/WIFI MiniProgramEnv/Windows",
        'Content-Type': "application/json",
        'tenant': "MINISO",
        'content-uid': uid,
        'content-skey': skey,
        'Referer': "https://servicewechat.com/wx2a212470bade49bf/982/page-frame.html",
        'Accept-Language': "zh-CN,zh;q=0.9"
    }


# ===================== 签到 =====================

def index(uid, skey, session):
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/signInTask/award/receive"
    header = get_headers(uid, skey)
    data = {"activityId": "18", "taskId": 79}

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = session.post(url, headers=header, data=json.dumps(data), timeout=TIMEOUT)
            info = response.json()
        except Exception as e:
            pr(f"签到请求异常: {e}")
            return

        if info.get('code') == 200:
            pr("初始化签到中...")
            time.sleep(3)
            continue

        elif info.get('code') == 500:
            phone = re.findall(r'当前手机号(.*?)今日', info.get('message', ''))
            if phone:
                pr(f"用户名：{phone[0]}")
            pr("签到成功")
            time.sleep(2)
            task_liulan(uid, skey, session)
            time.sleep(2)
            wx_info(uid, skey, session)
            break

        else:
            pr(info.get('message', '签到失败'))
            break


# ===================== 任务 API =====================

def sicxs_id():
    url = "https://api.sicxs.cn/i/mcyp.php"
    response = requests.get(url, timeout=10)
    return response.json()


# ===================== 浏览任务 =====================

def task_liulan(uid, skey, session):
    pr("开始执行浏览任务")
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/task/uvClick"
    header = get_headers(uid, skey)

    task_list = sicxs_id()

    for task in task_list:
        task_id = task.get('msg')
        task_name = task.get('name', '未知任务')

        pr(f"浏览：{task_name}（ID：{task_id}）")

        try:
            if is_task_done_today(task_id, uid):
                pr(f"任务 {task_id} 今日已完成，跳过")
                continue
        except Exception:
            pass

        data = {
            "activityId": "18",
            "taskId": task_id,
            "taskType": 5
        }

        try:
            r = session.post(url, headers=header, data=json.dumps(data), timeout=TIMEOUT)
            info = r.json()
            time.sleep(10)

            if info.get('code') == 200:
                task_wc(uid, skey, task_id, session)
                task_lq(uid, skey, task_id, session)
            else:
                pr(f"{task_name} 失败：{info.get('message')}")

        except Exception as e:
            pr(f"{task_name} 异常跳过：{e}")
            # 异常不影响状态文件


def task_wc(uid, skey, task_id, session):
    """完成浏览"""
    url = "https://api.multibrands.miniso.com/multi-configure-platform/api/activity/task/browse/finish"
    header = get_headers(uid, skey)
    data = {"activityId": "18", "taskId": task_id}

    r = session.post(url, headers=header, data=json.dumps(data), timeout=TIMEOUT)
    info = r.json()
    time.sleep(15)

    if info.get('code') == 200:
        pr("✔ 浏览完成")
    else:
        pr("✘ 浏览失败")


def task_lq(uid, skey, task_id, session):
    """领取奖励"""
    url = "https://api-saas.miniso.com/task-manage-platform/api/activity/periodTask/award/receive"
    header = get_headers(uid, skey)
    data = {"activityId": "18", "taskId": task_id, "taskType": 5}

    r = session.post(url, headers=header, data=json.dumps(data), timeout=TIMEOUT)
    info = r.json()
    time.sleep(15)

    if info.get('code') == 200:
        pr("🎉 奖励领取成功")
        try:
            mark_task_done_today(task_id, uid)
        except Exception as e:
            pr(f"记录完成任务失败: {e}")
    else:
        pr(info.get('message', '奖励领取失败'))


# ===================== 查询 mini 币 =====================

def wx_info(uid, skey, session):
    url = "https://api-saas.miniso.com/task-manage-platform/api/virtualCoin/member"
    header = get_headers(uid, skey)

    r = session.get(url, headers=header, timeout=TIMEOUT)
    info = r.json()
    current_points = info['data']['quantity']
    pr(f"当前 mini 币：{current_points}")

    try:
        update_points_today(current_points, uid)
    except Exception as e:
        pr(f"写入积分失败: {e}")


# ====== 固定代码 ======

def pr(message):
    msg.append(message + "\n")
    print(message)

def create_session_with_retry():
    """创建带有重试机制的会话"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=STATUS_FORCE_LIST,
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def set_session_proxy(session, proxy_str):
    """为 session 设置代理，支持传入 host:port 或带协议的完整代理地址。
    如果不以 http/https/socks5 开头，默认加上 socks5:// 前缀。"""
    if not proxy_str:
        return
    p = proxy_str.strip()
    if not (p.startswith('socks5://') or p.startswith('http://') or p.startswith('https://')):
        p = 'socks5://' + p
    session.proxies.update({
        'http': p,
        'https': p,
    })
    pr(f"已设置代理: {p}")

def get_accounts():
    """固定代码，获取变量"""
    if not os.path.exists('config.py'):
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(f'#可以在此文件中添加配置变量，例如：\n{env_name} =""\n')
        print(f"未检测到环境变量，已创建配置文件config.py，请填写变量后重试。")
        sys.exit()

    import config

    env_cookie = os.environ.get(env_name, "")
    si_cookie = getattr(config, env_name, "")
    cookies = "\n".join(filter(None, [env_cookie, si_cookie]))
    if not cookies.strip():
        print(f"请设置变量 export {env_name}='' 或在 config.py 中设置 {env_name} =")
        sys.exit()

    items = [c.strip() for c in re.split(r'\n|&', cookies) if c.strip()]
    seen = set()
    accounts = []
    for c in items:
        if c not in seen:
            seen.add(c)
            accounts.append(c)
    return accounts

def sicxs():
    accounts = get_accounts()
    total = len(accounts)
    if total < 1:
        print("未检测到账号")
        return
    for i, account in enumerate(accounts, 1):
        session = create_session_with_retry()
        try:
            print(f'\n----------- 账号【{i}/{total}】执行 -----------')
            parts = account.split("#")
            if len(parts) < 2:
                print("账号格式错误,请检查设置")
                continue
            uid = parts[0]
            skey = parts[1]
            # 可选代理参数
            if len(parts) >= 3 and parts[2].strip():
                set_session_proxy(session, parts[2].strip())
            index(uid, skey, session)
        except Exception as e:
            print(f"账号【{i}/{total}】执行出错：{e}")
        finally:
            try:
                send("名创优品", ''.join(msg))
            except Exception:
                print("发送通知失败或未配置 notify")
            msg.clear()
            session.close()
    print(f'\n-----------  执 行  结 束 -----------')
if __name__ == '__main__':   
   sicxs()
