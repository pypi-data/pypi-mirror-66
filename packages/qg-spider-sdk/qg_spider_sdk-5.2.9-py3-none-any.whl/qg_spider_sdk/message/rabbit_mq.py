import asyncio
import aio_pika
from qg_struct.config import config
import uuid
import json
import inspect
import traceback
import logging
import os
from qg_struct import init_log
init_log()

website_queue_name = 'website' + config['app_name'] + str(uuid.uuid1())
website_routing_key = 'website.#'
topic_exchange_name = 'website'
download_website_notification = 'download_website_queue'
finish_website_bloom_notification = 'finish_website_bloom_queue'
special_spider_close_queue = 'special_spider_close_queue'


class RabbitMq(object):
    website_callback = set()

    async def open(self, wait_time=5):
        try:
            self.connection = await aio_pika.connect_robust(
                config['rabbitMQ']['url']
            )
            self.channel = await self.connection.channel()    # type: aio_pika.Channel
            self.website_exchange = await self.channel.declare_exchange(
                topic_exchange_name, aio_pika.ExchangeType.TOPIC, auto_delete=True
            )
            asyncio.ensure_future(self.receive_website_msg())
        except:
            logging.error(traceback.format_exc())
            logging.error('rabbit连接错误,强制退出')
            os._exit(1)

    async def send_msg(self, sbody: str, msg_type):
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=sbody.encode()
            ),
            routing_key=msg_type,
            timeout=60
        )

    async def send_website_msg(self, sbody: str, wait_time=5):
        error = False
        try:
            await self.website_exchange.publish(
                aio_pika.Message(
                    type=website_queue_name,
                    body=sbody.encode()
                ),
                routing_key=website_routing_key
            )
        except:
            logging.error(traceback.format_exc())
            error = True
        finally:
            if error:
                logging.error(f'发送网站消息异常 ,{wait_time} s 后重发')
                await self.send_website_msg(sbody, wait_time=min(wait_time * 2, 120))

    def register_website_callback(self, callback):
        self.website_callback.add(callback)

    async def receive_website_msg(self):
        queue = await self.channel.declare_queue(
            website_queue_name, auto_delete=True, arguments={'x-expires': 1000 * 180}
        )
        await queue.bind(self.website_exchange, website_routing_key)
        async for message in queue:
            with message.process():
                if message.type == website_queue_name:
                    continue
                logging.info(f'收到网站同步信息,发送者 {message.type}')
                logging.info(message.body)
                for callback in self.website_callback:
                    if inspect.iscoroutinefunction(callback):
                        await callback(message.body)
                    else:
                        callback(message.body)

    async def send_url_download_msg(self, site_code: str):
        return await self.send_msg(site_code, download_website_notification)

    async def receive_url_download_msg(self, callback):
        return await self.receive_msg(download_website_notification, callback)

    async def send_website_bloom_finish_msg(self, site_code: str):
        return await self.send_msg(site_code, finish_website_bloom_notification)

    async def receive_website_bloom_finish_msg(self, callback):
        return await self.receive_msg(finish_website_bloom_notification, callback)

    async def send_special_spider_close_msg(self, spider_name: str):
        return await self.send_msg(spider_name, special_spider_close_queue)

    async def receive_special_spider_close_msg(self, callback):
        return await self.receive_msg(special_spider_close_queue, callback)

    async def receive_msg(self, queue_name, callback):
        queue = await self.channel.declare_queue(
            queue_name, auto_delete=True
        )
        async for message in queue:
            with message.process():
                if inspect.iscoroutinefunction(callback):
                    await callback(message.body)
                else:
                    callback(message.body)


rabbit_mq = RabbitMq()
asyncio.get_event_loop().run_until_complete(rabbit_mq.open())
