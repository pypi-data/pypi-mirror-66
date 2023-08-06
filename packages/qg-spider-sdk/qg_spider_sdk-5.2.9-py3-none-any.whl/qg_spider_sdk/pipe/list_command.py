from qg_spider_sdk.entity.url_meta import UrlMeta
from qg_spider_sdk.entity.proxy import Proxy
from qg_spider_sdk.entity.website import Website
import json
import datetime
import asyncio

wait_sche_url_key = 'waitSchedQue'
wait_extr_key = 'waitExtrQue'
wait_download_key = 'waitDLSet'
proxy_wait_download_key = 'proxyWaitDLSet'
wait_save_url_key = 'waitSaveUrlQue'
daily_wait_shce_website_key = 'dailyWaitScheWebsiteQue'
initial_wait_shce_website_key = 'initialWaitScheWebsiteQue'
daily_proxy_wait_shce_website_key = 'dailyProxyWaitScheWebsiteQue'
initial_proxy_wait_shce_website_key = 'initialProxyWaitScheWebsiteQue'
special_wait_shce_website_key = 'specialWaitScheWebsiteQue'
proxy_special_wait_shce_website_key = 'proxySpecialWaitScheWebsiteQue'
end_url_key = 'endQue'
wait_extr_paeg_key = 'waitExtrPageQue'
pause_url_format_key = 'pause_url_{}'
proxy_key = "proxy_que"
message_key = "msg_que_buf"

class PauseUrlMixin:
    """
    暂停网站队列
    """

    async def set_pause_url(self, site_code, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入暂停url
        """
        res = await self._set_list(pause_url_format_key.format(site_code), url_meta, *url_metas)
        return res

    async def trans_pause_urls(self, site_code):
        """
        转移暂停url到待调度url
        """
        while True:
            res = await self._get_list(pause_url_format_key.format(site_code), number=2000)
            if not res:
                return
            res = map(lambda x: UrlMeta(*json.loads(x)),
                      filter(lambda x: x, res))
            await self.set_wait_sche_url(*res)

    async def rem_pause_urls(self, site_code):
        """
        删除该网站暂停队列
        """
        while True:
            res = await self._get_list(pause_url_format_key.format(site_code), number=2000)
            if not res:
                return
            res = list(map(lambda x: UrlMeta(*json.loads(x)),
                           filter(lambda x: x, res)))
            if res:
                await self.set_end_url(*res, *res)


class DailyWaitScheWebsiteMixin:
    """
    日增待调度网站有序集命令封装
    """

    async def set_daily_wait_sche_website(self, website: Website, *websites: [Website]):
        """
        加入待调度网站，根据是否代理加入不同的队列，有序集会根据网站优先级字段排序，所以优先级字段限制为int，float
        """
        temp = [website.priority, website.site_code]
        for i in websites:
            temp.append(i.priority)
            temp.append(i.site_code)
        res = await self.memory_db.zadd(daily_wait_shce_website_key, *temp)
        return res

    async def get_daily_wait_sche_website(self) -> int:
        """
        获取一定数量的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(daily_wait_shce_website_key, 0, number=1)
        site_codes = list(map(lambda x: int(
            x), filter(lambda x: x, res)))
        if site_codes:
            return site_codes[0]

    async def get_daily_wait_sche_websites(self, number) -> [int]:
        """
        获取一定数量的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(daily_wait_shce_website_key, 0, number=number)
        return list(map(lambda x: int(x), filter(lambda x: x, res)))

    async def get_daily_wait_sche_website_len(self) -> int:
        """
        获取一定数量的待调度网站队列长度
        """
        return await self.memory_db.zlen(daily_wait_shce_website_key)

    async def delete_daily_wait_sche_websites(self, site_code, *site_codes):
        return await self.memory_db.zrem(daily_wait_shce_website_key, site_code, *site_codes)


class InitialWaitScheWebsiteMixin:
    """
    初始待调度网站有序集命令封装
    """

    async def set_initial_wait_sche_website(self, website: Website, *websites: [Website]):
        """
        加入待调度网站，根据是否代理加入不同的队列，有序集会根据网站优先级字段排序，所以优先级字段限制为int，float
        """
        temp = [website.priority, website.site_code]
        for i in websites:
            temp.append(i.priority)
            temp.append(i.site_code)
        res = await self.memory_db.zadd(initial_wait_shce_website_key, *temp)
        return res

    async def get_initial_wait_sche_website(self) -> int:
        """
        获取一定数量的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(initial_wait_shce_website_key, 0, number=1)
        site_codes = list(map(lambda x: int(
            x), filter(lambda x: x, res)))
        if site_codes:
            return site_codes[0]

    async def get_initial_wait_sche_websites(self, number) -> [int]:
        """
        获取一定数量的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(initial_wait_shce_website_key, 0, number=number)
        return list(map(lambda x: int(x), filter(lambda x: x, res)))

    async def get_initial_wait_sche_website_len(self) -> int:
        """
        获取一定数量的待调度网站队列长度
        """
        return await self.memory_db.zlen(initial_wait_shce_website_key)

    async def delete_initial_wait_sche_websites(self, site_code, *site_codes):
        return await self.memory_db.zrem(initial_wait_shce_website_key, site_code, *site_codes)


class DailyProxyWaitScheWebsiteMixin:
    """
    需要代理的待调度网站有序集命令封装
    """

    async def set_daily_proxy_wait_sche_website(self, website: Website, *websites: [Website]):
        """
        加入需要代理的待调度网站，根据是否代理加入不同的队列，有序集会根据网站优先级字段排序，所以优先级字段限制为int，float
        """
        temp = [website.priority, website.site_code]
        for i in websites:
            temp.append(i.priority)
            temp.append(i.site_code)
        res = await self.memory_db.zadd(daily_proxy_wait_shce_website_key, *temp)
        return res

    async def get_daily_proxy_wait_sche_website(self) -> int:
        """
        获取一定数量的需要代理的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(daily_proxy_wait_shce_website_key, 0, number=1)
        site_codes = list(map(lambda x: int(
            x), filter(lambda x: x, res)))
        if site_codes:
            return site_codes[0]

    async def get_daily_proxy_wait_sche_websites(self, number) -> [int]:
        """
        获取一定数量的需要代理的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(daily_proxy_wait_shce_website_key, 0, number=number)
        return list(map(lambda x: int(x), filter(lambda x: x, res)))

    async def get_daily_proxy_wait_sche_website_len(self) -> int:
        """
        获取一定数量的需要代理的待调度网站队列长度
        """
        return await self.memory_db.zlen(daily_proxy_wait_shce_website_key)

    async def delete_daily_proxy_wait_sche_websites(self, site_code, *site_codes):
        return await self.memory_db.zrem(daily_proxy_wait_shce_website_key, site_code, *site_codes)


class InitialProxyWaitScheWebsiteMixin:
    """
    需要代理的待调度网站有序集命令封装
    """

    async def set_initial_proxy_wait_sche_website(self, website: Website, *websites: [Website]):
        """
        加入需要代理的待调度网站，根据是否代理加入不同的队列，有序集会根据网站优先级字段排序，所以优先级字段限制为int，float
        """
        temp = [website.priority, website.site_code]
        for i in websites:
            temp.append(i.priority)
            temp.append(i.site_code)
        res = await self.memory_db.zadd(initial_proxy_wait_shce_website_key, *temp)
        return res

    async def get_initial_proxy_wait_sche_website(self) -> int:
        """
        获取一定数量的需要代理的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(initial_proxy_wait_shce_website_key, 0, number=1)
        site_codes = list(map(lambda x: int(
            x), filter(lambda x: x, res)))
        if site_codes:
            return site_codes[0]

    async def get_initial_proxy_wait_sche_websites(self, number) -> [int]:
        """
        获取一定数量的需要代理的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(initial_proxy_wait_shce_website_key, 0, number=number)
        return list(map(lambda x: int(x), filter(lambda x: x, res)))

    async def get_initial_proxy_wait_sche_website_len(self) -> int:
        """
        获取一定数量的需要代理的待调度网站队列长度
        """
        return await self.memory_db.zlen(initial_proxy_wait_shce_website_key)

    async def delete_initial_proxy_wait_sche_websites(self, site_code, *site_codes):
        return await self.memory_db.zrem(initial_proxy_wait_shce_website_key, site_code, *site_codes)


class SpecialWaitScheWebsiteMixin:
    """
    独立爬虫的待调度网站有序集命令封装
    """

    async def set_special_wait_sche_website(self, website: Website, *websites: [Website]):
        """
        加入独立爬虫的待调度网站，根据是否代理加入不同的队列，有序集会根据网站优先级字段排序，所以优先级字段限制为int，float
        """
        temp = [website.priority, website.site_code]
        for i in websites:
            temp.append(i.priority)
            temp.append(i.site_code)
        res = await self.memory_db.zadd(special_wait_shce_website_key, *temp)
        return res

    async def get_special_wait_sche_website(self) -> int:
        """
        获取独立爬虫的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(special_wait_shce_website_key, 0, number=1)
        site_codes = list(map(lambda x: int(
            x), filter(lambda x: x, res)))
        if site_codes:
            return site_codes[0]

    async def get_special_wait_sche_websites(self, number) -> [int]:
        """
        获取一定数量的独立爬虫的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(special_wait_shce_website_key, 0, number=number)
        return list(map(lambda x: int(x), filter(lambda x: x, res)))

    async def get_special_wait_sche_website_len(self) -> int:
        """
        获取独立爬虫的待调度网站队列长度
        """
        return await self.memory_db.zlen(special_wait_shce_website_key)

    async def delete_special_wait_sche_websites(self, site_code, *site_codes):
        return await self.memory_db.zrem(special_wait_shce_website_key, site_code, *site_codes)


class ProxySpecialWaitScheWebsiteMixin:
    """
    需要翻墙独立爬虫的待调度网站有序集命令封装
    """

    async def set_proxy_special_wait_sche_website(self, website: Website, *websites: [Website]):
        """
        加入需要翻墙独立爬虫的待调度网站，根据是否代理加入不同的队列，有序集会根据网站优先级字段排序，所以优先级字段限制为int，float
        """
        temp = [website.priority, website.site_code]
        for i in websites:
            temp.append(i.priority)
            temp.append(i.site_code)
        res = await self.memory_db.zadd(proxy_special_wait_shce_website_key, *temp)
        return res

    async def get_proxy_special_wait_sche_website(self) -> int:
        """
        获取需要翻墙独立爬虫的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(proxy_special_wait_shce_website_key, 0, number=1)
        site_codes = list(map(lambda x: int(
            x), filter(lambda x: x, res)))
        if site_codes:
            return site_codes[0]

    async def get_proxy_special_wait_sche_websites(self, number) -> [int]:
        """
        获取一定数量的需要翻墙独立爬虫的待调度网站列表，数量不一定符合
        number: 数量
        """
        res = await self.memory_db.zrange(proxy_special_wait_shce_website_key, 0, number=number)
        return list(map(lambda x: int(x), filter(lambda x: x, res)))

    async def get_proxy_special_wait_sche_website_len(self) -> int:
        """
        获取需要翻墙独立爬虫的待调度网站队列长度
        """
        return await self.memory_db.zlen(proxy_special_wait_shce_website_key)

    async def delete_proxy_special_wait_sche_websites(self, site_code, *site_codes):
        return await self.memory_db.zrem(proxy_special_wait_shce_website_key, site_code, *site_codes)


class WaitScheUrlMixin:
    """
    待调度url队列封装
    """

    async def set_wait_sche_url(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入待调度url
        """
        res = await self._set_list(wait_sche_url_key, url_meta, *url_metas)
        return res

    async def get_wait_sche_url(self):
        """
        获取待调度url
        """
        res = await self._get_list(wait_sche_url_key, number=1)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        if url_metas:
            return url_metas[0]

    async def get_wait_sche_urls(self, number):
        """
        获取待调度url
        """
        res = await self._get_list(wait_sche_url_key, number=number)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        return url_metas

    async def get_wait_sche_url_len(self) -> int:

        return await self.memory_db.llen(wait_sche_url_key)

    async def clear_wait_sche_url(self):
        return await self.memory_db.delete(wait_sche_url_key)


class WaitExtrMixin:
    """
    待提取url队列封装
    """

    async def set_wait_extr(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入待提取url
        """
        res = await self._set_list(wait_extr_key, url_meta, *url_metas)
        return res

    async def get_wait_extr(self):
        """
        获取待提取url
        """
        res = await self._get_list(wait_extr_key, number=1)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        if url_metas:
            return url_metas[0]

    async def get_wait_extrs(self, number):
        """
        获取待提取url
        """
        res = await self._get_list(wait_extr_key, number=number)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        return url_metas

    async def get_wait_extr_len(self) -> int:

        return await self.memory_db.llen(wait_extr_key)

    async def clear_wait_extr_url(self):
        return await self.memory_db.delete(wait_extr_key)


class WaitExitPageMixin:
    """
    待提取page队列封装
    """

    async def set_wait_extr_page(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入待提取urlkey
        """
        res = await self._set_list(wait_extr_paeg_key, url_meta, *url_metas)
        return res

    async def get_wait_extr_page(self):
        """
        获取待提取urlkey
        """
        res = await self._get_list(wait_extr_paeg_key, number=1)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        if url_metas:
            return url_metas[0]

    async def get_wait_extr_pages(self, number):
        """
        获取待提取urlkey
        """
        res = await self._get_list(wait_extr_paeg_key, number=number)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        return url_metas

    async def get_wait_extr_page_len(self) -> int:

        return await self.memory_db.llen(wait_extr_paeg_key)


class WaitDownloadMixin:
    """
    待下载url队列封装
    """

    async def set_wait_download(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入待下载url
        """
        res = await self._set_list(wait_download_key, url_meta, *url_metas)
        return res

    async def get_wait_download(self):
        """
        获取待下载url
        """
        res = await self._get_list(wait_download_key, number=1)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        if url_metas:
            return url_metas[0]

    async def get_wait_downloads(self, number):
        """
        获取待下载urls
        """
        res = await self._get_list(wait_download_key,  number=number)

        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        return url_metas

    async def get_wait_download_len(self) -> int:

        return await self.memory_db.llen(wait_download_key)

    async def clear_wait_download_url(self):
        return await self.memory_db.delete(wait_download_key)


class ProxyWaitDownloadMixin:
    """
    可代理的待下载url队列封装
    """

    async def set_proxy_wait_download(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入需要代理的待下载url
        """
        res = await self._set_list(proxy_wait_download_key, url_meta, *url_metas)
        return res

    async def get_proxy_wait_download(self):
        """
        获取需要代理的待下载url
        """
        res = await self._get_list(proxy_wait_download_key,  number=1)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        if url_metas:
            return url_metas[0]

    async def get_proxy_wait_downloads(self, number):
        """
        获取需要代理的待下载urls
        """
        res = await self._get_list(proxy_wait_download_key, number=number)

        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        return url_metas

    async def get_proxy_wait_download_len(self) -> int:

        return await self.memory_db.llen(proxy_wait_download_key)

    async def clear_proxy_wait_download_url(self):
        return await self.memory_db.delete(proxy_wait_download_key)


class WaitSaveUrlMixin:
    """
    待保存url队列封装
    """

    async def set_wait_save_url(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入待保存html
        """
        res = await self._set_list(wait_save_url_key, url_meta, *url_metas)
        return res

    async def set_wait_save_url_lpush(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入待保存html
        """
        res = await self._set_list_lpush(wait_save_url_key, url_meta, *url_metas)
        return res

    async def get_wait_save_url(self):
        """
        获取待保存html
        """

        res = await self._get_list(wait_save_url_key, number=1)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        if url_metas:
            return url_metas[0]

    async def get_wait_save_urls(self, number):
        """
        获取待保存html
        """
        res = await self._get_list(wait_save_url_key, number=number)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))

        return url_metas

    async def get_wait_save_url_len(self) -> int:

        return await self.memory_db.llen(wait_save_url_key)


class EndUrlMixin:
    """
    url结束队列封装
    """

    async def set_end_url(self, url_meta: UrlMeta, *url_metas: [UrlMeta]):
        """
        加入end url
        """
        res = await self._set_list(end_url_key, url_meta, *url_metas)
        return res

    async def get_end_url(self):
        """
        获取end url
        """

        res = await self._get_list(end_url_key, number=1)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        if url_metas:
            return url_metas[0]

    async def get_end_urls(self, number):
        """
        获取end url
        """
        res = await self._get_list(end_url_key, number=number)
        url_metas = list(map(lambda x: UrlMeta(
            *json.loads(x)), filter(lambda x: x, res)))
        return url_metas

    async def get_end_url_len(self) -> int:
        return await self.memory_db.llen(end_url_key)


class ProxyMixin:
    """
    proxy队列封装
    """

    async def set_proxy(self, proxy: Proxy, *proxys: [Proxy]):
        """
        加入proxy
        """
        temp = [json.dumps(proxy)]
        for i in proxys:
            temp.append(json.dumps(i))
        res = await self.memory_db.lpush(proxy_key, *temp)
        return res

    async def get_proxy(self):
        """
        获取proxy
        """

        res = await self.memory_db.lpop(proxy_key, number=1)
        Proxys = list(map(lambda x: Proxy(
            *json.loads(x)), filter(lambda x: x, res)))
        if Proxys:
            return Proxys[0]

    async def get_proxys(self, number):
        """
        获取proxy
        """
        res = await self.memory_db.lpop(proxy_key, number=number)
        return list(map(lambda x: Proxy(*json.loads(x)), filter(lambda x: x, res)))

    async def get_all_proxys(self):
        """
        获取proxy
        """
        number = await self.memory_db.llen(proxy_key)
        res = await self.memory_db.lpop(proxy_key, number=number)
        return list(map(lambda x: Proxy(*json.loads(x)), filter(lambda x: x, res)))

    async def del_proxy(self, proxy: Proxy):
        res = await self.memory_db.lrem(proxy_key, json.dumps(proxy))
        return res

    async def get_proxy_len(self) -> int:

        return await self.memory_db.llen(proxy_key)

    async def get_all_proxy_range(self):
        res = await self.memory_db.lrange(proxy_key, 0, -1)
        return list(map(lambda x: Proxy(*json.loads(x)), filter(lambda x: x, res)))

class MessageMixin:
    """
    待消息队列封装
    """

    async def set_message(self, message, *messages):
        """
        加入消息
        """
        temp = [json.dumps(message)]
        for i in messages:
            temp.append(json.dumps(i))
        res = await self.memory_db.lpush(message_key, *temp)
        return res
