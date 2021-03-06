# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 05:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Like_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='user_images')),
                ('image_url', models.CharField(max_length=255)),
                ('caption', models.CharField(max_length=240)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('has_liked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sesseion_token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=120)),
                ('username', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=40)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='sesseion_token',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demoapp.UserModel'),
        ),
        migrations.AddField(
            model_name='post_model',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demoapp.UserModel'),
        ),
        migrations.AddField(
            model_name='like_model',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demoapp.Post_Model'),
        ),
        migrations.AddField(
            model_name='like_model',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demoapp.UserModel'),
        ),
    ]
