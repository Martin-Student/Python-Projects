# Generated by Django 4.2.10 on 2024-02-08 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_members_age'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Members',
            new_name='Member',
        ),
    ]
