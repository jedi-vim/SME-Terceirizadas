# Generated by Django 2.2.8 on 2020-01-22 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dieta_especial', '0006_merge_20200122_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacaodietaespecial',
            name='ativo',
            field=models.BooleanField(default=True, verbose_name='Está ativo?'),
        ),
    ]
