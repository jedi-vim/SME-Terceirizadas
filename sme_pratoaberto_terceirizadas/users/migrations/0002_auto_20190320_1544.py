# Generated by Django 2.0.13 on 2019-03-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='functional_register',
            field=models.CharField(blank=True, max_length=60, null=True, unique=True, verbose_name='Functional register'),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile_phone',
            field=models.CharField(max_length=11, null=True, verbose_name='Mobile phone'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, null=True, verbose_name='Phone'),
        ),
    ]
