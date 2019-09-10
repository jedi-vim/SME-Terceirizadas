# Generated by Django 2.0.13 on 2019-09-02 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0002_auto_20190826_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codae',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='diretoriaregional',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='escola',
            name='codigo_codae',
            field=models.CharField(blank=True, default='', max_length=10, unique=True, verbose_name='Código CODAE'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='escola',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=160, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faixaidadeescolar',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lote',
            name='iniciais',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='Iniciais'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lote',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='periodoescolar',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subprefeitura',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tipogestao',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tipounidadeescolar',
            name='iniciais',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='Iniciais'),
            preserve_default=False,
        ),
    ]
