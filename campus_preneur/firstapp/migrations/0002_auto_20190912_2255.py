# Generated by Django 2.2.5 on 2019-09-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
