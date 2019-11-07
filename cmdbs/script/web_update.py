#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/8/14 0014 10:41
# @Author  : lxb
# @FileName: web_update.py
# @Software: PyCharm
# @Desc    : 同步文件到外网(这里没必要(网络i/o)多线程，因为上传逻辑不复杂，这个脚本可能跑单线程都比多线程快，当然改成多线程也是好改)


import os
import re
import time
import logging
import configparser
import shutil
import datetime
import smtplib
import email.mime.text
import email.mime.multipart
import ftplib
import socket


class Syncfile(object):

    def connect_ftp(self, data):
        config = configparser.ConfigParser()
        config.read('/root/pyscript/ftpinfo.ini')  # 存放ftp账户信息文件
        ip_list = config.sections()
        if data in ip_list:
            ip, user, passwed, port = config.get(data, data).split()
            ftp = ftplib.FTP()
            ftp.encoding = 'utf-8'
            try:
                ftp.connect(ip, int(port), timeout=10)
                ftp.login(user, passwed)
            except (socket.timeout, ftplib.error_perm) as err:
                logging.error('%s not connect ftp---->%s' % (ip, err))
                content = '%s not connect ftp---->%s' % (ip, err)
                self._sendmail(content)
                raise ConnectionError(content)  # 这里连接不上ftp就直接退出
            else:
                return ftp
        else:
            logging.error('it is not exists this ftp account %s' % data)  # 没有拿到机器信息
            content = 'it is not exists this ftp account %s' % data
            self._sendmail(content)
            raise ValueError(content)  # 这里如果没有找到ftp账户信息也是直接退出

    def upload(self, ftpinfo, data):
        web_dir = '/web/wwwroot/'  # web目录
        ignore_file = ['/Apps/Common/Conf/config.php',
                       '/Apps/Cms/Org/Gamesync.class.php',
                       '/Apps/Admin/Conf/config.php',
                       ]  # 存放禁止更新的文件
        for item in open(data, encoding='utf-8'):  # 读取文件里边更新内容
            flag = True
            ftp = self.connect_ftp(ftpinfo)
            os.chdir(web_dir)
            if item == "\n":  # 忽略空行
                continue
            format_item = item.strip().replace('\\', '/')
            file_path = os.path.dirname(format_item)
            file_name = os.path.basename(format_item)
            if not os.path.exists(format_item):  # 忽略不存在的文件或者目录
                logging.error('%s--->not exists' % format_item)
                content = '%s--->not exists' % format_item
                self._sendmail(content)
                continue
            for ignore in ignore_file:  # 忽略禁止更新的文件
                if re.findall(ignore, format_item).__len__() != 0:
                    logging.error('%s--->Prohibit updates.' % format_item)
                    flag = False
            if flag is False:
                continue
            if format_item.split('/').__len__() <= 3 and format_item.split('/')[0] != 'shell':  # 忽略目录层级小于等于3的更新内容
                logging.error('%s--->Directory level is wrong.' % format_item)
                continue

            if os.path.isdir(format_item):  # 这里是更新目录
                for root, dirs, file in os.walk(format_item):
                    for filename in file:
                        u_file = os.path.join(root, filename)
                        u_file_path = os.path.dirname(u_file)
                        u_file_name = os.path.basename(u_file)
                        flag = True
                        for ftpdir in u_file_path.split('/'):  # 这里因为不支持在ftp上联级创建目录，所以只能是一个个创建目录
                            if flag:                           # 如：ftp.mkd('/a/b/c/d')这个是不支持的，只能是创建完一个再进行下一个，所以用for循环
                                try:
                                    ftp.cwd("/" + str(ftpdir))
                                except ftplib.error_perm:
                                    ftp.mkd("/" + str(ftpdir))
                                    ftp.cwd("/" + str(ftpdir))
                                flag = False
                            else:
                                try:
                                    ftp.cwd(str(ftpdir))
                                except ftplib.error_perm:
                                    ftp.mkd(str(ftpdir))
                                    ftp.cwd(str(ftpdir))

                        try:
                            ftp.storbinary('STOR ' + u_file_name, open(u_file, 'rb'))  # 上传
                            time.sleep(0.5)
                        except ftplib.error_perm as err:
                            logging.error('%s--->upload error msg:%s' % (u_file, err))
                            content = '%s update failed, error msg:%s' % (u_file, err)
                            self._sendmail(content)
                        else:
                            logging.info("%s" % u_file)
            else:  # 这里是更新文件
                flag = True
                for ftpdir in file_path.split('/'):
                    if flag:
                        try:
                            ftp.cwd("/" + str(ftpdir))
                        except ftplib.error_perm:
                            ftp.mkd("/" + str(ftpdir))
                            ftp.cwd("/" + str(ftpdir))
                        flag = False
                    else:
                        try:
                            ftp.cwd(str(ftpdir))
                        except ftplib.error_perm:
                            ftp.mkd(str(ftpdir))
                            ftp.cwd(str(ftpdir))

                try:
                    ftp.storbinary('STOR ' + file_name, open(format_item, 'rb'))
                    time.sleep(0.5)
                except (ftplib.error_perm, OSError) as err:
                    logging.error('%s--->upload error msg:%s' % (format_item, err))
                    content = '%s update failed, error msg:%s' % (format_item, err)
                    self._sendmail(content)
                else:
                    logging.info("%s" % format_item)
            ftp.close()

    @staticmethod
    def _sendmail(data):  # 邮件报警
        server = None
        recv = ['120332269@qq.com', '15889809122@163.com']
        msg = email.mime.multipart.MIMEMultipart()
        subject = "Web update files failed massage."
        content = str(data)
        msg["From"] = '1354198737@qq.com'
        msg["To"] = ",".join(recv)
        msg["Subject"] = subject
        text = email.mime.text.MIMEText(content)
        msg.attach(text)
        try:
            server = smtplib.SMTP_SSL('smtp.qq.com')
            server.login('1354198737@qq.com', 'kfcznkkspsvrhdef')
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        except Exception as err:
            logging.error('send mail fail------->%s' % err)
        finally:
            server.quit()


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        filename='/root/pyscript/web_update.log',  # 更新日志记录
                        filemode='a')
    update_dir = '/web/wwwroot/update'  # ftp目录
    update_record = '/root/pyscript/update_record/'  # 更新文件存放路径
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    ftp_instance = Syncfile()  # 实例化类Syncfile
    for root, dirs, file in os.walk(update_dir):  # 这里是循环获取每个指定目录下的文件
        for dirname in dirs:
            paths = os.path.join(root, dirname)
            for files in os.listdir(paths):
                u_file = os.path.join(paths, files)
                if os.path.isfile(u_file):
                    ftp_instance.upload(dirname, u_file)  # 调用实例方法(ftp上传)，下载就没写了
                    shutil.move(u_file, update_record + dirname + '_' + date)  # 保存更新记录文件到指定目录


if __name__ == '__main__':
    main()
