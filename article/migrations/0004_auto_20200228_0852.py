# Generated by Django 3.0.3 on 2020-02-28 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200228_0851'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='sub_category',
            new_name='parent',
        ),
    ]
