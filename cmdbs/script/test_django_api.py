#!/usr/bin/env python3
# coding:       utf-8
# Name:         test_django_api
# Date:         2019/10/11
# Author:       xuanbiao
# Description:  

import requests
import json
import base64

url = 'http://127.0.0.1:8000/cmdbs/api/'
key = 'f14c8391289294dff2b5de44dd6b9032'
name = 'lxb'
item = 'servers'
data = {
    'key': json.dumps(key).encode('utf-8'),
    'name': json.dumps(name).encode('utf-8'),
    'item': json.dumps(item).encode('utf-8'),
}

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3724.8 Safari/537.36'}

res = requests.get(url, headers=head, params=data)
print(res.text)

