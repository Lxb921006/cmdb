#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/7/25 0025 16:40
# @Author  : lxb
# @FileName: view_map.py
# @Software: PyCharm
# @Desc    : The role of the script

import matplotlib.pyplot as plt
import random


machine_status = {'cpu': 30,
                  'memory': 40,
                  'disk': 80
                  }
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=len(machine_status))

# Plot Bars
plt.figure(figsize=(16, 10), dpi=80)
plt.bar([k for k, v in machine_status.items()],
        [v for k, v in machine_status.items()],
        color=c,
        width=.5)
for i, val in machine_status.items():
    plt.text(i, val, float(val),
             horizontalalignment='center',
             verticalalignment='bottom',
             fontdict={'fontweight': 500, 'size': 12},)

# Decoration
plt.gca().set_xticklabels([k for k, v in machine_status.items()],
                          rotation=60,
                          horizontalalignment='right',
                          fontdict={'fontsize': 15})
plt.title("192.168.171.247", fontsize=22)
plt.ylabel('percent', fontsize=15)
plt.ylim(0, 100)
plt.savefig('192.168.171.247.png')
plt.show()