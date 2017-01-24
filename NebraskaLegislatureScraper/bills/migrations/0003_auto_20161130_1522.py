# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_auto_20161128_1636'),
    ]

    operations = [
        migrations.RenameField(
            model_name='committee',
            old_name='committee_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='committee',
            old_name='committee_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='senator',
            old_name='senator_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='senator',
            name='senator_id',
        ),
        migrations.AlterField(
            model_name='senator',
            name='id',
            field=models.CharField(max_length=10, serialize=False, primary_key=True),
        ),
    ]
