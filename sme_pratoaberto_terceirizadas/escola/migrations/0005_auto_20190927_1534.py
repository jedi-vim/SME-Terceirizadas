# Generated by Django 2.0.13 on 2019-09-27 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0004_remove_escola_codigo_codae'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lote',
            options={'ordering': ('nome',), 'verbose_name': 'Lote', 'verbose_name_plural': 'Lotes'},
        ),
    ]