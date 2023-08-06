"""
系统资源管理
"""
import psutil
from qg_spider_sdk.entity import SysRes
from qg_spider_sdk.message import rabbit_mq
import datetime
import time
import asyncio
import json
import os
from qg_struct import config
import logging
import traceback
import aio_pika
from . import datapipe


class SysResMan(object):

    @classmethod
    async def open(cls, process_name,process_type=None, interval=5, channel=None,con=None):
        while True:
            try:
                sys_res = await cls._get_sys_res(process_name,process_type, interval)
                if channel:
                    await cls._send_sys_res_msg_thread(sys_res, channel,con)
                else:
                    await cls._send_sys_res_msg(sys_res)
            except Exception:
                logging.error(f'获取系统资源异常')
                logging.error(traceback.format_exc())
            
    @classmethod
    async def _get_sys_res(cls, process_name,process_type, interval):
        # 内存使用情况
        virtual_memory = psutil.virtual_memory()
        # 磁盘使用情况
        disk_usage = psutil.disk_usage('/')
        # ip信息
        ip = config.get('ip')
        ramnum = await cls.get_ramnum(virtual_memory)
        ramper = virtual_memory.percent
        disk = disk_usage.total
        diskper = disk_usage.percent
        netnumandcpu = await cls._get_netnum(interval)
        netnum = netnumandcpu[0]
        # cpu 使用情况
        cpuper = netnumandcpu[1]
        return SysRes(ip=ip, process_name=process_name,process_type=process_type, cpuper=cpuper, netnum=netnum, ramper=ramper, ramnum=ramnum, disk=disk, diskper=diskper, siworking=1)

    @classmethod
    async def get_ramnum(cls, virtual_memory):
        ramnum = virtual_memory.total
        ramnumdeal = round(ramnum/(1024*1024), 1)
        return ramnumdeal

    @classmethod
    async def _send_sys_res_msg(cls, sys_res):
        dt = datetime.datetime.now()
        strg = dt.strftime('%Y-%m-%d %H:%M:%S')

        resourcebodyNew ={"ResMsg":{"msgtype": 'ResStatic', "servname": sys_res.process_name,"servtype": sys_res.process_type, "servip": sys_res.ip if not config['app_name'] == 'starter' else '{}:{}'.format(sys_res.ip, config['port']),
                        "sendtime": datetime.datetime.now().timestamp(), "isworking": sys_res.siworking, "msgdata": {
                        'netnum' : sys_res.netnum,
                        'ramper' : sys_res.ramper,
                        'ramnum' : sys_res.ramnum,
                        'cpuper' : sys_res.cpuper
                    }}}
        # 放入redis
        await datapipe.set_message(resourcebodyNew)

    @classmethod
    async def _send_sys_res_msg_thread(cls, sys_res, channel,con):
        dt = datetime.datetime.now()
        strg = dt.strftime('%Y-%m-%d %H:%M:%S')
        if con:
            resourcebodyNew = {"ResMsg":{"msgtype": 'ResStatic', "servname": sys_res.process_name, "servtype": sys_res.process_type,"servip": sys_res.ip if not config['app_name'] == 'starter' else '{}:{}'.format(sys_res.ip, config['port']),
                            "sendtime": datetime.datetime.now().timestamp(), "isworking": sys_res.siworking, "msgdata": {
                            'netnum' : sys_res.netnum,
                            'ramper' : sys_res.ramper,
                            'ramnum' : sys_res.ramnum,
                            'cpuper' : sys_res.cpuper
                        }}}
            # 放入redis
            con.rpush('msg_que_buf',json.dumps(resourcebodyNew))
    @classmethod
    async def _io_get_bytes(cls, sent=False, recv=False):
        internet = psutil.net_io_counters()  # 获取与网络IO相关的信息
        if internet == None:                 # 如果获取IO信息失败
            return None
        io_sent = internet.bytes_sent        # 开机以来发送的所有字节数
        io_recv = internet.bytes_recv        # 开机以来接收的所有字节数
        if sent == True and recv == True:
            return [io_sent, io_recv]
        elif sent == True:
            return io_sent
        elif recv == True:
            return io_recv
        else:
            return None

    @classmethod
    async def _get_netnum(cls, interval):
        byteSent1 = await cls._io_get_bytes(sent=True)  # 获取开机以来上传的字节数
        byteRecv1 = await cls._io_get_bytes(recv=True)  # 获取开机以来下载的字节数
        await asyncio.sleep(interval)                           # 间隔 interval 秒
        cpuper = psutil.cpu_percent()
        # os.system('cls')                               # 执行清屏命令
        byteSent2 = await cls._io_get_bytes(sent=True)  # 再次获取开机以来上传的字节数
        byteRecv2 = await cls._io_get_bytes(recv=True)  # 再次获取开机以来下载的字节数
        sent = byteSent2-byteSent1                     # interval 秒内所获取的上传字节数
        recv = byteRecv2-byteRecv1                     # interval 秒内所获取的下载字节数
        unit = 'B/S'                 # 显示的速度单位, 每次显示前重置单位为( 字节(B)/秒(S) )
        k = 1024
        sent = sent / k
        recv = recv / k
        return (round(recv/interval, 2), cpuper)


if __name__ == "__main__":
    sysResMan = SysResMan()
    sysResMan.get_sys_res('11')
