# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('bill_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('bill_number', models.CharField(max_length=10)),
                ('bill_name', models.CharField(max_length=250)),
                ('introduction_date', models.DateField()),
                ('status', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsideredAmendment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50, blank=True)),
                ('link', models.CharField(max_length=100)),
                ('bill_id', models.ForeignKey(to='bills.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('action', models.CharField(max_length=100)),
                ('journal_page', models.CharField(max_length=50)),
                ('bill_id', models.ForeignKey(to='bills.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Introducer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('introducer_id', models.CharField(max_length=10)),
                ('introducer_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProposedAmendment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proposer', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50, blank=True)),
                ('link', models.CharField(max_length=100)),
                ('bill_id', models.ForeignKey(to='bills.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='TextCopy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
                ('bill_id', models.ForeignKey(to='bills.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=100)),
                ('bill_id', models.ForeignKey(to='bills.Bill')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='introducer_id',
            field=models.ManyToManyField(to='bills.Introducer'),
        ),
        migrations.AddField(
            model_name='additionalinfo',
            name='bill_id',
            field=models.ForeignKey(to='bills.Bill'),
        ),
    ]
