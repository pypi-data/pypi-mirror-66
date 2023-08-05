# auto generated by update_py.py

import datetime
import json
import redis
import requests
import threading
import time

from collections import defaultdict

from tlclient.linker.constant import FistType
from tlclient.linker.fist import Fist


class NotificationClient:

    def __init__(self, logger):
        self.logger = logger

    def send(self, content):
        pass

    def send_status(self, is_running=True):
        pass

    def close(self):
        self.send_status(False)


class WxworkClient(NotificationClient):

    def __init__(self, webhook_url, logger):
        NotificationClient.__init__(self, logger)
        self.webhook_url = webhook_url

        self.level_2_color = {
            'info': 'info',
            'warning': 'warning',
            'error': 'red',
        }

        self.send_status()

    def parse_level(self, message):
        level = 'info'
        if 'exited' in message or 'error' in message:
            level = 'error'
        elif 'disconnected' in message:
            level = 'warning'
        return level

    def convert_to_content(self, data):
        contents = ''
        for title, title_value in data.items():
            for message, message_value in title_value.items():
                level = self.parse_level(message)
                level_content = '**<font color="{}">{}</font>**'.format(self.level_2_color[level], level.upper())
                if len(message_value) == 1:
                    message_content = message
                    time_content = message_value[0].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    max_time_content = max(message_value).strftime('%Y-%m-%d %H:%M:%S')
                    min_time_content = min(message_value).strftime('%Y-%m-%d %H:%M:%S')

                    message_content = message + '({}次)'.format(len(message_value))
                    time_content = '{} ~ {}'.format(min_time_content, max_time_content)

                content = f'{level_content}\n' +\
                          f'>来源: {title}\n' +\
                          f'>信息: **<font color="{self.level_2_color[level]}">{message_content}</font>**\n' +\
                          f'>时间: <font color="blue">{time_content}</font>\n'
                contents += content + '\n'
        return contents

    def send(self, content):
        message = {
            'msgtype': 'markdown',
            'markdown': {
                'content': self.convert_to_content(content)
            }
        }
        try:
            rsp = requests.post(self.webhook_url, json=message, timeout=3)

            data = json.loads(rsp.text)
            if data['errcode'] == 0:
                self.logger.debug('[Wxwork] sent successfully')
            elif data['errcode'] == 45009:
                self.logger.warning('[Wxwork] api freq out of limit (err_msg){}'.format(data['errmsg']))
            else:
                self.logger.error('[Wxwork] unknown rsp (rsp){}'.format(data))
        except Exception as e:
            self.logger.error('[Wxwork] exception (err_msg){}'.format(e))

    def send_status(self, is_running=True):
        status = 'start' if is_running else 'exited'
        content = {
            'notification': {
                f'notification {status}': [datetime.datetime.now()]
            }
        }
        self.send(content)

    def send_redis_status(self, err_msg, is_running=True):
        status = 'connected' if is_running else 'disconnected'
        content = {
            'notification': {
                f'redis {status} (err_msg){err_msg}': [datetime.datetime.now()]
            }
        }
        self.send(content)


class NotificationCenter(Fist):

    def __init__(self, name, env_name, addr, host='localhost', port=6379, password=None, key='notification'):
        Fist.__init__(self, name, FistType.BASE, env_name)
        self.set_master_addr(addr)
        self.create_fist()

        self.key = key
        self.clients = []
        self._redis = redis.StrictRedis(host, port, password=password, decode_responses=True, socket_timeout=3)

    def start(self):
        Fist.start(self)

        try:
            self.r_len = self._redis.llen(self.key)
            self.logger.info('[Notification] redis connected (init_size){}'.format(self.r_len))
            self.process_redis_status()
        except Exception as e:
            self.logger.error('[Notification] connect redis error. (err_msg){}'.format(e))
            self.process_redis_status(e, False)
            self.stop()

        new_thread = threading.Thread(target=self.notify_thread)
        new_thread.setDaemon(True)
        new_thread.start()

        self.connected = True

    def get_data_from_redis(self):
        redis_data = []

        try:
            redis_len = self._redis.llen(self.key)

            if not self.connected:
                self.connected = True
                self.process_redis_status()

            if redis_len > self.r_len:
                self.logger.info('[Notification] redis connected (prev_size){} (curr_size){}'.format(self.r_len, redis_len))
                redis_data = [json.loads(data) for data in self._redis.lrange(self.key, self.r_len, redis_len)]

            self.r_len = redis_len

        except Exception as e:
            self.logger.error('[Notification] redis disconnected. (err_msg){}'.format(e))
            if self.connected:
                self.connected = False
                self.process_redis_status(e, False)

        return redis_data

    def classify_data(self, redis_data):
        res = defaultdict(lambda: defaultdict(list))
        for data in redis_data:
            timestamp = datetime.datetime.strptime(data['timestamp'], '%Y%m%d-%H:%M:%S')
            res[data['title']][data['message']].append(timestamp)
        return res

    def notify_thread(self):
        while True:
            # redis_data: [{'message': 'market1 exited.', 'timestamp': '20191224-10:47:25', 'title': 'market1', 'type': 1}]
            redis_data = self.get_data_from_redis()
            # content: 'market1' -> 'market1 exited.' -> ['2019-12-24 10:47:25']
            if len(redis_data) > 0:
                content = self.classify_data(redis_data)
                if content:
                    self.process_content(content)
            time.sleep(3)

    def process_content(self, content):
        for client in self.clients:
            client.send(content)

    def process_redis_status(self, err_msg=None, is_running=True):
        for client in self.clients:
            client.send_redis_status(err_msg, is_running)

    def add_wxwork_client(self, webhook_url):
        wxwork_client = WxworkClient(webhook_url, self.logger)
        self.clients.append(wxwork_client)

    def on_close(self):
        self.logger.info("[Notification] close clients (fist_name){}".format(self.fist_name))
        self._redis.close()
        for client in self.clients:
            client.close()
        self.clients = []
