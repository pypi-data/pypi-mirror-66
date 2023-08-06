"""
    任务队列业务封装
"""
from qg_struct import MemoryDB, config, init_log
import logging
import traceback
from .pool_command import ServiceMixin, SpecialSpiderRegisterMixin, WebsiteUrlRegistryMixin, WebsiteMixin, UrlPageMixin, UrlRecordMixin, ParseResultMixin,  ConfigMixin, WebsiteWorkTableMixin
from .list_command import WaitExitPageMixin, EndUrlMixin, WaitScheUrlMixin, WaitExtrMixin, WaitDownloadMixin,MessageMixin, \
    InitialWaitScheWebsiteMixin, DailyWaitScheWebsiteMixin, PauseUrlMixin, ProxyWaitDownloadMixin, DailyProxyWaitScheWebsiteMixin, InitialProxyWaitScheWebsiteMixin, SpecialWaitScheWebsiteMixin, WaitSaveUrlMixin, ProxyMixin, ProxySpecialWaitScheWebsiteMixin
from .script_command import ScriptMixin
import asyncio
init_log()
memory_db = config['memoryDB']


class Datapipe(WebsiteMixin, WaitExitPageMixin, EndUrlMixin, UrlRecordMixin, UrlPageMixin, ParseResultMixin, WaitScheUrlMixin,
               WaitExtrMixin, ConfigMixin,
               WaitDownloadMixin, WebsiteWorkTableMixin,
               InitialWaitScheWebsiteMixin, DailyWaitScheWebsiteMixin, PauseUrlMixin, WebsiteUrlRegistryMixin,
               ProxyWaitDownloadMixin, DailyProxyWaitScheWebsiteMixin, InitialProxyWaitScheWebsiteMixin,
               SpecialWaitScheWebsiteMixin, ProxySpecialWaitScheWebsiteMixin, SpecialSpiderRegisterMixin, WaitSaveUrlMixin, ServiceMixin, ProxyMixin,
               ScriptMixin,MessageMixin):

    def __init__(self):
        sentinels = list(map(lambda x: (x[0], x[1]), memory_db['sentinels']))
        master_name = memory_db['master_name']
        password = memory_db['password']
        self.memory_db = MemoryDB(
            sentinels, db=int(memory_db.get('database')) if memory_db.get('database') else 0, master_name=master_name, password=password)
        self.isClose = True

    async def open(self):
        """
        开启任务队列连接
        """
        try:
            error = False
            await self.memory_db.open()
            self.isClose = False
        except:
            error = True
            logging.error(traceback.format_exc())
            logging.error('开始redis连接异常')
        finally:
            if error:
                await asyncio.sleep(5)
                await self.open()

    async def close(self):
        """
        关闭任务队列连接
        """
        await self.memory_db.close()
        self.isClose = True


datapipe = Datapipe()
loop = asyncio.get_event_loop()
loop.run_until_complete(datapipe.open())

__all__ = ('datapipe', 'Datapipe')
