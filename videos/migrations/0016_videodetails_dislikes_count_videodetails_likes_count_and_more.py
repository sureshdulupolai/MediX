# Generated by Django 5.1.6 on 2025-03-22 16:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_alter_videodetails_customer_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='videodetails',
            name='dislikes_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='videodetails',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Vd_Like_Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.PositiveIntegerField(default=0)),
                ('dislike', models.PositiveIntegerField(default=0)),
                ('user_vd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.videodetails')),
            ],
            options={
                'unique_together': {('user_vd', 'video')},
            },
        ),
        migrations.DeleteModel(
            name='VideoCategory',
        ),
    ]
