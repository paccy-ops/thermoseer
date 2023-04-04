# Generated by Django 4.0.5 on 2023-04-03 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_alter_scannertemperature_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='scanner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scanners', to='demo.scannertemperature'),
        ),
    ]
