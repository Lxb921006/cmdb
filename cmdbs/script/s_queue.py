#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/5/21 0021 11:34
# @Author  : lxb
# @FileName: remote_cmd.py
# @Software: PyCharm
# @Desc    : 远程操作模板脚本

import paramiko
import time
import socket
import sys
import configparser
import threading
import argparse
import queue
import winrm
import random
import subprocess


class Remote(threading.Thread):
    def __init__(self, t_queue):
        self.t_queue = t_queue
        super().__init__()

    def run(self):
        while 1:
            data = self.t_queue.get()  # 获取队列里边的数据
            self.check_os(data)
            if self.t_queue.task_done():  # 完成了队里的任务告诉join可以结束阻塞
                break
            time.sleep(random.randrange(2, 5))

    def check_os(self, data):  # 判断操作系统给对应的方法执行任务
        ip_info, command, item_name = data
        if command['os'] == 'win':
            self.win_os(data)
        elif command['os'] == 'lin':
            self.linux_os(data)
        else:
            raise ValueError("choose [win\\lin]")

    def win_os(self, data):  # 这里是windows系统的远程操作跟上传下载文件(windows需安装rsync)
        ip_info, command, item_name = data
        flag_w = True
        if command['cmd']:
            try:
                win = winrm.Session("http://"+ip_info[0]+":"+ip_info[2]+"/wsman",
                                    auth=(ip_info[1], ip_info[3]))
                res = win.run_cmd(command['cmd'])  # 这里是远程执行cmd
            except Exception as err:
                flag_w = False
                sys.stdout.write("%s have error msg:%s in %s rows\n" % (ip_info[0], err, err.__traceback__.tb_lineno))
            if flag_w:
                sys.stdout.write("############%s-%s finished############\n" % (item_name, ip_info[0]))
                if not res.std_err:
                    sys.stdout.write(res.std_out.decode('ansi').strip() + '\n')
                else:
                    sys.stdout.write("%s-%s Running windows cmd fail--->%s\n" % (item_name, ip_info[0], res.std_err.std_out.decode('ansi')))
        if command['action'] == 'put':  # 这里是上传文件
            res = subprocess.getstatusoutput("rsync -av {} rsync://{}:20791/{}".format(command['sourcefile'],
                                                                                       ip_info[0],
                                                                                       command['targetfile']))
            sys.stdout.write(str(res) + '\n')
            if res[0] == 0:
                sys.stdout.write("%s-%s upload finished.\n" % (item_name, ip_info[0]))
            else:
                sys.stdout.write("%s-%s upload fail.\n" % (item_name, ip_info[0]))

        if command['action'] == 'get':  # 这里是下载文件
            res = subprocess.getstatusoutput("rsync -av rsync://{}:20791/{} {}".format(
                                                                          ip_info[0],
                                                                          command['sourcefile'],
                                                                          command['targetfile']+"_"+ip_info[0]))
            if res[0] == 0:
                sys.stdout.write("%s-%s download finished.\n" % (item_name, ip_info[0]))
            else:
                sys.stdout.write("%s-%s download fail.\n" % (item_name, ip_info[0]))

    def linux_os(self, data):  # 这里是linux的操作
        ip_info, command, item_name = data
        flag_l = True
        try:
            if len(ip_info) >= 5:  # 使用key登录
                client = paramiko.Transport((ip_info[0], int(ip_info[2])))
                client.connect(username=ip_info[1], password=ip_info[3])
                ssh = paramiko.SSHClient()
                ssh._transport = client
                sftp = paramiko.SFTPClient.from_transport(client)
            else:  # 使用密码登录
                p_key = paramiko.RSAKey.from_private_key_file(ip_info[3])
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_info[0], username=ip_info[1], port=ip_info[2], pkey=p_key, timeout=6)
                trn = ssh.get_transport()
                sftp = paramiko.SFTPClient.from_transport(trn)
        except Exception as err:
            flag_l = False
            sys.stdout.write("%s-%s have error msg:%s in %s rows\n" % (item_name, ip_info[0], err, err.__traceback__.tb_lineno))
        if flag_l:
            # 这里是ftp,ssh方法的映射
            method = {
                'put': sftp.put,
                'down': sftp.get,
                'cmd': ssh.exec_command
            }
            if command['action'] == 'put':  # 这里是上传
                try:
                    method['put'](command['sourcefile'], command['targetfile'])
                except IOError as err:
                    sys.stdout.write('%s-%s--->upload %s fail,error msg--->%s\n' % (item_name, ip_info[0], command['sourcefile'], err))
                else:
                    sys.stdout.write("%s-%s--->upload %s finished.\n" % (item_name, ip_info[0], command['sourcefile']))
            if command['action'] == 'get':  # 这里是下载
                try:
                    method['down'](command['sourcefile'], command['targetfile']+"_"+ip_info[0])
                except IOError as err:
                    sys.stdout.write('%s-%s--->download %s fail,error msg--->%s\n' % (item_name, ip_info[0], command['sourcefile'], err))
                else:
                    sys.stdout.write("%s-%s--->download %s finished.\n" % (item_name, ip_info[0], command['sourcefile']))
            if command['cmd']:  # 这里是执行远程执行cmd
                try:
                    stdin, stdout, stderr = method['cmd'](command['cmd'], timeout=10)
                except socket.timeout:
                    sys.stdout.write("%s-%s running cmd timeout.\n" % (item_name, ip_info[0]))
                else:
                    err = stderr.read().strip()
                    if err:
                        sys.stdout.write(err + '\n')
                    else:
                        for res in stdout:
                            sys.stdout.write(res.strip() + '\n')
                    sys.stdout.write("############%s-%s finished############\n" % (item_name, ip_info[0]))
            ssh.close()


def main():
    info = dict()
    threads_num = 5
    queue_ = queue.Queue()
    config = configparser.ConfigParser()
    config.read('/root/pyscript/machines.ini')  # 机器账户信息的存放文件，这个千万别泄露喽
    parser = argparse.ArgumentParser(description="this is helpful info.")  # 下面是执行这个脚本要加的参数（都是必须参数）
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("item_section", help="please input the sections like [all-nginx/all-web..] and so on.")  # 这个是父节点
    parser.add_argument("-S", "--system", help="please input system like [win/lin]", required=True)  # 这个是操作系统的选择
    parser.add_argument("-I", "--item", nargs='*', help="please choose type such as [nginx-1/web-1/all].",
                        required=True)  # 这个子节点的选择
    group.add_argument("-C", "--cmd", help="remote cmd.")  # 执行cmd
    group.add_argument("-A", "--action", nargs=3, help="put/get sourcefile targetfile.")  # 上传下载
    args = parser.parse_args()
    if args.action is None and args.cmd is None:
        error_msg = 'please input Operational order.'
        raise SystemExit(error_msg)
    if args.action is None and args.cmd is not None:
        info = {
            'action': None,
            'sourcefile': None,
            'targetfile': None,
            'cmd': args.cmd,
            'os': args.system
        }
    if args.action is not None and args.cmd is None:
        info = {
            'action': args.action[0],
            'sourcefile': args.action[1],
            'targetfile': args.action[2],
            'cmd': None,
            'os': args.system
        }
    if args.item_section in config.sections():
        if len(args.item) == 1 and args.item[0] == 'all':
            for all_ip in config.options(args.item_section):
                queue_.put((config.get(args.item_section, all_ip).split(), info, all_ip))
        else:
            if args.item:
                for ip in args.item:
                    if ip in config.options(args.item_section):
                        queue_.put((config.get(args.item_section, ip).split(), info, ip))  # 把机器信息放到队列里边
                    else:
                        sys.stdout.write('not exist this machine--->%s,please check the help info\n' % ip)
            else:
                raise SystemExit('miss item,please check --help.')
    else:
        sec_error_msg = 'not exist this item--->%s,please check the help info' % args.item_section
        raise SystemExit(sec_error_msg)

    for _ in range(threads_num):
        t = Remote(queue_)
        t.daemon = True  # 设置子线程为守护线程，目的是所有队里中的任务执行完就退出。
        t.start()  #
    queue_.join()  # （阻塞）等待队里的任务都执行完才结束主进程

# 脚本用法介绍：python3 remote_cmd.py --help 执行这条命令可以看到帮助信息
# 示例：
# python3 remote_cmd.py all-web -S lin -I all -C "free -m" 这个是返回all-web这个节点下面所有服务器的内存信息-C后面放cmd(有些cmd要接绝对路径)
# python3 remote_cmd.py all-web -S lin -I all -A put /opt/aaa.txt /opt/aaa.txt 这个是传送/opt/aaa.txt文件到all-web这个节点下面的所有服务器
# python3 remote_cmd.py all-web -S lin -I all -A get /opt/aaa.txt /opt/aaa.txt 这个是下载all-web这个节点下面的所有服务器/opt/aaa.txt文件到本地
# python3 remote_cmd.py all-web -S lin -I web-1,web-2 指定子节点


if __name__ == '__main__':
    main()

