# Generated by Django 4.2.10 on 2024-02-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0002_alter_relation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
