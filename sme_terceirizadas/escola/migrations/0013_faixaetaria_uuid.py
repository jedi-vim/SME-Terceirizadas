# Generated by Django 2.2.8 on 2020-02-19 19:46

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0012_faixaetaria_mudancafaixasetarias'),
    ]

    operations = [
        migrations.AddField(
            model_name='faixaetaria',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
