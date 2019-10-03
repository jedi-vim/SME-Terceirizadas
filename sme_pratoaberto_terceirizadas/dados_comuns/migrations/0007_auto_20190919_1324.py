# Generated by Django 2.0.13 on 2019-09-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0006_auto_20190918_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsolicitacoesusuario',
            name='status_evento',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Solicitação Realizada'), (1, 'CODAE autorizou'), (2, 'Terceirizada tomou ciência'), (3, 'Terceirizada recusou'), (4, 'CODAE negou'), (5, 'CODAE pediu revisão'), (6, 'DRE revisou'), (7, 'DRE validou'), (8, 'DRE pediu revisão'), (9, 'DRE não validou'), (10, 'Escola revisou'), (11, 'Escola cancelou'), (12, 'DRE cancelou')]),
        ),
    ]