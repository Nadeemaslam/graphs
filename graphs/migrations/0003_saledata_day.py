# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0002_auto_20150707_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='saledata',
            name='day',
            field=models.TextField(max_length=10, null=True),
        ),
    ]
