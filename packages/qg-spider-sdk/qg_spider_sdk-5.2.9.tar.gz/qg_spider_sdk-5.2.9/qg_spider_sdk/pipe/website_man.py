import asyncio
from qg_spider_sdk.entity import Website
from . import datapipe
from qg_tool.tool import find
from qg_spider_sdk.message import rabbit_mq
import json
import logging
from qg_spider_sdk.enums import WebsiteExecuteStatus
import inspect
import traceback
from qg_struct import init_log
init_log()

'''
{
  delete: [],
  update: [],
  add: [],
}
'''


class WebsiteMan:

    website_list = []
    website_stop_callback = set()
    website_regain_callback = set()

    @classmethod
    def register_stop_callback(cls, func):
        """
        注册网站停止回调,参数为site_code
        """
        cls.website_stop_callback.add(func)

    @classmethod
    def unregister_stop_callback(cls, func):
        cls.website_stop_callback.remove(func)

    @classmethod
    def register_regain_callback(cls, func):
        """
        注册网站暂停回调,参数为site_code
        """
        cls.website_regain_callback.add(func)

    @classmethod
    def unregister_regain_callback(cls, func):
        cls.website_regain_callback.remove(func)

    @classmethod
    async def open(cls, wait_time=5):
        error = False
        try:
            await cls._sync_all()
            rabbit_mq.register_website_callback(cls._receive_msg)
        except:
            error = True
            logging.error(traceback.format_exc())
            logging.error(f'{wait_time} s 后重试')
        finally:
            if error:
                await asyncio.sleep(wait_time)
                await cls.open(min(wait_time*2, 120))
        # 监听消息

    @classmethod
    async def _sync_all(cls, wait_time=5):
        error = False
        try:
            cls.website_list = await datapipe.get_all_websites()
        except:
            error = True
            logging.error(traceback.format_exc())
            logging.error(f'{wait_time} s 后重试')
        finally:
            if error:
                await asyncio.sleep(wait_time)
                await cls._sync_all(min(wait_time*2, 120))

    @classmethod
    async def _sync(cls, body: dict):
        try:
            delete_list = body.get('delete')
            update_list = body.get('update')
            add_list = body.get('add')
            if delete_list:
                for site_code in delete_list:
                    website = find(
                        lambda website: website['site_code'] == site_code, cls.website_list)
                    cls.website_list.remove(website)
            if update_list:
                websites = await datapipe.get_websites(*update_list)
                for website in websites:
                    old_website = find(
                        lambda x: x['site_code'] == website['site_code'], cls.website_list)

                    if old_website.status != website.status and website.status == WebsiteExecuteStatus.stopped.code:
                        # 触发stop hook
                        for callback in cls.website_stop_callback:
                            if inspect.iscoroutinefunction(callback):
                                await callback(website.site_code)
                            else:
                                callback(website.site_code)
                    elif old_website.si_site_paused() and website.status == WebsiteExecuteStatus.started.code:
                        # 触发regain hook
                        for callback in cls.website_regain_callback:
                            if inspect.iscoroutinefunction(callback):
                                await callback(website.site_code)
                            else:
                                callback(website.site_code)
                    old_website.update(website)

            if add_list:
                websites = await datapipe.get_websites(*add_list)
                for website in websites:
                    old_website = cls.get_website(website.site_code)
                    if old_website:
                        old_website.update(website)
                    else:
                        cls.website_list.append(website)
        except:
            logging.error('同步失败,重新刷新全部网站信息')
            if add_list:
                logging.error(add_list)
            if update_list:
                logging.error(update_list)
            if delete_list:
                logging.error(delete_list)
            logging.error(traceback.format_exc())
            await cls._sync_all()

    @classmethod
    async def _send_msg(cls, body: dict):
        await rabbit_mq.send_website_msg(json.dumps(body))

    @classmethod
    async def _receive_msg(cls, body):
        body = json.loads(body)
        await cls._sync(body)

    @classmethod
    def get_website(cls, site_code: int) -> Website:
        return find(
            lambda website: website['site_code'] == site_code, cls.website_list)

    @classmethod
    async def get_global_website(cls, site_code: int) -> Website:
        return await datapipe.get_website(site_code)

    @classmethod
    async def sync_website_by_sitecode(cls, site_code: int):
        website = None
        is_error = False
        try:
            website = await cls.get_global_website(site_code)
            if website:
                old_website = cls.get_website(site_code)
                if old_website:
                    old_website.update(website)
                else:
                    cls.website_list.append(website)
        except:
            is_error = True
            logging.error(traceback.format_exc())
        finally:
            if is_error:
                return await cls.sync_website_by_sitecode(site_code)
            if website:
                return True
            return False

    @classmethod
    def get_websites(cls, site_codes: [int]) -> [Website]:
        return list(filter(lambda x: x, map(lambda stie_code: cls.get_website(stie_code), site_codes)))

    @classmethod
    async def update_website(cls, website: Website):
        await datapipe.set_website(website)
        await cls._send_msg({
            'update': [website['site_code']]})

    @classmethod
    async def update_websites(cls, websites: [Website]):
        await datapipe.set_websites(websites)
        await cls._send_msg({
            'update': list(map(lambda website: website['site_code'], websites))})

    @classmethod
    async def add_website(cls, website: Website):
        cls.website_list.append(website)
        await datapipe.set_website(website)
        await cls._send_msg({
            'add': [website['site_code']]})

    @classmethod
    async def add_websites(cls, websites: [Website]):
        for website in websites:
            cls.website_list.append(website)
        await datapipe.set_websites(websites)
        await cls._send_msg({
            'add': list(map(lambda website: website['site_code'], websites))})

    @classmethod
    async def delete_website(cls, website: Website):
        cls.website_list.remove(website)
        await datapipe.delete_website(website['site_code'])
        await cls._send_msg({
            'delete': [website['site_code']]})

    @classmethod
    async def delete_websites(cls, websites: [Website]):
        for website in websites:
            cls.website_list.remove(website)
        await datapipe.delete_website(*map(lambda website: website['site_code'], websites))
        await cls._send_msg({
            'delete': list(map(lambda website: website['site_code'], websites))})


asyncio.get_event_loop().run_until_complete(WebsiteMan.open())
