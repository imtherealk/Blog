# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20141228_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='image',
            field=models.ImageField(null=True, blank=True, upload_to='sandbox/entry-images'),
            preserve_default=True,
        ),
    ]
