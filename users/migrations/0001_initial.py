# Generated by Django 4.1.3 on 2022-12-03 11:23

from django.db import migrations, models
import django.utils.timezone
import tenant_users.permissions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email Address')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, tenant_users.permissions.models.PermissionsMixinFacade),
        ),
    ]
