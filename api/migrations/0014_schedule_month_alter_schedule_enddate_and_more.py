# Generated by Django 5.0.6 on 2024-08-11 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_schedule_name_alter_schedule_enddate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='month',
            field=models.DateField(null=True, blank=True),
            preserve_default=False,
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
