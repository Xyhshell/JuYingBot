# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from datetime import datetime
# import os
# import requests
# import urllib3
# import yaml
# import pywxdll
# import time
#
# # 禁用SSL证书验证警告
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "Cache-Control": "no-cache",
#     "Pragma": "no-cache",
#     "Priority": "u=0, i",
#     "Sec-Ch-Ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": '"Windows"',
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
# }
#
#
# class RandomKFC:
#     def __init__(self):
#         main_config_path = "main_config.yml"
#         with open(main_config_path, "r", encoding="utf-8") as f:  # 读取设置
#             main_config = yaml.safe_load(f.read())
#
#         self.ip = main_config["ip"]  # 机器人ip
#         self.port = main_config["port"]  # 机器人端口
#         self.bot = pywxdll.Pywxdll(self.ip, self.port)  # 机器人api
#         self.admin_list = main_config["admins"]  # 获取管理员列表
#         self.data = self.bot.get_contact_list()
#
#         pic_cache_path = "resources/pic_cache"  # 检测是否有pic_cache文件夹
#         if not os.path.exists(pic_cache_path):
#             os.makedirs(pic_cache_path)
#
#     def work(self, wxid):
#         now = datetime.now()  # 更新当前时间
#         date_ = now.strftime('%Y%m%d%H%M%S')
#         # 图片缓存路径
#         pic_cache_path_original = os.path.join(os.getcwd(), f"resources\\pic_cache\\picture_{date_}.png")
#         print(date_)
#         try:
#             if not os.path.exists(pic_cache_path_original):
#                 with requests.Session() as session:
#                     old = session.get('https://api.vvhan.com/api/moyu', allow_redirects=False)
#                     print(old.url)  # 输出
#                     location = old.headers['Location']  # 获取重定向的位置信息
#                     new_my = session.get(location)  # 发送重定向请求
#                     print(new_my.url)  # 输出
#
#                 response = requests.get(new_my.url, headers=headers, verify=False)
#                 response.raise_for_status()
#
#                 with open(pic_cache_path_original, "wb") as file:  # 下载并保存
#                     file.write(response.content)
#             time.sleep(1.5)
#             self.bot.send_pic_msg(wxid, os.path.abspath(pic_cache_path_original))  # 发送图片
#         except Exception as error:
#             out_message = f"出现错误❌！{error}"
#             self.bot.send_txt_msg(self.admin_list[0], out_message)  # 发送
#
#
# # 定义你想要执行的任务
# def kfc_job():
#     print("命中事件：当前时间是", time.strftime("%Y-%m-%d %H:%M:%S"))
#     push_list = []
#     now_kfc = RandomKFC()
#     for i in now_kfc.data:  # 在通讯录数据中for
#         wxid = i["wxid"]  # 获取微信号(加好友用)
#         if wxid.startswith("wxid_"):  # 判断是好友 群 还是其他（如文件传输助手）
#             if wxid not in push_list:
#                 push_list.append(wxid)
#                 now_kfc.work(wxid=wxid)
#
#
# def main_start():
#     # 创建调度器
#     scheduler = BackgroundScheduler()
#     # 检查并添加任务，避免重复添加
#     if not scheduler.get_job('task_1'):
#         # 添加定时任务
#         trigger_1 = CronTrigger(hour=7, minute=55, second=10)  # 每天7:55:10执行
#         scheduler.add_job(kfc_job, trigger_1, id="task_1")
#     # if not scheduler.get_job('task_1'):
#     #     # 添加定时任务
#     #     trigger_1 = CronTrigger(hour=21, minute=1, second=30)  # 每天7:55:10执行
#     #     scheduler.add_job(kfc_job, trigger_1, id="task_1")
#
#     print("> 定时任务启动完毕...")
#     # 启动调度器
#     scheduler.start()
#
#
# if __name__ == '__main__':
#     main_start()


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import os
import requests
import urllib3
import yaml
import pywxdll
import time
from loguru import logger

# 禁用SSL证书验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}


class RandomKFC:
    def __init__(self):
        main_config_path = "main_config.yml"
        with open(main_config_path, "r", encoding="utf-8") as f:  # 读取设置
            main_config = yaml.safe_load(f.read())

        self.ip = main_config["ip"]  # 机器人ip
        self.port = main_config["port"]  # 机器人端口
        self.bot = pywxdll.Pywxdll(self.ip, self.port)  # 机器人api
        self.admin_list = main_config["admins"]  # 获取管理员列表
        self.data = self.bot.get_contact_list()

        pic_cache_path = "resources/pic_cache"  # 检测是否有pic_cache文件夹
        if not os.path.exists(pic_cache_path):
            os.makedirs(pic_cache_path)

    def download(self, pic_cache_path_original):


        try:
            # 获取文件大小，单位为字节
            file_size = os.path.getsize(pic_cache_path_original)
            # 计算500KB的字节数
            size_500kb = 500 * 1024
            # 比较文件大小是否小于500KB
            if file_size < size_500kb:
                logger.info(f"文件大小小于500KB，重新下载")
                return False
        except Exception as e:
            logger.error(f"检查文件大小失败: {e}")
            return False

        return True

    def work(self, wxid):
        date_ = time.strftime("%Y-%m-%d")
        # 图片缓存路径
        pic_cache_path_original = os.path.join(os.getcwd(), f"resources\\pic_cache\\picture_{date_}.png")
        logger.info(f"图片缓存路径: {pic_cache_path_original}")

        try:
            # 如果文件不存在或者文件大小小于500KB，重新下载
            for _ in range(3):
                if not os.path.exists(pic_cache_path_original) or not self.download(pic_cache_path_original):
                    logger.info(f"开始下载图片")
                    if self.download(pic_cache_path_original):
                        break
            else:
                logger.error("图片下载失败，三次重试后仍然失败")
                self.bot.send_txt_msg(self.admin_list[0], "下载失败，三次重试后仍然失败")
                return

            # 发送图片
            logger.info(f'[信息] {pic_cache_path_original}| [发送到] {wxid}')
            self.bot.send_pic_msg(wxid, os.path.abspath(pic_cache_path_original))  # 发送图片

        except Exception as error:
            out_message = f"出现错误❌！{error}"
            logger.error(f'[发送信息]{out_message}| [发送到] {wxid}')
            self.bot.send_txt_msg(self.admin_list[0], out_message)  # 发送


# 定义你想要执行的任务
def kfc_job():
    print("命中事件：当前时间是", time.strftime("%Y-%m-%d %H:%M:%S"))
    push_list = []
    now_kfc = RandomKFC()
    for i in now_kfc.data:  # 在通讯录数据中for
        wxid = i["wxid"]  # 获取微信号(加好友用)
        if wxid.startswith("wxid_"):  # 判断是好友 群 还是其他（如文件传输助手）
            if wxid not in push_list:
                push_list.append(wxid)
                now_kfc.work(wxid=wxid)

    # wxid = "wxid_7zue8xzry38i22"
    # now_kfc.work(wxid=wxid)


def main_start():
    # 创建调度器
    scheduler = BackgroundScheduler()
    # 检查并添加任务，避免重复添加
    if not scheduler.get_job('task_1'):
        # 添加定时任务
        # trigger_1 = CronTrigger(hour=12, minute=30, second=00)
        # scheduler.add_job(kfc_job, trigger=trigger_1, id="task_1", misfire_grace_time=60)
        pass

    print("> 定时任务启动完毕...")
    # 启动调度器
    scheduler.start()


if __name__ == '__main__':
    main_start()
