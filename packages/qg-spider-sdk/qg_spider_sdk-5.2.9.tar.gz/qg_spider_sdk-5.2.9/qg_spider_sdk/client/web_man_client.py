from qg_struct import get_app_homepage
import aiohttp
import json
import logging


class WebManClient:
    @classmethod
    async def get_prefix(cls, **kwargs):
        return await get_app_homepage('cetc-webManage', **kwargs)

    @classmethod
    async def get_websites(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(await cls.get_prefix()+'websiteInfo/getWebsites') as response:
                return await response.json()

    @classmethod
    async def get_website_by_code(cls, code):
        async with aiohttp.ClientSession() as session:
            async with session.post(await cls.get_prefix()+'websiteInfo/getWebsiteByCode', data={"code": code}) as response:
                return await response.json()

    @classmethod
    async def send_email(cls, address, subject, context, is_thread=False):
        async with aiohttp.ClientSession() as session:
            body = {
                "subject": subject,
                "address": address,
                "context": context
            }
            async with session.post(await cls.get_prefix(is_thread=is_thread)+'mail/sendMail', data=body) as response:
                return await response.text()
