# Generated by Django 4.0.1 on 2022-01-18 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.models
import rules.contrib.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=inventory.models.location_image_upload_handler)),
                ('address', models.TextField(blank=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'Alert'), (20, 'Warning'), (30, 'Good')], default=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('maintenance_team', models.ForeignKey(blank=True, help_text='Team members can view this location.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_maintenance_team', to='common.team')),
                ('management_team', models.ForeignKey(blank=True, help_text='Team members can view, change or delete this location.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_management_team', to='common.team')),
                ('owner', models.ForeignKey(help_text='Owner can view, change or delete this location.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['status', 'name'],
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=inventory.models.objekt_image_upload_handler)),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'Alert'), (20, 'Warning'), (30, 'Good')], default=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.location')),
                ('maintenance_team', models.ForeignKey(blank=True, help_text='Team members can view this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objekt_maintenance_team', to='common.team')),
                ('management_team', models.ForeignKey(blank=True, help_text='Team members can view or update this object.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objekt_management_team', to='common.team')),
                ('owner', models.ForeignKey(help_text='Owner can view, change or delete this object.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['status', 'name'],
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
