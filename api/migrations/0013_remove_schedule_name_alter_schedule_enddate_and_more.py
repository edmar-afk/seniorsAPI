# Generated by Django 5.0.6 on 2024-08-11 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_schedule_end_time_remove_schedule_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='name',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='endDate',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='startDate',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=False,
        ),
    ]
