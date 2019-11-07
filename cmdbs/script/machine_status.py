#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/7/25 0025 13:35
# @Author  : lxb
# @FileName: machine_status.py
# @Software: PyCharm
# @Desc    : 获取机器状态数据,图形化展示(只适用linux)

import redis
import json
import socket
import psutil


class Machines(object):

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.auth = 123
        self.port = 6379
        self.db = 5

    def cpu_rate(self):
        cpu_usage_rate = psutil.cpu_percent()
        return cpu_usage_rate

    def memory_rate(self):
        memory_usage_rate = psutil.virtual_memory().percent
        return memory_usage_rate

    def disk_rate(self):
        disk_list = [
            (all_disk.device, psutil.disk_usage(all_disk.mountpoint).percent) for all_disk in psutil.disk_partitions()
        ]
        return disk_list

    def save_to_redis(self):
        disk_all = self.disk_rate()
        machine_status = {'cpu': self.cpu_rate(),
                          'memory': self.memory_rate(),
                          }
        if len(disk_all) > 1:
            for item in disk_all:
                machine_status['disk'+'_'+item[0]] = item[1]
        else:
            machine_status = {'cpu': self.cpu_rate(),
                              'memory': self.memory_rate(),
                              'disk': self.disk_rate()
                              }
        json_data = json.dumps(machine_status)
        try:
            redis_object = redis.Redis(host=self.host, password=self.auth, port=self.port, db=self.db)
        except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError):
            return
        redis_object.lpush(self.host, json_data)


if __name__ == '__main__':
    run = Machines()
    run.save_to_redis()
