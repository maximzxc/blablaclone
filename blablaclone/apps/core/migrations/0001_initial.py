# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('surname', models.CharField(max_length=150)),
                ('car', models.CharField(max_length=150, blank=True)),
                ('phone', models.CharField(max_length=150, blank=True)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('about', models.TextField(blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'images', blank=True)),
                ('is_staff', models.BooleanField(default=False, editable=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                (b'objects', core.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('departure_time', models.DateTimeField()),
                ('free_places', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'title', blank=True, unique=True)),
                ('title', models.CharField(max_length=150)),
                ('driver', models.ForeignKey(related_name='user_rides', to=settings.AUTH_USER_MODEL)),
                ('from_city', models.ForeignKey(related_name='city_rides', to='core.City')),
                ('passangers', models.ManyToManyField(related_name='user_rides2', to=settings.AUTH_USER_MODEL)),
                ('to_city', models.ForeignKey(related_name='city_rides2', to='core.City')),
                ('will_visit', models.ManyToManyField(related_name='city_rides3', to='core.City')),
            ],
        ),
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('ride', models.ForeignKey(related_name='ride_riderequests', to='core.Ride')),
                ('user', models.ForeignKey(related_name='user_riderequests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
