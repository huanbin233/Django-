# Generated by Django 2.1.2 on 2019-03-09 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0032_auto_20190309_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_position',
            name='salary',
        ),
        migrations.AddField(
            model_name='job_position',
            name='salary1',
            field=models.IntegerField(default=0, verbose_name='薪资范围1'),
        ),
        migrations.AddField(
            model_name='job_position',
            name='salary2',
            field=models.IntegerField(default=0, verbose_name='薪资范围2'),
        ),
    ]