# Generated by Django 5.1.3 on 2024-11-19 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0005_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='reservation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='reservation_slot',
            field=models.SmallIntegerField(default=10),
        ),
    ]
