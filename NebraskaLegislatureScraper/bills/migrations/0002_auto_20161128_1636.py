# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('committee_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('committee_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Senator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('senator_id', models.CharField(max_length=10)),
                ('senator_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='bill',
            name='introducer_id',
        ),
        migrations.DeleteModel(
            name='Introducer',
        ),
        migrations.AddField(
            model_name='bill',
            name='co_sponsors',
            field=models.ManyToManyField(related_name='CoSponsors', null=True, to='bills.Senator'),
        ),
        migrations.AddField(
            model_name='bill',
            name='committee_primary_sponsor',
            field=models.ForeignKey(related_name='CommSponsor', to='bills.Committee', null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='senator_primary_sponsor',
            field=models.ForeignKey(related_name='SenSponsor', to='bills.Senator', null=True),
        ),
    ]
