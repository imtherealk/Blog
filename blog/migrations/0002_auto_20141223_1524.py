# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='Entry',
            new_name='entry',
        ),
        migrations.RenameField(
            model_name='entries',
            old_name='Tags',
            new_name='tags',
        ),
    ]
