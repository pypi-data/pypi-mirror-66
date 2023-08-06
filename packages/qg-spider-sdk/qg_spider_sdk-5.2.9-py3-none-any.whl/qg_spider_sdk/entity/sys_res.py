"""
系统资源实体封装
"""

class SysRes(dict):
    def __init__(self,ip,process_name:str,process_type:str,cpuper,netnum,ramper,ramnum,disk,diskper,siworking):
        self.ip = ip
        self.process_name = process_name
        self.cpuper = cpuper
        self.netnum = netnum
        self.ramper = ramper
        self.ramnum = ramnum
        self.disk = disk
        self.diskper = diskper
        self.siworking = siworking
        self.process_type = process_type
        return super().__init__(self.__dict__)
    