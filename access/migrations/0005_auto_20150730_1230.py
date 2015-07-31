# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_auto_20150730_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(default=b'C', max_length=1, choices=[(b'S', b'Super Admin'), (b'A', b'Account Admin'), (b'C', b'Customer')]),
        ),
    ]
