# Generated by Django 5.0.6 on 2024-08-13 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_pension_qr_alter_profile_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pension',
            name='notification_status',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
