# Generated by Django 3.1 on 2020-08-22 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_auto_20200818_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='SpokojenySeSkolnimSys',
        ),
    ]