# Generated by Django 2.1.2 on 2019-03-25 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0041_notify_h'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify_h',
            name='status',
            field=models.BooleanField(default=True, verbose_name='已读'),
        ),
    ]