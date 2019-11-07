# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbs', '0003_auto_20190917_2204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfos',
            options={'permissions': (('view_machine', '机器管理'), ('view_platform', '平台管理'), ('view_Permission', '权限管理'), ('view_log', '日志查看'), ('view_operation_log', '操作日志'), ('view_web_log', 'web日志'), ('view_machine_list', '主机列表'), ('view_platform_update', '停机维护'), ('view_version_hotfix', '版本热更'), ('view_iframe_info', '查看基础页面'), ('view_cache', '缓存管理'), ('view_User_Management', '用户管理'), ('cmdb_machine_manage', '机器管理01'), ('cmdb_machine_operating', '机器操作01'), ('cmdb_machine_status', '机器状态01'), ('cmdb_platform_manage', '平台管理01'), ('cmdb_platform_operating', '平台操作01'), ('cmdb_platform_update', '前台更新01'), ('cmdb_log_manage', '日志管理01'), ('cmdb_log_web', 'web日志01'), ('cmdb_log_operating', '操作日志01'), ('cmdb_user_manage', '用户管理01'), ('cmdb_user_operating', '用户操作01'), ('cmdb_permission_set', '权限设置01'), ('cmdb_cache_clear', '缓存清除01'), ('cmdb_cache_clear02', '缓存清除02'), ('cmdb_api', '平台api01'), ('cmdb_api02', '平台api02'))},
        ),
    ]
