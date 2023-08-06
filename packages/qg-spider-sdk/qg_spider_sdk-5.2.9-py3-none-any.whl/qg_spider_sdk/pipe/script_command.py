from qg_spider_sdk.entity.url_meta import UrlMeta
import json
import datetime
import asyncio
from qg_struct import config


from .pool_command import service_key, url_record_key, website_key, url_record_key, url_page_key, parse_result_key, special_spider_register_key, website_url_registry_key, website_url_work_table_key
from .list_command import wait_extr_paeg_key, wait_sche_url_key, wait_extr_key, wait_download_key, proxy_wait_download_key, wait_save_url_key, daily_wait_shce_website_key, initial_wait_shce_website_key, daily_proxy_wait_shce_website_key, initial_proxy_wait_shce_website_key, special_wait_shce_website_key, proxy_special_wait_shce_website_key, end_url_key, pause_url_format_key


getListAndSetRecord = """
-- keys [listkey,number,exector,last_fetch_time]
local list = redis.call('LRANGE', KEYS[1], 0, KEYS[2] - 1)
local url_keys = {}
for i, v in ipairs(list) do
    local urlmeta = cjson.decode(v)
    url_keys[i] = urlmeta[1]
end
if (table.getn(url_keys) < 1) then return list end
for i = 1, #url_keys, 3000 do
    local url_records = redis.call('HMGET', 'url_record', unpack(url_keys, i,
                                                                 math.min(
                                                                     i + 2999,
                                                                     #url_keys)))
    local last_url_records = {}
    local j = 1
    for i, v in ipairs(url_records) do
        if (v) then
            local url_record_model = cjson.decode(v)
            url_record_model.belong_queue = KEYS[1]
            url_record_model.exector = KEYS[3]
            url_record_model.last_fetch_time = KEYS[4]
            url_record_model.cur_queue = cjson.null
            last_url_records[j * 2 - 1] = url_record_model.record_id
            last_url_records[j * 2] = cjson.encode(url_record_model)
            j = j + 1
        end
    end
    if (table.getn(last_url_records) > 0) then
        redis.call('HMSET', 'url_record', unpack(last_url_records))
    end
end

redis.call('LTRIM', KEYS[1], KEYS[2], -1)
return list

"""


class ScriptMixin:
    """
    lua脚本封装
    """
    need_flush_keys = [url_record_key, website_key, url_record_key,
                       url_page_key, parse_result_key, special_spider_register_key,
                       wait_extr_paeg_key, wait_sche_url_key, wait_extr_key, wait_download_key,
                       proxy_wait_download_key, wait_save_url_key, daily_wait_shce_website_key,
                       initial_wait_shce_website_key, daily_proxy_wait_shce_website_key,
                       initial_proxy_wait_shce_website_key, special_wait_shce_website_key,
                       proxy_special_wait_shce_website_key, end_url_key]
    need_flush_dynamic_keys = [
        pause_url_format_key, website_url_registry_key, website_url_work_table_key]

    async def _get_list(self, queuename, number, exector=service_key, last_fetch_time=datetime.datetime.now().timestamp()):
        """
        从队列获取url
        """
        if number < 1:
            return []
        sha1 = await self.memory_db._con.hget('script', 'getList')
        if not sha1:
            sha1 = await self.memory_db._con.script_load(getListAndSetRecord)
            await self.memory_db._con.hset('script', 'getList', sha1)
        try:
            res = await self.memory_db._con.evalsha(sha1,  [queuename, number, exector,
                                                            last_fetch_time])
        except Exception as e:
            # 异常删除 getList 脚本,下次调用会自动生成新的脚本
            await self.memory_db._con.hdel('script', 'getList')
            raise e
        return res

    async def _set_list(self, queuename, *urlMetas):
        """
        从队列获取url 事务设置record 分片set 10000一条
        """
        if urlMetas:
            i = 0
            while True:
                items = urlMetas[i:i+10000]
                i += 10000
                if not items:
                    break
                temp = [json.dumps(i) for i in items]
                records = await self.get_url_records(
                    *[urlMeta.key for urlMeta in items])
                pairs = []
                for record in records:
                    record.last_fetch_time = None
                    record.belong_queue = None
                    record.exector = None
                    record.cur_queue = queuename
                    pairs.append(record.record_id)
                    pairs.append(json.dumps(record))
                if pairs:
                    tr = self.memory_db._con.multi_exec()
                    tr.hmset(url_record_key, *pairs)
                    tr.rpush(queuename, *temp)
                    await tr.execute()

    async def _set_list_lpush(self, queuename, *urlMetas):
        """
        从队列获取url 事务设置record 分片set 10000一条
        """
        if urlMetas:
            i = 0
            while True:
                items = urlMetas[i:i+10000]
                i += 10000
                if not items:
                    break
                temp = [json.dumps(i) for i in items]
                records = await self.get_url_records(
                    *[urlMeta.key for urlMeta in items])
                pairs = []
                for record in records:
                    record.last_fetch_time = None
                    record.belong_queue = None
                    record.exector = None
                    record.cur_queue = queuename
                    pairs.append(record.record_id)
                    pairs.append(json.dumps(record))
                if pairs:
                    tr = self.memory_db._con.multi_exec()
                    tr.hmset(url_record_key, *pairs)
                    tr.lpush(queuename, *temp)
                    await tr.execute()

    async def flush_data(self):
        for i in self.need_flush_dynamic_keys:
            keys = await self.memory_db.keys(i.format('*'))
            if keys:
                await self.memory_db.delete(*keys)
        await self.memory_db.delete(*self.need_flush_keys)
