# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20141223_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entries',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
