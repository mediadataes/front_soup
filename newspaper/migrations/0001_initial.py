# Generated by Django 2.2.1 on 2019-05-22 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newspaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('url', models.URLField(max_length=128)),
                ('morning', models.TimeField(default=datetime.time(10, 0))),
                ('afternoon', models.TimeField(default=datetime.time(16, 0))),
                ('night', models.TimeField(default=datetime.time(22, 0))),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
