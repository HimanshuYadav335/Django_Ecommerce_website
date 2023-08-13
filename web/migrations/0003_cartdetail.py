# Generated by Django 4.1.1 on 2023-07-09 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_productdetail_ptitle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('pimage', models.ImageField(upload_to='C:\\venv\\Ecommerce\\static\\media')),
                ('pdetail', models.TextField(max_length=100)),
                ('pprice', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ptitle', models.TextField(default='non', max_length=20)),
                ('pnumber', models.IntegerField(default=1, max_length=5)),
            ],
        ),
    ]
