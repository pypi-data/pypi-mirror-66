from qg_struct import get_app_homepage
import aiohttp
import json
import logging


class IndependCrawlClient:
    @classmethod
    async def get_prefix(cls, **kwargs):
        return await get_app_homepage('starter', **kwargs)

    @classmethod
    async def check_has_spider(cls, name, is_thread=False):
        prefix = await cls.get_prefix(is_thread=is_thread)
        async with aiohttp.ClientSession() as session:
            body={"spider_name":name}
            async with session.post(prefix+'command/check_has_spider', data=body) as response:
                result=await response.json(content_type=None)
                return result
                
