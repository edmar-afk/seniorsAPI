# Generated by Django 5.0.6 on 2024-08-12 00:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_schedule_enddatetime_alter_schedule_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='pension_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pension'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='endDatetime',
            field=models.TimeField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='month',
            field=models.DateField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='startDatetime',
            field=models.TimeField(null=True, blank=True),
            preserve_default=False,
        ),
    ]
