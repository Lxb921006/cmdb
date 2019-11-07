#!/usr/bin/env python3
# coding:       utf-8
# Name:         test_yeild
# Date:         2019/8/3
# Author:       xuanbiao
# Description:  

import re

a = [r'C:\Users\xuanbiao\Desktop\cdn.confbak', r'C:\Users\xuanbiao\Desktop\cdn.conf']
t = r'C:\Users\xuanbiao\Desktop\cdn-tttt.conf'

content = ''
d = list()

for i in a:
    for t in open(i, encoding='utf-8'):
        if re.findall('server_name.*', t.strip()):
            g = re.split('server_name|;|[ \t]', t.strip())
            d.append(" ".join(g).strip())
            print(" ".join(g))

for h in a:
    open(h, 'w', encoding='utf-8').write(re.sub('[ \t]server_name.*', '[ \t]server_name ' + " ".join(d),
                                                open(t, encoding='utf-8').read()))
