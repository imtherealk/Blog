# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_entries_comment_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entries',
            name='created',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
