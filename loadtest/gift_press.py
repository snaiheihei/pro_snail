# -*- coding: utf-8 -*-
# The HttpLocust class has been renamed to HttpUser in version 1.0.
from locust import HttpUser, TaskSet, task
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GiftPress(TaskSet):

    def on_start(self):
        # this function is very very useful to transport args from file when a close class
        with open('data.txt', 'r') as f:
            data = f.read()
        self.room_id = data.split(' ')[0]
        self.uid = data.split(' ')[1]
        self.gid = data.split(' ')[2]
        self.gift_name = data.split(' ')[3]
        # self.gift_url = data.split(' ')[4]
        # print(self.room_id, self.uid, self.gid)
    def on_stop(self):
        pass

    @task()
    def send_gift(self):
        url = 'http://tc.service.tieba.baidu.com/service/ala?'
        param1 = {
                'charm_count': '',
                'charm_value': 0,
                'gift_count': 1,
                'gift_id': self.gid,
                'gift_name': self.gift_name,
                'gift_url': 'https://ala-gift.cdn.bcebos.com/gift/2020-10/1603449637587/240x240.png',
                'is_boom': 0,
                'is_free': 0,
                'order_id': '8000302152389338517063725281597894562',
                'scene_id': 8000302,
            }
        param = json.dumps(param1,ensure_ascii=False)
        data = {
            'method': 'sendServiceInfoEx',
            'room_id': self.room_id,
            'user_id': self.uid,
            'msg_type': 24,
            'content': param,
            'ie': 'utf-8',
            'format': 'json'
        }
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        # res = self.client.get(url, params=data, headers=header)
        # print(res.json())

class User(HttpUser):
    # weight default set 1 ,if only one thread user
    # weight = 4
    # task_set = GiftPress
    tasks = [GiftPress]
    min_wait = 3000
    max_wait = 6000


