# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_auto_20150722_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(default=b'C', max_length=1, choices=[(b'S', b'SUPER ADMIN'), (b'A', b'ACCOUNT ADMIN'), (b'C', b'CUSTOMER')]),
        ),
    ]
