# Generated by Django 2.1.2 on 2019-01-05 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogsettings',
            name='latest_feed_most_recent',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='blogsettings',
            name='site_link',
            field=models.CharField(default='blog', max_length=40),
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]
