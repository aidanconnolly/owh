# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_auto_20161130_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='co_sponsors',
            field=models.ManyToManyField(related_name='CoSponsors', to='bills.Senator'),
        ),
    ]
