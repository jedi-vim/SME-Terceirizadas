# Generated by Django 2.0.13 on 2019-08-29 18:20

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('kit_lanche', '0002_auto_20190826_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaokitlancheunificada',
            name='status',
            field=django_xworkflows.models.StateField(max_length=25, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaDiretoriaRegionalWorkflow', states=['RASCUNHO', 'CODAE_A_VALIDAR', 'DRE_PEDE_ESCOLA_REVISAR', 'CODAE_CANCELOU_PEDIDO', 'CODAE_APROVADO', 'TERCEIRIZADA_TOMA_CIENCIA', 'CANCELAMENTO_AUTOMATICO'])),
        ),
    ]