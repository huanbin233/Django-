# Generated by Django 2.1.2 on 2019-04-14 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0048_auto_20190414_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendresume',
            name='is_employ',
            field=models.CharField(choices=[('1', '录取'), ('0', '待考验')], default='0', max_length=2, verbose_name='录取情况'),
        ),
    ]