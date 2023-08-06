# 爬虫系统公共类封装

## 目标

- [x] redis db 划分
- [x] url 记录池封装
- [x] 下载页面池封装
- [x] 解析结果池封装
- [x] 网站信息类封装

## redis db 划分(0-15)

```
- 0 -> 常用的队列与有序集或集合
其中的hash表定义
    - website -> 网站信息
    - url_record -> url 记录池
    - url_page -> 下载页面池封装
    - parse_result -> 解析结果池封装
- 10-15 -> 监控自行处理
```

