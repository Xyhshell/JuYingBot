import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import yaml
import pywxdll

from plugins import weather
from plugins import random_kfc


now = datetime.now()  # 更新当前时间


class Work_main:
    def __init__(self):
        main_config_path = "main_config.yml"
        with open(main_config_path, "r", encoding="utf-8") as f:  # 读取设置
            main_config = yaml.safe_load(f.read())

        self.ip = main_config["ip"]  # 机器人ip
        self.port = main_config["port"]  # 机器人端口
        self.bot = pywxdll.Pywxdll(self.ip, self.port)  # 机器人api
        self.admin_list = main_config["admins"]  # 获取管理员列表
        self.data = self.bot.get_contact_list()


async def taday_w():
    print("命中事件：当前时间是", time.strftime("%Y-%m-%d %H:%M:%S"))
    word_ = '?work ?天气 樟树'
    woek_main = Work_main()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    formatted_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    for i in woek_main.data:  # 在通讯录数据中for
        wxid = i["wxid"]  # 获取微信号(加好友用)
        if wxid.startswith("wxid_"):  # 判断是好友 群 还是其他（如文件传输助手）
            this_ = {'content': f'{word_}', 'id': f'{timestamp}', 'id1': '', 'id2': '', 'id3': '', 'srvid': 1,
                     'time': f'{formatted_timestamp}', 'type': 1, 'wxid': f'{wxid}'}
            print(this_)
            await weather.weather().run(recv=dict(this_))

    # this_ = {'content': f'{word_}', 'id': f'{timestamp}', 'id1': '', 'id2': '', 'id3': '', 'srvid': 1,
    #          'time': f'{formatted_timestamp}', 'type': 1, 'wxid': f'{wxid}'}
    # print(this_)
    # await weather.weather().run(recv=dict(this_))


async def kfc_w():
    print("命中事件：当前时间是", time.strftime("%Y-%m-%d %H:%M:%S"))
    word_ = '?work ?kfc'
    woek_main = Work_main()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    formatted_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    for i in woek_main.data:  # 在通讯录数据中for
        wxid = i["wxid"]  # 获取微信号(加好友用)
        if wxid.startswith("wxid_"):  # 判断是好友 群 还是其他（如文件传输助手）
            this_ = {'content': f'{word_}', 'id': f'{timestamp}', 'id1': '', 'id2': '', 'id3': '', 'srvid': 1,
                     'time': f'{formatted_timestamp}', 'type': 1, 'wxid': f'{wxid}'}
            print(this_)
            await random_kfc.random_kfc().run(recv=dict(this_))


def acmain_start():
    # 创建一个异步调度器
    acscheduler = AsyncIOScheduler()

    # 添加任务，设置在每天的(hour=7, minute=54, second=50)执行
    actrigger_kfc = CronTrigger(hour=7, minute=54, second=50)
    acscheduler.add_job(kfc_w, actrigger_kfc, misfire_grace_time=60)

    # 添加任务，设置在每天的(hour=7, minute=0, second=10)执行
    actrigger_0 = CronTrigger(hour=7, minute=0, second=10)
    acscheduler.add_job(taday_w, actrigger_0, misfire_grace_time=60)
    actrigger_1 = CronTrigger(hour=12, minute=0, second=20)
    acscheduler.add_job(taday_w, actrigger_1, misfire_grace_time=60)
    actrigger_2 = CronTrigger(hour=17, minute=1, second=36)
    acscheduler.add_job(taday_w, actrigger_2, misfire_grace_time=60)

    print("> 定时任务启动完毕(异步)...")
    # 启动调度器
    acscheduler.start()


async def i_main():
    # 启动异步调度器
    acmain_start()

    # 保持事件循环运行
    try:
        await asyncio.Event().wait()  # 使用 await asyncio.Event().wait() 保持事件循环运行
    except (KeyboardInterrupt, SystemExit):
        pass


def is_main():
    asyncio.run(i_main())


if __name__ == '__main__':
    asyncio.run(i_main())
