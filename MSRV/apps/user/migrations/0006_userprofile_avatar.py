# Generated by Django 5.1.6 on 2025-04-08 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
