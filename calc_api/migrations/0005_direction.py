# Generated by Django 4.0.2 on 2022-02-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc_api', '0004_equipment_project_price_alter_equipment_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(default='', max_length=15)),
                ('direction_name_ua', models.CharField(default='', max_length=100)),
                ('direction_name_ru', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
