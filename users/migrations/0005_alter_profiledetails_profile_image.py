# Generated by Django 5.1.6 on 2025-03-10 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_title_profiledetails_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiledetails',
            name='Profile_Image',
            field=models.ImageField(default='https://static.vecteezy.com/system/resources/thumbnails/013/360/247/small/default-avatar-photo-icon-social-media-profile-sign-symbol-vector.jpg', upload_to='profile/'),
        ),
    ]
