# Generated by Django 3.2 on 2024-11-24 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingApp', '0002_auto_20241123_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='apoderado',
            name='alumno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ingApp.alumno'),
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='apellido',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='domicilio',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='nacionalidad',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='nivel_educacional',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='oficio',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='apoderado',
            name='run',
            field=models.CharField(max_length=12),
        ),
    ]
