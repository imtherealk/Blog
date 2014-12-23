# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20141223_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='comment_num',
            field=models.PositiveSmallIntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
