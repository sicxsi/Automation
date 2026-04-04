# 脚本合集说明

本仓库收录了多个常用站点的自动签到/任务脚本，支持青龙面板与本地 Python 环境运行。
本仓库代码都是AI生成，封号概不负责。

---

## 脚本列表

| 脚本名         | 功能简介           | 目标网址/平台                        |
| -------------- | ------------------ | ------------------------------------ |
| 白鲸鱼回收     | 自动签到     | 微信小程序             |
| 科技玩家       | 自动签到     | https://www.kejiwanjia.com           |
| 恩山无线论坛   | 自动签到           | https://www.right.com.cn             |
| 飞牛nas        | 自动签到           | https://www.fenew.com                |
| 隔壁网         | 自动签到           | https://www.gebi1.com                |
| 海胆           | 自动签到           | https://www.haidan.video             |
| 杜比           | 自动签到           | https://www.hddolby.com              |
| 家园           | 自动签到           | https://www.hdhome.org               |
| 全球主机论坛   | 自动签到           | https://hostloc.com                  |
| 回收猿回收     | 自动签到           | 微信小程序                |
| 葫芦侠三楼     | 自动签到           | app           |
| 精益论坛       | 自动签到           | https://www.jylt.com                 |
| 铃音           | 自动签到           | https://pt.soulvoice.club            |
| 通信人家园     | 自动登录           | https://txrjy.com                    |
| 名创优品          | 自动签到           | 微信小程序            |


---

## 青龙面板使用方法



## 本地运行方法

1. **安装依赖**  
   需安装 Python 3.7+，并安装依赖：
   ```bash
   pip install requests
   ```

2. **配置变量**  
   - 新建 `config.py` 文件，按脚本注释填写变量，例如：
     ```python
     wx_bjyhs ="auth1#username1\nauth2#username2"
     wy_rigth="cookie"
     ```
   - 或设置环境变量（如 `export wx_bjyhs="..."`）。

3. **运行脚本**  
   ```bash
   python 脚本名.py
   ```

4. **查看结果**  
   - 运行结果会在控制台输出。
   - 部分脚本会生成 json 记录文件。

---

## 说明

- 多账号支持：变量用换行或 `&` 分割。
- 通知：部分脚本支持青龙通知（需配置通知模块）。
- 若遇到问题，请先检查变量格式和依赖环境。

---

如需详细使用说明或遇到问题，欢迎提交