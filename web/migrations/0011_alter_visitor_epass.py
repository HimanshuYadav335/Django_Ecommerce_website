# Generated by Django 4.1.1 on 2023-08-15 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_alter_visitor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='epass',
            field=models.TextField(max_length=10),
        ),
    ]
