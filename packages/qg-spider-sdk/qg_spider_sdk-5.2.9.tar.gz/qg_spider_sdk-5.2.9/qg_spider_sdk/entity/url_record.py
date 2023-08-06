class UrlRecord(dict):
    """
    url記錄表
    """

    def __init__(self, site_code: int = None, task_number: str = None,
                 url: str = None, download_time: str = None, during: float = None, url_type: str = '',
                 status: str = None, record_id: str = None, deep: int = 0, father_id: int = None, try_nums: int = 0, proxy_try_nums: int = 0, si_success: int = None, site_state_code: str = '', work_type: str = '',
                 last_fetch_time: int = None, belong_queue: str = None, exector: str = None,
                 cur_queue: str = None, **kwargs):

        if not record_id:
            raise ValueError('record_id必填')
        if not site_code:
            raise ValueError('sitecode必填')
        if not task_number:
            raise ValueError('task_number必填')
        if not url:
            raise ValueError('url必填')
        self.record_id = record_id
        self.site_code = site_code
        self.task_number = task_number
        self.url = url
        self.download_time = download_time
        self.during = during
        self.url_type = url_type
        self.status = status
        self.deep = deep
        self.father_id = father_id
        self.try_nums = try_nums
        self.proxy_try_nums = proxy_try_nums
        self.si_success = si_success
        self.site_state_code = site_state_code
        self.work_type = work_type
        self.last_fetch_time = last_fetch_time
        self.belong_queue = belong_queue
        self.exector = exector
        self.cur_queue = cur_queue  # 当前所处队列
        super().__init__(self.__dict__)

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
