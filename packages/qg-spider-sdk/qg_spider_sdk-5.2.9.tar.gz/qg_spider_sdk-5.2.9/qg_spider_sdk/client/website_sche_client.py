from qg_struct import get_app_homepage
import aiohttp
import logging


class WebsiteScheClient:
    @classmethod
    async def get_prefix(cls, **kwargs):
        return await get_app_homepage('website-sche', **kwargs)

    @classmethod
    async def force_up_order(cls, await_time: int, is_thread=False):
        """强制清盘

        Arguments:
            await_time {int} -- 清盘等待时间

        """
        timeout = await_time + 600
        url = await cls.get_prefix(is_thread=is_thread) + 'command/force_up_order'
        logging.info(url)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={"await_time": await_time}, timeout=timeout) as response:
                try:
                    res = await response.json()
                except:
                    raise ValueError(await response.text())
                return res
