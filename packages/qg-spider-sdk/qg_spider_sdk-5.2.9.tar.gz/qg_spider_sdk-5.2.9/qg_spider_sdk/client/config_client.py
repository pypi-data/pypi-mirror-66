from qg_struct import get_app_homepage
import aiohttp
import logging


class ConfigClient:
    @classmethod
    async def get_prefix(cls):
        return await get_app_homepage('cetc-config')

    @classmethod
    async def get_config_data(cls, config_code):
        url = await cls.get_prefix()+'sysConfig/getSysConfigByConfigCode'
        logging.info(url)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={"configCode": config_code}) as response:
                try:
                    res = await response.json()
                except:
                    raise ValueError(await response.text())
                return res
