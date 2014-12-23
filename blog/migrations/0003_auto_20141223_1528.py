# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141223_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='Title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='Content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='Password',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='entries',
            old_name='Category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='entries',
            old_name='Content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='entries',
            old_name='Title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='tagmodel',
            old_name='Title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='entries',
            name='Comments',
        ),
    ]
