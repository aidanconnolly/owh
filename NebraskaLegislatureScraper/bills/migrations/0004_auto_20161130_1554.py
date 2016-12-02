# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_auto_20161130_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalinfo',
            name='link',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_name',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='consideredamendment',
            name='link',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='history',
            name='action',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='proposedamendment',
            name='link',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='textcopy',
            name='link',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='link',
            field=models.CharField(max_length=200),
        ),
    ]
