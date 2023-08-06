import json
"""
网站类实体封装
"""
from qg_spider_sdk.enums import WebsiteExecuteStatus
from qg_tool.tool import omit


class Website(dict):

    def __init__(self, site_code: int, site_name: str, site_type: str, task_number: str, site_state_code: str, status, priority: (
            int, float), proxy: bool,  interval: str, work_type: str, homepage: str,
        collection_weight: str, site_down_type_code: str, deep: int = 1, during: float = 0, start_urls: list = [], start_time: str = None, params: dict = {}, last_start_time: str = None, deny_rules: [str] = [], timeout: int = 20,
            crawl_type: str = None, spider_name: str = '', encoding_rules: list = [], has_encoding: bool = True, has_ip_proxy: bool = True, has_entrance_mould: int = 0, si_more_rules: int = None, more_rules: [] = None, langs: [] = [],
            middleWares=[], **kwargs):
        self.site_code = site_code
        self.site_name = site_name
        self.site_type = site_type
        self.task_number = task_number
        self.site_state_code = site_state_code
        self.start_time = start_time
        self.status = status
        self.priority = priority
        self.proxy = proxy
        self.start_urls = start_urls
        self.params = params
        self.during = during
        self.deep = deep
        self.interval = interval
        self.work_type = work_type
        self.homepage = homepage
        self.collection_weight = collection_weight
        self.site_down_type_code = site_down_type_code
        self.last_start_time = last_start_time
        self.deny_rules = deny_rules
        self.timeout = timeout
        self.crawl_type = crawl_type
        self.spider_name = spider_name
        self.encoding_rules = encoding_rules
        self.has_encoding = has_encoding
        self.has_ip_proxy = has_ip_proxy
        self.has_entrance_mould = has_entrance_mould
        self.si_more_rules = si_more_rules
        self.more_rules = more_rules
        self.langs = langs
        self.middleWares = middleWares
        super().__init__(self.__dict__)

    def update(self, website):
        self.__dict__ = website.__dict__
        super().__init__(self.__dict__)
        return self

    def update_analgesia(self, website):
        self.__dict__ = {
            **omit(website.__dict__, 'task_number',
                   'status', 'last_start_time'),
            'task_number': self.__dict__['task_number'],
            'status': self.__dict__['status'],
            'last_start_time': self.__dict__['last_start_time'],
        }
        super().__init__(self.__dict__)
        return self

    def __setattr__(self, name, value, setattr=True):
        if setattr:
            self.__setitem__(name, value, False)

        return super().__setattr__(name, value)

    def __setitem__(self, key, value, setitem=True):
        if key == '__dict__':
            return
        if setitem:
            self.__setattr__(key, value, False)
        return super().__setitem__(key, value)

    def get_deep(self):
        return self.deep

    def get_collection_weight(self):
        return self.collection_weight

    def get_site_code(self):
        return self.site_code

    def get_site_name(self):
        return self.site_name

    def get_params(self):
        return self.params

    def get_start_time(self):
        return self.start_time

    def get_site_type(self):
        return self.site_type

    def get_work_type(self):
        return self.work_type

    def get_site_state_code(self):
        return self.site_state_code

    def get_content_url_rule(self):
        return self.params.get('content_url_rule')

    def get_crawl_url_rule(self):
        return self.params.get('can_crawl_rule')

    def get_deny_url_rules(self):
        return self.deny_rules

    def get_resolv_rule(self):
        return self.params.get('resolv_rule')

    def get_resolv_exclude(self):
        resolv_rule = self.get_resolv_rule()
        if resolv_rule:
            return resolv_rule.get('exclude')
        else:
            return None

    def si_site_start(self):
        if self.status == WebsiteExecuteStatus.started.code:
            return True
        if self.status == WebsiteExecuteStatus.wait_schedule.code:
            return True

    def si_site_stop(self):
        if self.status == WebsiteExecuteStatus.stopped.code:
            return True
        if self.status == WebsiteExecuteStatus.disabled.code:
            return True
        if self.status == WebsiteExecuteStatus.wait_stop.code:
            return True

    def si_site_stop_not_wait(self):
        if self.status == WebsiteExecuteStatus.stopped.code:
            return True
        if self.status == WebsiteExecuteStatus.disabled.code:
            return True

    def si_site_wait_stop(self):
        if self.status == WebsiteExecuteStatus.wait_stop.code:
            return True

    def si_site_paused(self):
        if self.status == WebsiteExecuteStatus.paused.code:
            return True

    def get_task_number(self):
        return self.task_number

    def get_resolv_title(self):
        resolv_rule = self.get_resolv_rule()
        if resolv_rule:
            return resolv_rule.get('title')
        else:
            return None

    def get_resolv_content(self):
        resolv_rule = self.get_resolv_rule()
        if resolv_rule:
            return resolv_rule.get('content')
        else:
            return None

    def get_resolv_source(self):
        resolv_rule = self.get_resolv_rule()
        if resolv_rule:
            return resolv_rule.get('source')
        else:
            return None

    def get_resolv_plate(self):
        resolv_rule = self.get_resolv_rule()
        if resolv_rule:
            return resolv_rule.get('plate')
        else:
            return None

    def get_resolv_author(self):
        resolv_rule = self.get_resolv_rule()
        if resolv_rule:
            return resolv_rule.get('author')
        else:
            return None

    def get_resolv_publish_time(self):
        resolv_rule = self.get_resolv_rule()
        if resolv_rule:
            return resolv_rule.get('publish_time')
        else:
            return None
