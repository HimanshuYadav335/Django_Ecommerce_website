# Generated by Django 4.1.1 on 2023-07-15 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_order_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.BooleanField(default=False),
        ),
    ]
