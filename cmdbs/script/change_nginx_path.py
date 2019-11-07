#!/usr/bin/env python3
# coding   : utf-8
# @Time    : 2019/7/26 0026 15:03
# @Author  : lxb
# @FileName: change_nginx_path.py
# @Software: PyCharm
# @Desc    : change nginx path

import os
import re
import sys
import time
import shutil
import random
import platform


def change_nginx_status(nginx_path, replace_path, nginx_name, restore=None):
    if not os.path.isdir(nginx_path) and not os.path.isdir(replace_path):
        return -1
    else:
        os.chdir(nginx_path)

    if platform.system() == 'Windows':  # 操作系統判斷
        if not os.path.isfile(nginx_name):
            return -2
        if restore == 'back':  # 恢復
            shutil.copyfile(nginx_name + 'bak001', nginx_name)
        else:
            line_number = dict()
            check_content = list()
            domain_number = 1
            content = ''
            real_content = ''
            shutil.copyfile(nginx_name, nginx_name + 'bak001')
            sys.stdout.write('#########################Valid domain name###########################' + '\n')
            for w_content in enumerate(open(nginx_name + 'bak001', encoding='utf-8')):  # 展示选择需要维护的web
                if re.findall('^ServerName', w_content[1].strip()):
                    line_number[str(domain_number)] = w_content[1]
                    sys.stdout.write(str(domain_number)+')\t'+w_content[1].split()[-1]+'\n')
                    domain_number += 1
            sys.stdout.write(str(domain_number)+')\t'+'all'+'\n')
            sys.stdout.write('#####################################################################' + '\n')
            try:
                recv_data = input('Please enter the specified number({}-{}):'.format(1, domain_number))
            except KeyboardInterrupt:
                return
            if not recv_data or recv_data == 'exit':
                return

            if recv_data == str(domain_number):  # 替换指定域名web为维护状态
                open(nginx_name, 'w', encoding='utf-8').write(
                        re.sub('[ \t]ServerName.*', '[ \t]ServerName ' + 'repairing',
                               open(nginx_name + 'bak001', encoding='utf-8').read()
                               )
                        )
                for k, v in line_number.items():
                    templates = '''<VirtualHost *:80> 
                                    DocumentRoot D:\wwwroot\weihu
                                    ServerName   {}
                                    <Directory D:\wwwroot\weihu>
                                    RewriteEngine On
                                    RewriteRule ^(.*)  index_weihu.html
                                    </Directory>
                                   </VirtualHost>\n'''.format(v.split()[-1])
                    content += templates
                open(nginx_name, 'w', encoding='utf-8').write(content)
            else:
                for recv_number in re.split(' |,|-|\||_|~|;', recv_data):
                    if int(recv_number) not in [i for i in range(1, domain_number+1)]:
                        continue
                    check_content.append(line_number.get(recv_number, None).split()[-1])
                for item in open(nginx_name + 'bak001', encoding='utf-8'):
                    flag = True
                    for r_content in check_content:
                        if re.findall(r_content, item):
                            real_content += re.sub(r_content, 'repairing', item)
                            flag = False
                    if flag is False:
                        continue
                    real_content += item
                for adds in check_content:
                    templates = '''<VirtualHost *:80> 
                                    DocumentRoot D:\wwwroot\weihu
                                    ServerName   {}
                                    <Directory D:\wwwroot\weihu>
                                    RewriteEngine On
                                    RewriteRule ^(.*)  index_weihu.html
                                    </Directory>
                                   </VirtualHost>\n'''.format(adds)
                    real_content += templates
                open(nginx_name, 'w', encoding='utf-8').write(real_content)

        os.system('sc stop Apache2a')
        time.sleep(1)
        os.system('sc start Apache2a')
        sys.stdout.write('finished.\n')
        time.sleep(1)

    if platform.system() == 'Linux':
        if restore == 'back':
            for all_retore in os.listdir('/opt/bak'):
                restore_name = os.path.join('/opt/bak', all_retore)
                if re.findall('confbak001$', restore_name):
                    shutil.copyfile(restore_name, all_retore.split('bak001')[0])
        else:
            item_number = 1
            num_domain = dict()
            all_conf_file = list()
            sys.stdout.write('#########################Valid domain name###########################' + '\n')
            for nginxfile in os.listdir('.'):
                if re.findall('conf$', nginxfile) and os.path.isfile(nginxfile):
                    template_file = '/opt/bak/' + nginxfile + 'bak001'
                    shutil.copyfile(nginxfile, template_file)
                    domain = nginxfile.split('.conf')[0]
                    num_domain[item_number] = domain
                    all_conf_file.append(nginxfile)
                    sys.stdout.write(str(item_number) + ')\t' + domain + '\n')
                    item_number += 1
            sys.stdout.write(str(item_number) + ')\t' + 'all' + '\n')
            sys.stdout.write('#####################################################################' + '\n')
            try:
                recv_data = input('Please enter the specified number({}-{}):'.format(1, item_number))
            except KeyboardInterrupt:
                return
            if not recv_data or recv_data == 'exit':
                return

            bak_file = nginx_path + '/template.confc'
            if recv_data == str(item_number):
                for files in all_conf_file:
                    a = re.findall('[ \t]server_name.*', open(files, encoding='utf-8').read())
                    b = re.split('server_name|;| ', a[0])
                    d = [e for e in b if e != '']
                    f = " ".join(d)
                    open(files, 'w', encoding='utf-8').write(
                        re.sub('[ \t]server_name.*', '\tserver_name ' + " " + f + ';',
                               open(bak_file, encoding='utf-8').read())
                        )
            else:
                for recv_number in re.split(' |,|-|\||_|~|;', recv_data):
                    if int(recv_number) not in [i for i in range(1, item_number+1)]:
                        continue
                    select_domain = num_domain.get(int(recv_number), None)
                    replace_file = select_domain+'.conf'
                    a = re.findall('[ \t]server_name.*', open(replace_file, encoding='utf-8').read())
                    b = re.split('server_name|;| ', a[0])
                    d = [e for e in b if e != '']
                    f = " ".join(d)
                    open(replace_file, 'w', encoding='utf-8').write(
                        re.sub('[ \t]server_name.*', '\tserver_name ' + f + ';',
                               open(bak_file, encoding='utf-8').read())
                    )
        time.sleep(random.randrange(5, 8))
        os.system(
            "python3 /root/pyscript/remote_cmd.py all-web -S lin -I all -C \"/usr/local/nginx/sbin/nginx -s reload\""
        )
        sys.stdout.write('finished.\n')


if __name__ == '__main__':
    if len(sys.argv[1:]) == 3:
        change_nginx_status(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv[1:]) == 4:
        change_nginx_status(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(
            'usage:nginx path, replace path, choose[nginx filename for windows|random for linux], back means restore.'
        )




