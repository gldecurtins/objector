# Generated by Django 4.0.2 on 2022-02-03 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=80, unique=True, verbose_name='name'),
        ),
    ]