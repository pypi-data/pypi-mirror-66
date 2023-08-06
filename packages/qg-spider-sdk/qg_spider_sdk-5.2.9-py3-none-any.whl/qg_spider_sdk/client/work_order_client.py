from qg_struct import get_app_homepage
import aiohttp
import json
import logging


class WebOrderClient:
    @classmethod
    async def get_prefix(cls, **kwargs):
        return await get_app_homepage('cetc-workOrder', **kwargs)

    @classmethod
    async def create_warning_workorder(cls, body, is_thread=False):
        prefix = await cls.get_prefix(is_thread=is_thread)
        async with aiohttp.ClientSession() as session:
            async with session.get(prefix+'workOrder/new', ) as response:
                try:
                    new_info = await response.json()
                    code = new_info["code"]
                except:
                    raise ConnectionError(
                        f'{prefix} 连接异常', prefix, await response.text())
                if code != "0":
                    raise ValueError(f'{prefix} 连接异常', prefix, new_info)
            async with session.post(prefix+'workOrder/submit', data=json.dumps({
                **new_info["data"],
                **body,
            }), headers={
                "Content-Type": "application/json; charset=utf-8"
            }) as response:
                try:
                    resp = await response.json()
                    code = resp["code"]
                except:
                    raise ConnectionError(
                        f'{prefix} 连接异常', prefix, await response.text())
                if code != "0":
                    raise ValueError(f'{prefix} 连接异常', prefix, resp)
                return resp["data"]
