# Generated by Django 3.2.9 on 2021-11-26 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_categoria_nivel'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='is_grupo',
            field=models.BooleanField(default=False, verbose_name='Grupo'),
        ),
    ]
