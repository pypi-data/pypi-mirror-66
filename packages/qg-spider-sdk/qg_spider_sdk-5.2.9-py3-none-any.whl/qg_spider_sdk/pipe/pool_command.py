import uuid
import datetime
from qg_spider_sdk.entity import Website, ProxyOld, ParseResult, UrlRecord, UrlMeta
from qg_struct import config
import json
import random

website_key = 'website'
url_record_key = 'url_record'
url_page_key = 'url_page'
parse_result_key = 'parse_result'
website_url_registry_key = 'website_url_registry_{}'
website_url_hash_key = 'hash'
website_url_work_table_key = 'website_url_work_table_{}'
special_spider_register_key = 'special_spider_register'
config_key = 'config'
service_register_key = 'service_register'
service_key = '{ip}:{port}/{app_name}'.format(
    ip=config['ip'], port=config['port'], app_name=config['app_name'])


url_count_num = 3


class WebsiteMixin:

    async def get_website(self, site_code):
        """
        获取网站信息
        """
        res = await self.memory_db.hget(website_key, site_code)
        websites = list(map(lambda website: Website(
            **json.loads(website)), filter(lambda x: x, res)))
        if websites:
            return websites[0]

    async def get_websites(self, site_code, *site_codes):
        """
        获取网站信息
        """
        res = await self.memory_db.hget(website_key, site_code, *site_codes)
        return list(map(lambda website: Website(
            **json.loads(website)), filter(lambda x: x, res)))

    async def set_website(self, website: Website):
        """
        设置网站信息
        """
        res = await self.memory_db.hset(website_key, website['site_code'], json.dumps(website))
        return res

    async def set_websites(self, websites: [Website]):
        """
        设置网站信息
        """
        temp = []
        for website in websites:
            temp.append(website['site_code'])
            temp.append(json.dumps(website))
        res = await self.memory_db.hset(website_key, *temp)
        return res

    async def delete_website(self, site_code, *site_codes):
        """
        删除网站信息
        """
        await self.memory_db.hdel(website_key, site_code, *site_codes)

    async def get_all_site_codes(self):
        """
        返回所有的网站site_code
        """
        res = await self.memory_db.hkeys(website_key)
        return list(map(lambda x: int(res), filter(lambda x: x, res)))

    async def get_all_websites(self):
        """
        返回所有的网站信息
        """
        res = await self.memory_db.hvals(website_key)
        return list(map(lambda website: Website(**json.loads(website)), filter(lambda x: x, res)))

    async def get_website_len(self):
        return await self.memory_db.hlen(website_key)


class UrlRecordMixin:

    async def get_url_record(self, key) -> UrlRecord:
        """
        获取url
        :param key:
        :param keys:
        :return:
        """
        res = await self.memory_db.hget(url_record_key, key)
        url_records = list(map(lambda x: UrlRecord(
            **json.loads(x)), filter(lambda x: x, res)))
        if url_records:
            return url_records[0]

    async def get_url_records(self, key, *keys) -> [UrlRecord]:
        """
        获取url
        :param key:
        :param keys:
        :return:
        """
        res = await self.memory_db.hget(url_record_key, key, *keys)
        return list(map(lambda x: UrlRecord(**json.loads(x)), filter(lambda x: x, res)))

    async def set_url_record(self, key, record: UrlRecord, *pairs):
        """
        设置url记录
        :param key:
        :param record:
        :param pairs:长度必须为偶数
        :return:
        """
        records = [key, json.dumps(record)]
        for i, pair in enumerate(pairs):
            if i % 2:
                records.append(json.dumps(pair))
            else:
                records.append(pair)
        res = await self.memory_db.hset(url_record_key, *records)
        return res

    async def delete_url_record(self, key, *keys):
        """
        删除url记录
        :param key:
        :param keys:
        :return:
        """
        return await self.memory_db.hdel(url_record_key, key, *keys)

    async def get_url_record_len(self):
        return await self.memory_db.hlen(url_record_key)

    async def get_all_url_records(self) -> [UrlRecord]:
        """获取所有的url记录

        Returns:
            [UrlRecord] -- [description]
        """
        url_records = await self.memory_db.hvals(url_record_key)
        return list(map(lambda url_record: UrlRecord(**json.loads(url_record)),
                        filter(lambda x: x, url_records)))

    async def clear_url_record(self):
        return await self.memory_db.delete(url_record_key)


class UrlPageMixin:
    async def get_url_page(self, key):
        """
        获取html
        :param key:
        :param keys:
        :return:
        """
        res = await self.memory_db.hget(url_page_key, key)
        htmls = list(filter(lambda x: x, res))
        if htmls:
            return htmls[0]

    async def get_url_pages(self, key, *keys):
        """
        获取html
        :param key:
        :param keys:
        :return:
        """
        res = await self.memory_db.hget(url_page_key, key, *keys)
        return list(filter(lambda x: x, res))

    async def set_url_page(self, key, page: (str, bytes), *pairs):
        """
        设置html
        :param key:
        :param page:
        :param pairs:长度必须为偶数
        :return:
        """
        res = await self.memory_db.hset(url_page_key, key, page, *pairs)
        return res

    async def delete_url_page(self, key, *keys):
        """
        删除html
        :param key:
        :param keys:
        :return:
        """
        return await self.memory_db.hdel(url_page_key, key, *keys)

    async def get_url_page_len(self):
        return await self.memory_db.hlen(url_page_key)

    async def clear_url_page(self):
        return await self.memory_db.delete(url_page_key)


class ParseResultMixin:
    async def get_parse_result(self, key):
        """
        获取解析结果
        :param key:
        :param keys:
        :return:
        """
        res = await self.memory_db.hget(parse_result_key, key)
        parse_results = list(map(lambda x: ParseResult(
            **json.loads(x)), filter(lambda x: x, res)))
        if parse_results:
            return parse_results[0]

    async def get_parse_results(self, key, *keys):
        """
        获取解析结果
        :param key:
        :param keys:
        :return:
        """
        res = await self.memory_db.hget(parse_result_key, key, *keys)
        return list(map(lambda x: ParseResult(**json.loads(x)), filter(lambda x: x, res)))

    async def set_parse_result(self, key, result: ParseResult, *pairs):
        """
        设置解析结果
        :param key:
        :param result:
        :param pairs:长度必须为偶数
        :return:
        """
        temp = []
        for i, value in enumerate(pairs):
            if i % 2:
                temp.append(value)
            else:
                temp.append(json.dumps(value))
        res = await self.memory_db.hset(parse_result_key, key, json.dumps(result), *temp)
        return res

    async def delete_parse_result(self, key, *keys):
        """
        删除解析结果
        :param key:
        :param keys:
        :return:
        """
        return await self.memory_db.hdel(parse_result_key, key, *keys)

    async def get_url_parse_result_len(self):
        return await self.memory_db.hlen(parse_result_key)

    async def clear_url_result(self):
        return await self.memory_db.delete(parse_result_key)


class WebsiteUrlRegistryMixin:
    """
    url 登记表
    """

    async def set_website_url_registry_count(self, site_code, key, *keys):
        """
        设置注册登记表
        :param key:
        :return:
        """
        pairs = []
        for i in keys:
            pairs.append(i)
            pairs.append(url_count_num)
        res = await self.memory_db.hset(website_url_registry_key.format(site_code), website_url_hash_key, f'{service_key}-{datetime.datetime.now().timestamp()}', key, url_count_num, *pairs)
        return res

    async def delete_website_url_registry_count(self, site_code, key, *keys):
        """
        删除field
        """
        await self.memory_db.hset(website_url_registry_key.format(site_code), website_url_hash_key, f'{service_key}-{datetime.datetime.now().timestamp()}')
        return await self.memory_db.hdel(website_url_registry_key.format(site_code),  key, *keys)

    async def get_all_website_url_key(self, site_code):
        """
        获取注册表所有的url key
        """
        res = await self.memory_db.hkeys(website_url_registry_key.format(site_code))
        return list(map(lambda y: str(y, encoding='utf-8'), filter(lambda x: x and str(x, encoding='utf-8') != website_url_hash_key, res)))

    async def has_website_url_registry(self, site_code):
        """
        网站注册表是否存在
        """
        return await self.memory_db.exists(website_url_registry_key.format(site_code))

    async def has_website_url_record(self, site_code) -> bool:
        """
        网站注册表是否还有记录
        """
        register_len = await self.memory_db.hlen(website_url_registry_key.format(site_code))
        return register_len > 1

    async def delete_website_url_registry(self, site_code):
        """
        删除网站注册表
        """
        return await self.memory_db.delete(website_url_registry_key.format(site_code))

    async def get_website_url_registry_hash(self, site_code):
        res = await self.memory_db.hget(website_url_registry_key, site_code)
        if res and res[0]:
            return str(res[0], encoding='utf-8')


class SpecialSpiderRegisterMixin:

    async def get_special_spider_launcher_ip(self, site_code):
        """
        获取独立爬虫启动器位置
        """
        res = await self.memory_db.hget(special_spider_register_key, site_code)
        if res and res[0]:
            return str(res[0], encoding='utf-8')

    async def get_special_spider_launcher_ip_list(self, site_code, *site_codes):
        """
        获取独立爬虫启动器位置列表
        """
        res = await self.memory_db.hget(special_spider_register_key, site_code, *site_codes)
        if res:
            return list(map(lambda x: str(x, encoding='utf-8'), filter(lambda x: x, res)))

    async def set_special_spider_launcher_ip(self, site_code, ip, *pairs):
        """
        设置独立爬虫启动器位置
        """
        res = await self.memory_db.hset(special_spider_register_key, site_code, ip, *pairs)
        return res

    async def delete_special_spider_register(self, site_code, *site_codes):
        """
        删除独立爬虫启动器位置
        """
        return await self.memory_db.hdel(special_spider_register_key, site_code, *site_codes)

    async def get_all_special_spider_site_code(self):
        """
        获取所有的独立爬虫site_code
        """
        res = await self.memory_db.hkeys(special_spider_register_key)
        return list(map(lambda y: int(y), filter(lambda x: x, res)))

    async def get_all_special_spider_info(self):
        """
        获取所有的分配独立爬虫信息
        """
        res = await self.memory_db.hgetall(special_spider_register_key)
        temp = {}
        for key in res:
            temp[str(key, encoding='utf-8')] = str(res[key], encoding='utf-8')
        return temp


class ConfigMixin:

    async def get_config(self, config_type):
        """
        获取配置信息
        """
        return (await self.memory_db.hget(config_key, config_type))[0]

    async def set_config(self, config_type, value, *pairs):
        """
        设置配置信息
        """
        res = await self.memory_db.hset(config_key, config_type, value, *pairs)
        return res

    async def delete_config(self, config_type, *config_types):
        """
        删除配置信息
        """
        await self.memory_db.hdel(config_key, config_type, *config_types)

    async def get_all_config(self):
        """获取所有配置信息
        """
        return await self.memory_db.hgetall(config_key)

    async def get_survival_time_threshold(self):
        res = await self.get_config('survival_time_threshold')
        if not res:
            res = 30
            await self.set_config('survival_time_threshold', res)
        return int(res)


class ServiceMixin:
    """服务登记表

    """

    async def get_service_info(self, serviceKey: str = None) -> dict:
        """获取服务信息

        Arguments:
            serviceKey {str} -- ip:port/[app_name]

        Returns:
            int -- [上次存活时间]
        """
        serviceKey = serviceKey if serviceKey else service_key
        res = await self.memory_db.hget(service_register_key, serviceKey)
        return res[0] and json.loads(res[0])

    async def set_service_info(self, options: dict):
        res = await self.memory_db.hset(service_register_key, service_key, json.dumps(options))
        return res

    async def delete_service(self, *service_keys):
        """
        删除服务
        """
        await self.memory_db.hdel(service_register_key, *service_keys)

    async def get_all_services(self) -> dict:
        """获取所有服务

        Returns:
            dict -- [description]
        """
        res = await self.memory_db.hgetall(service_register_key)
        temp = {}
        for key in res:
            temp[str(key, encoding='utf-8')] = json.loads(res[key])
        return temp


class WebsiteWorkTableMixin:
    """网站工作表

    """

    async def set_website_work_table_flag(self, site_code, zero_or_one: int):
        res = await self.memory_db.hset(website_url_work_table_key.format(site_code), service_key, zero_or_one)
        # 设置五分钟过期
        await self.memory_db.expire(website_url_work_table_key.format(site_code), 300)
        return res

    async def get_all_website_work_table_flags(self, site_code) -> dict:
        """获取该网站所有工作情况

        Returns:
            dict -- [description]
        """
        res = await self.memory_db.hgetall(website_url_work_table_key.format(site_code))
        temp = {}
        for key in res:
            temp[str(key, encoding='utf-8')] = int(res[key])
        return temp

    async def delete_website_work_table(self, site_code):
        """
        删除网站工作情况表
        """
        return await self.memory_db.delete(website_url_work_table_key.format(site_code))
