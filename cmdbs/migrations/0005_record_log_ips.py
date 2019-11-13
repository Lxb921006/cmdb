# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbs', '0004_auto_20190921_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='record_log',
            name='ips',
            field=models.CharField(max_length=20, default=1),
            preserve_default=False,
        ),
    ]
