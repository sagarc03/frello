# Generated by Django 4.0.4 on 2022-04-14 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frello', '0002_alter_project_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='create_by',
            new_name='created_by',
        ),
    ]
