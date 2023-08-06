from . import datapipe
import asyncio
import random
import json

CHN = 'CHN'
Foreign = 'Foreign'
Http = 'http'
Https = 'https'
All = 'all'
class ProxyManOld():
    proxy_chn_list = [] # 境内
    proxy_foregin_list = [] # 境外
    proxy_list = []
    @classmethod
    async def get_chn_proxy(cls):
        await cls.check_si_sync()
        chn_proxy = random.choice(cls.proxy_chn_list)
        if chn_proxy:
            chn_proxy = json.loads(chn_proxy)
            return chn_proxy
        else:
            return None

    @classmethod
    async def get_foreign_proxy(cls):
        await cls.check_si_sync()
        foreign_proxy = random.choice(cls.proxy_foregin_list)
        if foreign_proxy:
            foreign_proxy = json.loads(foreign_proxy)
            return foreign_proxy
        else:
            return None

    @classmethod
    async def get_chn_proxys(cls):
        await cls.check_si_sync()
        proxy_list = []
        for proxy in cls.proxy_chn_list:
            proxy = json.loads(proxy)
            proxy_list.append(proxy)
        return proxy_list

    @classmethod
    async def get_all_proxys(cls):
        await cls.check_si_sync()
        proxy_list = []
        for proxy in cls.proxy_list:
            proxy = json.loads(proxy)
            proxy_list.append(proxy)
        return proxy_list

    @classmethod
    async def get_foreign_proxys(cls):
        await cls.check_si_sync()
        proxy_list = []
        for proxy in cls.proxy_foregin_list:
            proxy = json.loads(proxy)
            proxy_list.append(proxy)
        return proxy_list

    @classmethod
    async def set_chn_proxys(cls,proxys):
        await datapipe.delete_proxy_old(CHN)
        await datapipe.set_proxys_old(CHN,proxys)

    @classmethod
    async def set_foreign_proxys(cls,proxys):
        await datapipe.delete_proxy_old(Foreign)
        await datapipe.set_proxys_old(Foreign,proxys)
    
    @classmethod
    async def set_proxys(cls,proxys):
        await datapipe.delete_proxy_old(All)
        await datapipe.set_proxys_old(All,proxys)

    @classmethod
    async def update_chn_proxy(cls,proxy):
        for index,proxy_obj in enumerate(cls.proxy_chn_list):
            proxy_obj = json.loads(proxy_obj)
            if proxy_obj.get('proxy') == proxy:
                proxy_obj['num'] =  proxy_obj.get('num') + 1
                cls.proxy_chn_list[index] = json.dumps(proxy_obj)

    @classmethod
    async def update_foreign_proxy(cls,proxy):
        for index,proxy_obj in enumerate(cls.proxy_foregin_list):
            proxy_obj = json.loads(proxy_obj)
            if proxy_obj.get('proxy') == proxy:
                proxy_obj['num'] =  proxy_obj.get('num') + 1
                cls.proxy_foregin_list[index] = json.dumps(proxy_obj)
    
    @classmethod
    async def update_proxy_list(cls,proxy):
        for index,proxy_obj in enumerate(cls.proxy_list):
            proxy_obj = json.loads(proxy_obj)
            if proxy_obj.get('proxy') == proxy:
                proxy_obj['num'] =  proxy_obj.get('num') + 1
                cls.proxy_list[index] = json.dumps(proxy_obj)

    @classmethod
    async def check_si_sync(cls):
        for proxy_obj in cls.proxy_chn_list:
            if isinstance(proxy_obj,str):
                proxy_obj = json.loads(proxy_obj)
            if proxy_obj.get('num') > 1:
                cls.proxy_chn_list.remove(json.dumps(proxy_obj))

        for proxy_foreign_obj in cls.proxy_foregin_list:
            if isinstance(proxy_foreign_obj,str):
                proxy_foreign_obj = json.loads(proxy_foreign_obj)
            if  proxy_foreign_obj.get('num') > 1:
                cls.proxy_foregin_list.remove(json.dumps(proxy_foreign_obj))
        
        for proxy_list_obj in cls.proxy_list:
            if isinstance(proxy_list_obj,str):
                proxy_list_obj = json.loads(proxy_list_obj)
            if proxy_list_obj.get('num') > 1:
                cls.proxy_list.remove(json.dumps(proxy_list_obj))

        if len(cls.proxy_chn_list) < 5:
            proxy_chn_list = await datapipe.get_proxys_old(CHN)
            if proxy_chn_list and proxy_chn_list[0]:
                cls.proxy_chn_list = json.loads(proxy_chn_list[0])

        if len(cls.proxy_foregin_list) < 5:
            proxy_foregin_list = await datapipe.get_proxys_old(Foreign)
            if proxy_foregin_list and proxy_foregin_list[0]:
                cls.proxy_foregin_list = json.loads(proxy_foregin_list[0])
        
        if len(cls.proxy_list) < 5:
            proxy_list = await datapipe.get_proxys_old(All)
            if proxy_list and proxy_list[0]:
                cls.proxy_list = json.loads(proxy_list[0])

    @classmethod
    async def _sync_all(cls):
        proxy_chn_list = await datapipe.get_proxys_old(CHN)
        if proxy_chn_list and proxy_chn_list[0]:
            cls.proxy_chn_list = json.loads(proxy_chn_list[0])
        proxy_foregin_list = await datapipe.get_proxys_old(Foreign)
        if proxy_foregin_list and proxy_foregin_list[0]:
            cls.proxy_foregin_list = json.loads(proxy_foregin_list[0])
        proxy_list = await datapipe.get_proxys_old(Foreign)
        if proxy_list and proxy_list[0]:
            cls.proxy_list = json.loads(proxy_list[0])

    @classmethod
    async def open(cls):
        await cls._sync_all()




asyncio.get_event_loop().run_until_complete(ProxyManOld.open())
