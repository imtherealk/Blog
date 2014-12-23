# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='Entry',
        ),
        migrations.RemoveField(
            model_name='entries',
            name='Tags',
        ),
        migrations.AddField(
            model_name='comments',
            name='entry',
            field=models.ForeignKey(to='blog.Entries'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entries',
            name='tags',
            field=models.ManyToManyField(to='blog.TagModel'),
            preserve_default=True,
        ),
    ]
