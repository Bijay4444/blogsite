# Generated by Django 5.1.1 on 2024-09-26 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='Status',
            new_name='status',
        ),
    ]
