"""
系统资源管理
"""
from qg_spider_sdk.message import rabbit_mq
from qg_tool.tool import get_host_ip
import datetime
import asyncio
from qg_struct import config
import logging
import traceback
import urllib
import json
import aiohttp


class VpnMsgMan(object):

    @classmethod
    async def checkCanVPN(cls):
        canVPN=False
        proxy = urllib.request.getproxies()
        if proxy:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.google.com/",verify_ssl=False,proxy=proxy['http'],timeout=30) as response:
                        await asyncio.sleep(0.2)
                        if response.status:
                            canVPN=True
            except:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://www.google.com/",verify_ssl=False,proxy=proxy['http'],timeout=30) as response:
                            await asyncio.sleep(0.2)
                            if response.status:
                                canVPN=True
                except:
                    pass
        return canVPN



   


