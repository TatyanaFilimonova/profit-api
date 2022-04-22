# Generated by Django 4.0.2 on 2022-04-11 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc_api', '0009_competence_customer_phone_staff_stage_project_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='phone',
        ),
        migrations.AddField(
            model_name='phone',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='customer_detail', to='calc_api.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phone',
            name='stuff',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='staff_detail', to='calc_api.staff'),
            preserve_default=False,
        ),
    ]
