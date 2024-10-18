# Generated by Django 5.0.6 on 2024-08-11 15:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_schedule_enddate_remove_schedule_startdate_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
        migrations.CreateModel(
            name='QrCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pension_status', models.TextField()),
                ('qr', models.FileField(upload_to='qrs/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])),
                ('seniors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]