# Generated by Django 3.1.5 on 2021-02-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_auto_20210209_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='place',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='repair',
            field=models.TextField(blank=True, null=True),
        ),
    ]
