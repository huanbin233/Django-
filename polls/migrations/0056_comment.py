# Generated by Django 2.1.2 on 2019-05-04 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0055_sendresume_show_notify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com', models.TextField(max_length=2000, verbose_name='评论内容')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Company', verbose_name='被评论公司')),
                ('stu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.UserProfile', verbose_name='评论人')),
            ],
        ),
    ]