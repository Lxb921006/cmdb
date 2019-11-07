#!/usr/bin/env python3
# coding:utf-8

from django.utils.safestring import mark_safe
from cmdbs.models import record_log
from cmdbs.models import Servers
from cmdbs.models import Item
from cmdbs.models import good_bad_count
import datetime
import matplotlib.pyplot as plt
import random
import redis
import json
import os
import configparser
import sys
import requests
import datetime
import winrm
import functools


def Opratings_log(user, desc, date):  # 这里是用户的操作记录方法
    try:
        add_r = record_log(
            login_user=user,
            operation_record=desc,
            date=date,
        )
        add_r.save()
    except:
        return -1


def get_machine_data():  # 从redis获取机器的状态数据
    ips = Servers.objects.filter().all()
    for connect_ip in ips:
        if connect_ip.ip == '192.168.171.142' or connect_ip.ip == '192.168.171.143':
            try:
                r = redis.Redis(host=connect_ip.ip, password='123', port=6379, db=5)
            except (redis.exceptions.ConnectionError, redis.exceptions.AuthenticationError):
                return
            if len(r.keys()) != 0:
                item = r.keys()[0]
                if len(r.brpop(item, 0)) != 0:
                    machine = json.loads(r.brpop(item, 0)[-1])
                    machine_status_show(item, machine)


def machine_status_show(ip, machine):  # 可视化展示机器状态
    if not isinstance(machine, dict):
        return
    all_colors = list(plt.cm.colors.cnames.keys())
    random.seed(100)
    c = random.choices(all_colors, k=len(machine))
    save_path = os.path.join(r'E:\mysite\mysite\static\img\machine', ip.decode()+'.png')

    # Plot Bars
    plt.figure(figsize=(10, 6), dpi=80)
    plt.bar([k for k, v in machine.items()],
            [v for k, v in machine.items()],
            color=c,
            width=.5)
    for i, val in machine.items():
        plt.text(i, val, float(val),
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 fontdict={'fontweight': 500, 'size': 13}, )

    # Decoration
    plt.gca().set_xticklabels([k for k, v in machine.items()],
                              rotation=60,
                              horizontalalignment='right',
                              fontdict={'fontsize': 12})
    plt.title(ip.decode(), fontsize=15)
    plt.ylabel('percent', fontsize=12)
    plt.ylim(0, 100)
    plt.savefig(save_path)
    # plt.show()


def push_package(project, ipaname):
    item_package = {
        "ddz": r"D:\wwwroot\www.4gqp.net\Static\game\Resources\ddz",
        "fish": r"D:\wwwroot\fish.4gqp.com\Static\game\Resources\fish",
        "dzdh": r"D:\wwwroot\www.4gqp.com\Static\game\Resources\dn",
        "kxddz": r"D:\wwwroot\www.4gqp.cn\Static\game\Resources\phdh",
        "mhby": r"D:\wwwroot\mh-fish.4gqp.com\Static\game\Resources\fish",
        "kbby": r"D:\wwwroot\kbby.4gqp.com\Static\game\Resources\fish"
    }
    ftp_dir = r'D:\wwwroot\ftpdir'
    backup_path = r'D:\wwwroot\ipa_backup\{}'.format(ipaname.split('.ipa')[0])
    res = get_servers_info('web-push', 'web-push-machines')
    ip = res.split()[0]
    user = res.split()[1]
    password = res.split()[2]
    cmd_bak = "copy {} {} /y".format(item_package[project] + os.sep + ipaname, backup_path)
    real_filename = ftp_dir + os.sep + ipaname
    tran_filename = "/cygdrive/d" + (item_package[project] + os.sep + ipaname).replace('D:', '').replace('\\', '/')
    cmd_copy = "copy {} {} /y".format(real_filename, item_package[project])
    cmd_run = r'cd C:\Program Files (x86)\ICW\bin  & rsync.exe -av {} rsync://192.168.3.7/test'.format(tran_filename)
    all_cmd = cmd_bak + ' & ' + cmd_copy + ' & ' + cmd_run
    try:
        win = winrm.Session("http://{}:{}/wsman".format(ip, 5985), auth=(user, password))
    except requests.exceptions.ConnectionError:
        return -1
    else:
        res = win.run_cmd(all_cmd)
        return res


def running_cmd(cmd):
    all_cmd = {'synAccount': 'sudo bash /opt/synAccount.sh',
               'synLogin': 'bash /opt/synLogin.sh',
               'synStore': 'python /opt/progressbar.py',
               'synGuild': 'bash /opt/synGuild.sh',
               'synAll': '/usr/bin/python3 /root/down_img.py',
               }
    return all_cmd[cmd]


def get_servers_info(sec, opts):
    path = path = "{}/{}".format(os.getenv('IMP'), 'app.ini')
    config = configparser.ConfigParser()
    config.read(path)
    try:
        res = config.get(sec, opts)
    except KeyError:
        return -1
    return res



