# Generated by Django 3.0.6 on 2020-07-28 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_auto_20200727_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphs',
            name='typy_mobilu_hist',
            field=models.CharField(default='default', max_length=100000),
        ),
    ]