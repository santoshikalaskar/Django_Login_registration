# Generated by Django 3.0.3 on 2020-02-12 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Loginregistration', '0002_auto_20200211_0543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='conformpassword',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='fullname',
        ),
    ]
