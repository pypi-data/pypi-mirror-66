from qg_spider_sdk.client.bloom_filter_client import BloomFilterClient
from qg_spider_sdk.message import rabbit_mq_sync
import datetime
import os
import re
import json
from urllib import parse
from urllib import request
import time
import traceback
import json
from qg_struct import config
#from dateutil.relativedelta import relativedelta
rex = r'((?<=[^0-9])|^)[1-2][0-9]{3}([-/年]|\.)?((\s*[0-1]{0,1}[0-9])([-/月]|\.)(\s*[0-3]{0,1}[0-9])|[0-1][0-9]([0-3][0-9]))((?=[^0-9])|$)'
class IndependMan(object):

    @classmethod
    def exist_and_add(cls,loop,url,site_code,work_type):
        if work_type=='test':
            isexist = cls.exist_test(loop,url,site_code)
        else:
            isexist = cls.exist(loop,url,site_code)
        return isexist

    @classmethod
    def exist(cls,loop,url,site_code):
        result=loop.run_until_complete(BloomFilterClient.exist_content(url,site_code))
        return result

    @classmethod
    def exist_test(cls,loop,url,site_code):
        result=loop.run_until_complete(BloomFilterClient.exist_test(url,site_code))
        return result

    @classmethod
    def add(cls,loop,url,site_code):
        result=loop.run_until_complete(BloomFilterClient.add_content(url,site_code))

    @classmethod
    def add_test(cls,loop,url,site_code):
        result=loop.run_until_complete(BloomFilterClient.add_test(url,site_code))

    @classmethod
    def init_env(cls,site_code):
        custom_settings = {}
        # 新建日志存放目录
        folder = os.path.exists("log")
        if not folder:
            os.makedirs("log")
        today = datetime.datetime.now()
        log_file_path = ("log/"+site_code+"_{}_{}_{}_.log").format(
            today.year, today.month, today.day)
        custom_settings = {'LOG_FILE': log_file_path,'LOG_LEVEL':'INFO','ROBOTSTXT_OBEY':False,'CONCURRENT_REQUESTS':1}
        

        return custom_settings

    @classmethod
    def find(cls,func, array):
        for item in array:
            if func(item):
                item = item.replace('site_code=', '') if item else None
                return item
        return None

    @classmethod
    def remove_html_tag(cls,txt):
        html_tag_cl = re.compile('<(/){0,1}.+?>')
        br_tag_cl = re.compile('<(/){0,1}\s*br\s*(/){0,1}>')
        space_cl = re.compile('\&nbsp;|&gt;|\xa0')
        space_cl2 = re.compile('{{.*}}')
        # 替换换行标签
        content = br_tag_cl.sub('\n\r', str(txt))
        # 去除html标签
        content = html_tag_cl.sub("", content)
        content = space_cl.sub(" ", content)
        content = space_cl2.sub(" ", content)
        return content

    @classmethod
    def remove_js_tag(cls,txt):
        repl = re.compile('<!-[\s\S]*?-->')
        js_tag = re.compile('<script[^>]*>([\s\S](?!<script))*?</script>')
        text = repl.sub('', txt)
        text = js_tag.sub('', txt)
        return text

    @classmethod
    def remove_blank(value):
        value = value.replace("\n", "")
        value = value.replace(" ", "")
        value = value.replace("\r", "")
        value = value.replace(" ", "")
        value = remove_html_tag(value)
        value = value.replace(")", "")
        value = value.replace("(", "")
        return value


    @classmethod
    def extract_date(cls,targetstr, site_language_code=None):
        targetstr = cls.remove_html_tag(targetstr)
        print(targetstr)
        
        rexp = re.search(
            r'今日|今天|today|Today|AGO|ago|Aujourd|сегодня|hoy|分钟前|小时前|時間前', targetstr)
        if rexp:
            dt = datetime.datetime.now()
            return dt.strftime('%Y{y}%m{m}%d{d}').format(
                y='年', m='月', d='日')

        rexp = re.search(r'昨日|昨天|yesterday|hier|Yesterday', targetstr)
        if rexp:
            dt = datetime.datetime.now()
            yesterday = dt + datetime.timedelta(days=-1)
            return yesterday.strftime('%Y{y}%m{m}%d{d}').format(
                y='年', m='月', d='日')

        targetstr2=targetstr.strip()
        rexp = re.search(r'^[0-2]{0,1}[0-9]:[0-5][0-9]', targetstr2)
        if rexp:
            dt = datetime.datetime.now()
            return dt.strftime('%Y{y}%m{m}%d{d}').format(
                y='年', m='月', d='日')

        timestr = re.search(
            r'((?<=[^0-9])|^)[0-3][0-9][\.]([0-1][0-9])[\.]([1-2][0-2]{2}[0-9])', targetstr)
        if timestr:
            targetstr = timestr.group(0)
            targetstrArray = targetstr.split(".")
            return targetstrArray[2]+'年'+targetstrArray[1]+'月'+targetstrArray[0]+'日'

        timestr = re.search(
            r'((?<=[^0-9])|^)[0-3][0-9][\.]([0-1][0-9])[\.]([0-2][0-9])', targetstr)
        if timestr:
            targetstr = timestr.group(0)
            targetstrArray = targetstr.split(".")
            if len(targetstrArray[2]) == 2:
                targetstrArray[2] = "20"+targetstrArray[2]
            return targetstrArray[2]+'年'+targetstrArray[1]+'月'+targetstrArray[0]+'日'
        
        timestr = cls.transdate(targetstr)
        if timestr:
            return timestr

        targetstr2 = targetstr.strip('\r\n').replace(u'\\u3000', u'')
        timestr = re.search(rex, targetstr2)
        if timestr:
            value = re.compile('^.*?(.-|/|年)').search(str(timestr.group(0)))
            timestr = re.sub(r'[^0-9]', '', timestr.group())
            if value:
                if len(value.group(0)) == 3:
                    timestr = "20"+timestr
            timestr=timestr.replace("/","")
            date = datetime.datetime.strptime(timestr, '%Y%m%d')
            return date.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        timestr = re.search(
            r'((?<=[^0-9])|^)[0-3][0-9][/]([0-1][0-9])[/]([0-2]{2}[0-9]{2})', targetstr)
        if timestr:
            targetstr = timestr.group(0)
            timestr = targetstr.split("/")
            return timestr[2]+"年"+timestr[1]+"月"+timestr[0]+"日"
        timestr = re.search(
            r'((?<=[^0-9])|^)[0-1][0-9]{1}[/]([0-3]{0,1}[0-9])[/]([0-2]{1}[0-9])', targetstr)
        if timestr:
            targetstr = timestr.group(0)
            timestr = targetstr.split("/")
            if len(timestr[2]) == 2:
                timestr[2] = "20"+timestr[2]
            return timestr[2]+"年"+timestr[0]+"月"+timestr[1]+"日"

    @classmethod
    def transCommonDate(cls,targetstr):
        targetstr2 = targetstr.strip('\r\n').replace(u'\\u3000', u'')
        timestr = re.search(rex, targetstr2)
        if timestr:
            value = re.compile('^.*?(.-|/|年)').search(str(timestr.group(0)))
            timestr = re.sub(r'[^0-9]', '', timestr.group())
            if value:
                if len(value.group(0)) == 3:
                    timestr = "20"+timestr
            date = datetime.datetime.strptime(timestr, '%Y%m%d')
            return date.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')

    @classmethod
    def transdate(cls,pub_time):
        pub_time=pub_time.replace('\n','')
        pub_time=pub_time.strip()
        year = re.search(r'[2][0][0-2][1-9]', pub_time)
        if year:
            year = year.group(0)
            months_set = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                        'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11',
                        'December': '12','Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11','Dec': '12','Abr':'04'}
            pub_time=pub_time.lower()
            pub_time=pub_time.replace(":","")
            month_rex = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|abr)', pub_time)
            if month_rex:
                month=month_rex.group(0)
                if month.capitalize() in months_set:
                    month=months_set[month.capitalize()]
                    day_rex = re.search(r'[0-3]{0,1}[0-9]{1}', pub_time)
                    if day_rex:
                        day=day_rex.group(0)
                        if len(day) == 1:
                            day = '0' + day
                        return year + '年' + month + '月' + day + '日'

    @classmethod
    def send_before_msg(cls,spider_name,site_code,task_number,first):
        dt = datetime.datetime.now()
        strg =dt.strftime('%Y-%m-%d %H:%M:%S') 
        msgstr={"websitcode":site_code,"taskcode":task_number,"spidername":spider_name,"first":first,"time":strg}
        rabbit_mq_sync.send_msg(json.dumps(msgstr),'MonitoringMQ_spider_before')

    @classmethod
    def send_after_msg(cls,spider_name,isdownok,dur_time,site_code,task_number):
        dt = datetime.datetime.now()
        strg =dt.strftime('%Y-%m-%d %H:%M:%S') 
        msgstr={"websitcode":site_code,"taskcode":task_number,"spidername":spider_name,"isdownok":isdownok,"usetime":dur_time,"time":strg}
        rabbit_mq_sync.send_msg(json.dumps(msgstr),'MonitoringMQ_spider_after')

    @classmethod
    def send_error_msg(cls,ip,errortype,errorlevel,site_code,task_code):

        msgstr={"servtype":"ind_crawl","msgtype":"error","servip":ip,"servname":'spider',"faulttype":errortype,"faultlevel":errorlevel,"sitecode":site_code,"taskcode":task_code,"sendtime":time.time(),'isworking':1}
        body={"FaultMsg":msgstr}
        msg_dict=json.dumps(body)
        return msg_dict

    @classmethod
    def send_warring_msg(cls,ip,warringtype,warringlevel,site_code,task_code):

        msgstr={"servtype":"ind_crawl","msgtype":"warning","servip":ip,"servname":'spider',"faulttype":warringtype,"faultlevel":warringlevel,"sitecode":site_code,"taskcode":task_code,"sendtime":time.time(),'isworking':1}
        body={"FaultMsg":msgstr}
        msg_dict=json.dumps(body)
        return msg_dict


    @classmethod
    def send_resolv_url_msg(self,website,url_count):
        dt = datetime.datetime.now()
        strg =dt.strftime('%Y-%m-%d %H:%M:%S') 
        resolv_msg = {"websitcode":website.get_site_code(),"taskcode":website.get_task_number(),"parseurls":url_count,"time":strg}
        rabbit_mq_sync.send_msg(json.dumps(resolv_msg),'MonitoringMQ_parseurl')

    @classmethod
    def send_resolv_page_msg(self,website,content_count,usetime):
        dt = datetime.datetime.now()
        strg =dt.strftime('%Y-%m-%d %H:%M:%S') 
        resolv_msg = {"websitcode":website.get_site_code(),"taskcode":website.get_task_number(),"parsecontent":content_count,"usetime":usetime,"time":strg}
        rabbit_mq_sync.send_msg(json.dumps(resolv_msg),'MonitoringMQ_parsecontent')

    @classmethod
    def deal_close(self,spider):
        spider.loop.run_until_complete(BloomFilterClient().delete_filter(spider.site_code))

