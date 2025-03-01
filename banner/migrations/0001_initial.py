# Generated by Django 5.1.6 on 2025-03-02 07:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_img', models.ImageField(upload_to='banner/')),
                ('banner_title', models.CharField(max_length=200)),
                ('banner_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
