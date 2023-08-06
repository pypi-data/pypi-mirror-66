class ParseResult(dict):
    def __init__(self, site_code: int = None, title:str='', create_date:str='', source:str='', plate:str='', author:str='', publish_time:str='', content:str='', url:str='',site_state_code:str='',work_type:str='',task_number:str=''):
        self.site_code = site_code
        self.create_date = create_date
        self.title = title
        self.source = source
        self.plate = plate
        self.author = author
        self.publish_time = publish_time
        self.content = content
        self.url = url
        self.site_state_code = site_state_code
        self.work_type = work_type
        self.task_number = task_number
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
