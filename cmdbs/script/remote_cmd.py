#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/5/21 0021 11:34
# @Author  : lxb
# @FileName: remote_cmd.py
# @Software: PyCharm
# @Desc    : 远程操作模板脚本

import paramiko
import time
import configparser
import threading
import argparse
import queue
import winrm
import subprocess


class Remote(threading.Thread):
    def __init__(self, t_queue):
        self.t_queue = t_queue
        super().__init__()

    def run(self):
        while not self.t_queue.empty():
            data = self.t_queue.get()
            self.check_os(data)
            time.sleep(0.5)

    def check_os(self, data):
        ip_info, command, = data
        if command['os'] == 'win_shell':
            self.win_os(data)
        elif command['os'] == 'linux_shell':
            self.linux_os(data)
        else:
            raise ValueError('choose [win_shell\linux_shell]')

    def win_os(self, data):
        ip_info, command = data
        flag_w = True
        if command['cmd']:
            try:
                win = winrm.Session("http://"+ip_info.split()[0]+":"+ip_info.split()[2]+"/wsman",
                                    auth=(ip_info.split()[1], ip_info.split()[3]))
                res = win.run_cmd(command['cmd'])
            except Exception as err:
                flag_w = False
                print("%s have error msg:%s in %s rows" % (ip_info.split()[0], err, err.__traceback__.tb_lineno))
            if flag_w:
                print("############%s finished############" % ip_info.split()[0])
                if not res.std_err:
                    print(res.std_out.decode('ansi').strip())
                else:
                    print("%s Running windows cmd fail--->%s" % (ip_info.split()[0], res.std_err.std_out.decode('ansi')))
        if command['action'] == 'put':
            res = subprocess.getstatusoutput("rsync -av {} rsync://{}:20791/{}".format(command['sourcefile'],
                                                                                       ip_info.split()[0],
                                                                                       command['targetfile']))
            print(res)
            if res[0] == 0:
                print("%s upload finished." % ip_info.split()[0])
            else:
                print("%s upload fail." % ip_info.split()[0])

        if command['action'] == 'get':
            res = subprocess.getstatusoutput("rsync -av rsync://{}:20791/{} {}".format(
                                                                          ip_info.split()[0],
                                                                          command['sourcefile'],
                                                                          command['targetfile']+"_"+ip_info.split()[0]))
            if res[0] == 0:
                print("%s download finished." % ip_info.split()[0])
            else:
                print("%s download fail." % ip_info.split()[0])

    def linux_os(self, data):
        ip_info, command = data
        flag_l = True
        try:
            if len(ip_info) >= 5:
                client = paramiko.Transport((ip_info.split()[0], int(ip_info.split()[2])))
                client.connect(username=ip_info.split()[1], password=ip_info.split()[3])
                ssh = paramiko.SSHClient()
                ssh._transport = client
                sftp = paramiko.SFTPClient.from_transport(client)
            else:
                p_key = paramiko.RSAKey.from_private_key_file(ip_info.split()[3])
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_info.split()[0], username=ip_info.split()[1], port=ip_info.split()[2], pkey=p_key, timeout=6)
                trn = ssh.get_transport()
                sftp = paramiko.SFTPClient.from_transport(trn)
        except Exception as err:
            flag_l = False
            print("%s have error msg:%s in %s rows" % (ip_info.split()[0], err, err.__traceback__.tb_lineno))
        if flag_l:
            method = {
                'put': sftp.put,
                'down': sftp.get,
                'cmd': ssh.exec_command
            }
            if command['action'] == 'put':
                try:
                    method['put'](command['sourcefile'], command['targetfile'])
                except IOError as err:
                    print('%s--->upload %s fail,error msg--->%s' % (ip_info.split()[0], command['sourcefile'], err))
                else:
                    print("%s--->upload %s finished." % (ip_info.split()[0], command['sourcefile']))
            if command['action'] == 'get':
                try:
                    method['down'](command['sourcefile'], command['targetfile']+"_"+ip_info.split()[0])
                except IOError as err:
                    print('%s--->download %s fail,error msg--->%s' % (ip_info.split()[0], command['sourcefile'], err))
                else:
                    print("%s--->download %s finished." % (ip_info.split()[0], command['sourcefile']))
            if command['cmd']:
                stdin, stdout, stderr = method['cmd'](command['cmd'], timeout=6)
                if not stderr.read():
                    for res in stdout:
                        print(res.strip())
                    print("############%s finished############" % ip_info.split()[0])
                else:
                    print('Invalid command--->%s' % command['cmd'])
            ssh.close()


def main():
    info = dict()
    threads_num = 5
    queue_ = queue.Queue()
    config = configparser.ConfigParser()
    config.read(r'C:\Users\Administrator\Desktop\test.ini')
    parser = argparse.ArgumentParser(description="this is helpful info.")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("item_section", help="please input the sections like [nginx/web..] and so on.")
    parser.add_argument("-S", "--system", help="please input system like [win_shell/linux_shell]", required=True)
    parser.add_argument("-I", "--item", nargs='*', help="please choose type such as [nginx-1/web-1/all].",
                        required=True)
    group.add_argument("-C", "--cmd", help="remote cmd.")
    group.add_argument("-A", "--action", nargs=3, help="put/get sourcefile targetfile.")
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
                queue_.put((config.get(args.item_section, all_ip), info))
        else:
            for ip in args.item:
                if ip in config.options(args.item_section):
                    queue_.put((config.get(args.item_section, ip), info))
                else:
                    print('not exist this machine--->%s,please check the help info' % ip)
    else:
        sec_error_msg = 'not exist this item--->%s,please check the help info' % args.item_section
        raise SystemExit(sec_error_msg)
    [Remote(queue_).start() for _ in range(threads_num)]


if __name__ == '__main__':
    main()
