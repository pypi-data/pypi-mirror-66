"""
系统资源实体封装
"""


class ProxyOld(dict):
    def __init__(self, proxy, ipType: str, area: str, speed: str, requestType: str, num: int):
        self.proxy = proxy
        self.ipType = ipType
        self.area = area
        self.speed = speed
        self.requestType = requestType
        self.num = num
        super().__init__(self.__dict__)
