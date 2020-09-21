# Generated by Django 2.2.13 on 2020-09-21 08:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dieta_especial', '0014_auto_20200903_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoContagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
