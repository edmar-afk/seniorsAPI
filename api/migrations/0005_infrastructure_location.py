# Generated by Django 5.0.6 on 2025-06-19 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_infrastructure'),
    ]

    operations = [
        migrations.AddField(
            model_name='infrastructure',
            name='location',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
