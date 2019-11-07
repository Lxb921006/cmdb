#!/usr/bin/env python3
# coding:       utf-8
# Name:         out_put
# Date:         2019/8/25
# Author:       xuanbiao
# Description:  

import subprocess
import shlex

cmd = r'F:\env_mysit\Scripts\dist\test_input.exe'

process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
while 1:
    process = process.stdout.readline().strip()
    if not process:
        break
    print(process)

