####开发抖音网站说明文档
1.设计思路
- 评论抓取对应 titktok_comment.py get_user_commits进行数据抓取
- tips:
   - 目前的部署方式为一台节点上面部署此业务方向的爬虫，后续抖音开发数据，可能会考虑多部署几台。
   
2.采集脚本说明
- titktok_comment.py:提取抖音视频下的页面信息

├── Spider_titktok                                  站点脚本文件夹（一个文件夹是一个站点的采集worker脚本)
│   ├── config.ini                                  常用变量配置(例如 代理ip设置)
│   ├── Cofig_parse.py                              配置文件的解析
│   ├── README.md                                   文档说明
│   ├── requirements.txt                            依赖库
│   ├── titktok_comment.py                          抖音评论采集脚本
└── (douyin cralwer)

3.目录结构说明
- Spider_titktok 表示抖音爬虫
- 生成json数据 抖音评论数据的采集
