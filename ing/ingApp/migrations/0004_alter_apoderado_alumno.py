# Generated by Django 3.2 on 2024-11-24 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingApp', '0003_auto_20241123_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apoderado',
            name='alumno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apoderado', to='ingApp.alumno'),
        ),
    ]