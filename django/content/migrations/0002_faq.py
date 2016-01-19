# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 11:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=150)),
                ('answer', models.TextField(max_length=500)),
                ('position', models.IntegerField()),
                ('publish', models.BooleanField(default=False)),
                ('privacy', models.CharField(choices=[('public_only', 'Public only'), ('public', 'Public'), ('private', 'Private')], default='private', max_length=100)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]