from qg_tool.tool import find
from typing import NamedTuple, Any


class EnumMeta(NamedTuple):
    code: str   # url key
    value: Any  # 网站代码


class WebsiteExecuteStatus:
    wait_schedule = EnumMeta('wait_schedule', '待调度')
    started = EnumMeta('started', '已启动')
    paused = EnumMeta('paused', '已暂停')
    wait_stop = EnumMeta('wait_stop', '待停止')
    stopped = EnumMeta('stopped', '已停止')
    disabled = EnumMeta('disabled', '已停用')

    @classmethod
    def get(cls, code):
        return find(lambda x: x.code == code, filter(lambda x: type(x) == EnumMeta, vars(cls).values()))


# class MessageEnum:
#     # 下载前
#     DOWNLOAD_BEFORE = 'MonitoringMQ_spider_before'
#     # 下载后
#     DOWNLOAD_AFTER = 'MonitoringMQ_spider_after'
#     # 网站开始
#     WEBSITE_START = 'MonitoringMQ_website_start'
#     # 网站停止
#     WEBSITE_STOP = 'MonitoringMQ_website_stop'
#     # 网站暂停
#     WEBSITE_PAUSE = 'MonitoringMQ_website_pause'
#     # 网站恢复
#     WEBSITE_RECOVER = 'MonitoringMQ_website_recover'
#     # url调度
#     DISPATCH_URL = 'MonitoringMQ_dispatch_url'
#     # 资源
#     RECOURSE = 'MonitoringMQ_recourse'
#     # 解析
#     RESOLV = 'MonitoringMQ_resolv'
#     # 网页保存
#     SAVE_PAGE = 'MonitoringMQ_save_page'
#     # 结果保存
#     SAVE_RESULT = 'MonitoringMQ_save_result'
#     # url保存
#     SAVE_URL = 'MonitoringMQ_save_url'


__all__ = ('WebsiteExecuteStatus', 'EnumMeta','DownloadEnum')
