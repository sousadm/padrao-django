# Generated by Django 3.2.9 on 2021-11-28 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_auto_20211128_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='categoria',
            name='created_dt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='categoria',
            name='update_dt',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
