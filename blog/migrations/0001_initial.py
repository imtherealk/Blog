# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Title', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
                ('Password', models.CharField(max_length=32)),
                ('Content', models.TextField(max_length=2000)),
                ('created', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Title', models.CharField(max_length=80)),
                ('Content', models.TextField()),
                ('created', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('Comments', models.PositiveSmallIntegerField(default=0, null=True)),
                ('Category', models.ForeignKey(to='blog.Categories')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Title', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entries',
            name='Tags',
            field=models.ManyToManyField(to='blog.TagModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='Entry',
            field=models.ForeignKey(to='blog.Entries'),
            preserve_default=True,
        ),
    ]
