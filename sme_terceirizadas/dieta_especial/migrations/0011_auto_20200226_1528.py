# Generated by Django 2.2.8 on 2020-02-26 18:28

from django.db import migrations, models
import django_xworkflows.models
import sme_terceirizadas.dados_comuns.validators


class Migration(migrations.Migration):

    dependencies = [
        ('dieta_especial', '0010_anexo_eh_laudo_alta'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacaodietaespecial',
            name='data_termino',
            field=models.DateField(null=True, validators=[sme_terceirizadas.dados_comuns.validators.nao_pode_ser_no_passado]),
        ),
        migrations.AlterField(
            model_name='solicitacaodietaespecial',
            name='status',
            field=django_xworkflows.models.StateField(max_length=37, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='DietaEspecialWorkflow', states=['RASCUNHO', 'CODAE_A_AUTORIZAR', 'CODAE_NEGOU_PEDIDO', 'CODAE_AUTORIZADO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU', 'ESCOLA_SOLICITOU_INATIVACAO', 'CODAE_NEGOU_INATIVACAO', 'CODAE_AUTORIZOU_INATIVACAO', 'TERCEIRIZADA_TOMOU_CIENCIA_INATIVACAO', 'TERMINADA'])),
        ),
    ]
