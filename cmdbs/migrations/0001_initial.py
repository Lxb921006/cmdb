# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='good_bad_count',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('good_count', models.IntegerField()),
                ('bad_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Groupinfos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('groupname', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'groupinfos',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('project', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=100)),
                ('servers_count', models.IntegerField()),
            ],
            options={
                'ordering': ['project'],
            },
        ),
        migrations.CreateModel(
            name='record_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('login_user', models.CharField(max_length=20)),
                ('operation_record', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('project', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=20)),
                ('ram', models.IntegerField()),
                ('hard_disk', models.IntegerField()),
                ('cpu', models.IntegerField()),
                ('os', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['project'],
            },
        ),
        migrations.CreateModel(
            name='Userinfos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('user', models.CharField(max_length=50)),
                ('passwd', models.CharField(max_length=20)),
                ('group', models.ForeignKey(to='cmdbs.Groupinfos')),
            ],
            options={
                'db_table': 'userinfos',
                'permissions': (('view_machine', '机器管理'), ('view_platform', '平台管理'), ('view_Permission', '权限管理'), ('view_log', '日志查看'), ('view_operation_log', '操作日志'), ('view_web_log', 'web日志'), ('view_machine_list', '主机列表'), ('view_platform_update', '停机维护'), ('view_version_hotfix', '版本热更'), ('view_iframe_info', '查看基础页面'), ('view_cache', '缓存管理'), ('view_User_Management', '用户管理')),
            },
        ),
    ]
