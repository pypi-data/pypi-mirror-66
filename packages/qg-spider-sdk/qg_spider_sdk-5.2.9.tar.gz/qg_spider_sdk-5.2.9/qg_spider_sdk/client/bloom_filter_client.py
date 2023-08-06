
from qg_struct import get_app_homepage
import aiohttp
import json
class BloomFilterClient():
    @classmethod
    async def get_bloom_url_prefix(cls):
        prefix=await get_app_homepage("bloom")
        return prefix

    @classmethod
    async def add_content(cls,url,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code,"value":url}
            async with session.post(prefix+'add_content', data=body) as response:
                return await response.text()

    @classmethod
    async def add_list(cls,url,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code,"value":url}
            async with session.post(prefix+'add_list', data=body) as response:
                return await response.text()

    @classmethod
    async def exist(cls,url,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code,"value":url}
            async with session.post(prefix+'exist', data=body) as response:
                result=await response.json(content_type=None)
                return result.get("exist")

    @classmethod
    async def exist_content(cls,url,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code,"value":url}
            async with session.post(prefix+'exist_content', data=body) as response:
                result=await response.json(content_type=None)
                return result.get("exist")

    @classmethod
    async def exist_list(cls,url,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code,"value":url}
            async with session.post(prefix+'exist_list', data=body) as response:
                result=await response.json(content_type=None)
                return result.get("exist")

    @classmethod
    async def add_test(cls,url,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code,"value":url}
            async with session.post(prefix+'add_test', data=body) as response:
                return await response.text()

    @classmethod
    async def exist_test(cls,url,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code,"value":url}
            async with session.post(prefix+'exist_test', data=body) as response:
                result=await response.json(content_type=None)
                return result.get("exist")

    @classmethod
    async def check_is_new_url(cls,urls):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"urls":json.dumps(urls)}
            async with session.post(prefix+'check_is_new_url', data=body) as response:
                result=await response.json(content_type=None)
                return result.get("urls")

    @classmethod
    async def check_is_new_url_test(cls,urls):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"urls":json.dumps(urls)}
            async with session.post(prefix+'check_is_new_url_test', data=body) as response:
                result=await response.json(content_type=None)
                return result.get("urls")

    @classmethod
    async def delete_filter(cls,site_code):
        prefix = await cls.get_bloom_url_prefix()
        async with aiohttp.ClientSession() as session:
            body={"site_code":site_code}
            async with session.post(prefix+'delete_filter', data=body) as response:
                pass

