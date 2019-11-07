#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/8/14 0014 17:37
# @Author  : lxb
# @FileName: ftp_test.py
# @Software: PyCharm
# @Desc    : The role of the script

import ftplib

ftp = ftplib.FTP()
ftp.connect('192.168.171.143')
ftp.login('www', '123321')

dirs = 'shell/a'

try:
    ftp.cwd("/" + str(dirs))
except ftplib.error_perm:
    print('1111')


