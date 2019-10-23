# Generated by Django 2.2.6 on 2019-10-10 13:40

from django.db import migrations, models
import sme_terceirizadas.dados_comuns.behaviors


class Migration(migrations.Migration):

    dependencies = [
        ('paineis_consolidados', '0009_solicitacoesV3'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacoesTerceirizada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('escola_uuid', models.UUIDField(editable=False)),
                ('lote', models.CharField(max_length=50)),
                ('dre_uuid', models.UUIDField(editable=False)),
                ('dre_nome', models.CharField(max_length=200)),
                ('terceirizada_uuid', models.UUIDField(editable=False)),
                ('criado_em', models.DateTimeField()),
                ('data_doc', models.DateField()),
                ('tipo_doc', models.CharField(max_length=30)),
                ('desc_doc', models.CharField(max_length=50)),
                ('status_evento', models.PositiveSmallIntegerField()),
                ('status', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'solicitacoes_consolidadas',
                'abstract': False,
                'managed': False,
            },
            bases=(models.Model, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade),
        ),
    ]
