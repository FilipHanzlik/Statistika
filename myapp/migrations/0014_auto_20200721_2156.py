# Generated by Django 3.0.6 on 2020-07-21 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20200721_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphs',
            name='vysky_graph_muzi',
            field=models.CharField(default='default', max_length=100000),
        ),
        migrations.AddField(
            model_name='graphs',
            name='vysky_graph_zeny',
            field=models.CharField(default='default', max_length=100000),
        ),
    ]