# Generated by Django 4.2.1 on 2023-06-14 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_status_name_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
