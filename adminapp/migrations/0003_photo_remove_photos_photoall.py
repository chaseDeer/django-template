# Generated by Django 4.1.7 on 2023-04-05 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_lunbo_photos_usermini_videolive_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assetsid', models.CharField(max_length=128)),
                ('assets_type', models.CharField(max_length=128)),
                ('assets_url', models.CharField(max_length=128)),
                ('creat_time', models.DateTimeField(auto_now_add=True)),
                ('updata_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='photos',
            name='photoall',
        ),
    ]
