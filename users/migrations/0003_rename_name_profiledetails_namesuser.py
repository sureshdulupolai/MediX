# Generated by Django 5.1.6 on 2025-03-10 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profiledetails_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profiledetails',
            old_name='Name',
            new_name='NamesUser',
        ),
    ]
