import asyncio
import pika
from qg_struct.config import config
import uuid
import json
import inspect
import traceback

website_queue_name = 'website' + str(uuid.uuid1())
website_routing_key = 'website.#'
topic_exchange_name = 'website'
download_website_notification = 'download_website_queue'
finish_website_bloom_notification = 'finish_website_bloom_queue'
special_spider_close_queue = 'special_spider_close_queue'


class RabbitMqSync(object):
    @classmethod
    def open(self):

        url = config['rabbitMQ']['url']
        url_attr = url.split('@')
        rabitMQip = url_attr[1].split(':')[0]
        rabitMQport = url_attr[1].split(':')[1].replace('/', '')
        rabitMQuser = url_attr[0].replace('amqp://', '').split(':')[0]
        rabitMQpassword = url_attr[0].replace('amqp://', '').split(':')[1]
        credentials = pika.PlainCredentials(rabitMQuser, rabitMQpassword)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabitMQip, rabitMQport, '/', credentials))

        self.channel = self.connection.channel()
    @classmethod
    def send_msg(self, sbody: str, msg_type, wait_time=5):
        try:
            self.channel.basic_publish(exchange='', routing_key=msg_type,
                                       body=sbody.encode())
        except:
            print(traceback.format_exc())
            #self.connection.process_data_events()
            self.open()
            self.channel.basic_publish(exchange='', routing_key=msg_type,
                                       body=sbody.encode())
    @classmethod
    def send_url_download_msg(self, site_code: str):
        return self.send_msg(site_code, download_website_notification)


rabbit_mq_sync = RabbitMqSync()
rabbit_mq_sync.open()
