"""
系统资源实体封装
"""
from typing import NamedTuple

class Proxy(NamedTuple):
    ip: str  # url key
    port: int  # 网站代码
    create_time: float  # 时间