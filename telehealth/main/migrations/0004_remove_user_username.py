# Generated by Django 4.0.5 on 2022-07-02 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
