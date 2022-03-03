import requests
from concurrent.futures import ThreadPoolExecutor
import time
from loguru import logger
import os
import json
from Config_parse import Parser_config
from pprint import pprint
BASE_URL_PATH= os.path.dirname(os.path.abspath(__file__))
class Spider_titk:
    def __init__(self):
        self.headers={
            "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "cookie":"sessionid_ss=2aa9f627fb090859b38f2986ea9729f5",
        }
        #"http://kevin:kevin297@106.53.201.250:7990"
        #填写代理配置
        cfg=Parser_config()
        self.proxy={
            "https":"http://"+cfg.get_user()+":"+cfg.get_passwd()+"@"+cfg.get_ip_port(),
        }
        self.url="https://www.tiktok.com/api/comment/list/"
        self.reply_url="https://www.tiktok.com/api/comment/list/reply/"
        self.TOTAL_count=0

    def get_user_id(self,temp):
        USER_LIST=[]
        for data in (temp):
            data=data.strip().replace('"','')
            USER_LIST.append(data)
        return USER_LIST

    def read_json(self):
        with open(BASE_URL_PATH+"\\user_ids.txt","r") as fp:
             temp=fp.readlines()
        return temp

    def get_comments_list(self,len_,params_list,count):
        num=int(len_/count)
        task_list=[]
        if num==0:
            return task_list
        for i in range(1,int(num+1)):
            params_list[14] = ("cursor",i*count)
            params=tuple(params_list)
            task_list.append(params)
        return task_list

    def parse_reply_params(self,cid,aweme_id):
        params_reply=(
            ('aid', '1988'),
            ('app_language', 'ja-JP'),
            ('app_name', 'tiktok_web'),
            ('battery_info', '1'),
            ('browser_language', 'zh-CN'),
            ('browser_name', 'Mozilla'),
            ('browser_online', 'true'),
            ('browser_platform', 'Linux x86_64'),
            ('browser_version',
             '5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'),
            ('channel', 'tiktok_web'),
            ('comment_id',cid),
            ('cookie_enabled', 'true'),
            ('count', '3'),
            ('current_region', 'JP'),
            ('cursor', '0'),
            ('device_id', '7070368797244556801'),
            ('device_platform', 'web_pc'),
            ('focus_state', 'true'),
            ('fromWeb', '1'),
            ('from_page', 'video'),
            ('history_len', '5'),
            ('is_fullscreen', 'false'),
            ('is_page_visible', 'true'),
            ('item_id',aweme_id),
            ('os', 'linux'),
            ('priority_region', ''),
            ('referer', 'https://www.tiktok.com/@pasioncanella/video/{}'.format(aweme_id)),
            ('region', 'SG'),
            ('root_referer', 'https://www.tiktok.com/foryou?is_copy_url=1&is_from_webapp=v1'),
            ('screen_height', '1080'),
            ('screen_width', '1920'),
            ('tz_name', 'Asia/Shanghai'),
            ('verifyFp', 'verify_8619440063f37a4147ab04c70d884b41'),
            ('webcast_language', 'zh-Hant-TW'),
        )
        self.get_replay_comments(params_reply)
        return params_reply

    def download_reply_json(self,json_data):
        with open("user_reply_comments.json","a",encoding="utf-8")  as fp:
            fp.write(json.dumps(json_data)+'\n')

    def get_replay_comments(self,params_reply):
        try:
            res=requests.get(self.reply_url,headers=self.headers,params=params_reply,proxies=self.proxy,timeout=5)
            if res.status_code==200:
                reply_json_data=res.json()
                self.download_reply_json(reply_json_data)
                #pprint(reply_json_data)
        except Exception as e:
            logger.error(e)

    def get_detail_comments(self,task_params):
        try:
            res=requests.get(self.url,headers=self.headers,params=task_params,proxies=self.proxy,timeout=5)
            if res.status_code==200:
                json_data=res.json()
                self.download_json(json_data)
                self.TOTAL_count+=1
                if json_data['comments'] !=None:
                    for data in json_data['comments']:
                        if data['reply_comment_total']!="0":
                            cid=data['cid']
                            reply_total=data['reply_comment_total']   #获取回复评论的总数
                            aweme_id=data['aweme_id']
                            logger.info("正在获取此用户id:{} 回复评论总数为:{}".format(cid,str(reply_total)))
                            replay_params=self.parse_reply_params(cid,aweme_id)
                            replay_params_list=list(replay_params)
                            replay_task_list=self.get_comments_list(reply_total,replay_params_list,3)
                            if not replay_task_list:
                                time.sleep(3)
                            with ThreadPoolExecutor(100)  as executor:
                                executor.map(self.get_replay_comments, replay_task_list)
                return json_data
        except Exception as e:
            logger.error(e)

    def get_detail_comment_total(self,task_params):
        try:
            res = requests.get(self.url, headers=self.headers, params=task_params, proxies=self.proxy, timeout=5)
            if res.status_code == 200:
                json_data = res.json()
                return json_data
        except Exception as e:
            logger.error(e)

    def get_comment_total(self,params_data):
        json_data=self.get_detail_comments(params_data)
        return json_data['total']

    def get_user_commits(self,user_list):
        logger.info("成功获取作者id->{}".format(user_list))
        params= (
            ('aid', '1988'),
            ('app_language', 'ja-JP'),
            ('app_name', 'tiktok_web'),
            ('aweme_id', user_list),
            ('battery_info', '0.99'),
            ('browser_language', 'zh-CN'),
            ('browser_name', 'Mozilla'),
            ('browser_online', 'true'),
            ('browser_platform', 'Linux x86_64'),
            ('browser_version',
             '5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'),
            ('channel', 'tiktok_web'),
            ('cookie_enabled', 'true'),
            ('count', '30'),
            ('current_region', 'JP'),
            ('cursor', '0'),
            ('device_id', '7070368797244556801'),
            ('device_platform', 'web_pc'),
            ('focus_state', 'true'),
            ('fromWeb', '1'),
            ('from_page', 'video'),
            ('history_len', '5'),
            ('is_fullscreen', 'false'),
            ('is_page_visible', 'true'),
            ('os', 'linux'),
            ('priority_region', ''),
            ('referer', 'https://www.tiktok.com/@pasioncanella/video/{}'.format(user_list)),
            ('region', 'SG'),
            ('root_referer', 'https://www.tiktok.com/@pasioncanella/video/{}'.format(user_list)),
            ('screen_height', '1080'),
            ('screen_width', '1920'),
            ('tz_name', 'Asia/Shanghai'),
            ('verifyFp', 'verify_8619440063f37a4147ab04c70d884b41'),
            ('webcast_language', 'zh-Hant-TW'),
        )
        self.headers["referer"]="https://www.tiktok.com/@nelsontyc/video/{}?is_copy_url=1&is_from_webapp=v1&lang=zh-Hant-TW".format(user_list)
        totals=self.get_comment_total(params)
        params_list=list(params)
        logger.info("作者id:{}  发表评论总数为:{}".format(user_list,totals))
        task_list=self.get_comments_list(totals,params_list,30)
        print(task_list)
        if not task_list:
            time.sleep(3)
        with ThreadPoolExecutor(100)  as executor:
            executor.map(self.get_detail_comments,task_list)

    def download_json(self,json_data):
        with open("user_info.json","a",encoding="utf-8")  as fp:
            fp.write(json.dumps(json_data)+'\n')

    def main(self):
        # temp=self.read_json()
        # tasks=self.get_user_id(temp)
        tasks=[7058186727248235782]
        if not tasks:
            time.sleep(3)
        with ThreadPoolExecutor(400) as executor:
            executor.map(self.get_user_commits,tasks)
        logger.info("此四百个任务已经完成，进行下一个任务轮次")

if __name__=="__main__":
    run=Spider_titk()
    start=time.time()
    run.main()
    logger.info("总共用时:------->{}".format(time.time()-start))