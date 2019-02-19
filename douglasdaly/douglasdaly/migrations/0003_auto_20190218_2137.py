# Generated by Django 2.1.7 on 2019-02-19 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20190218_2137'),
        ('douglasdaly', '0002_auto_20190105_0337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='siteadminsettings',
            options={'verbose_name': 'Site Admin Settings', 'verbose_name_plural': 'Site Admin Settings'},
        ),
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'Site Settings', 'verbose_name_plural': 'Site Settings'},
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_image',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.ImageAsset'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_show_card',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='home_tagline',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
