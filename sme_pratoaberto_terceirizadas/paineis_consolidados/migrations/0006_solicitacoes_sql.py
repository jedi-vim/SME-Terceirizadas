# Generated by Django 2.0.13 on 2019-08-26 19:31

import environ
from django.db import migrations

ROOT_DIR = environ.Path(__file__) - 2

sql_path = ROOT_DIR.path('sql', '0006_solicitacoes.sql')
with open(sql_path, 'r') as f:
    sql = f.read()


class Migration(migrations.Migration):
    dependencies = [
        ('paineis_consolidados', '0005_merge_20190903_1628'),
    ]

    operations = [
        migrations.RunSQL(sql),
    ]
