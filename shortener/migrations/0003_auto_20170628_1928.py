# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 13:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_links_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='links',
            new_name='Link',
        ),
    ]