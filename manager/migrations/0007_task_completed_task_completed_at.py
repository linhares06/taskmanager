# Generated by Django 4.2.1 on 2023-06-15 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_alter_status_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]