# Generated by Django 2.2.8 on 2020-03-03 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_prometheus.models
import django_xworkflows.models
import sme_terceirizadas.dados_comuns.behaviors
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('escola', '0014_mudancafaixasetarias_uuid'),
        ('terceirizada', '0003_auto_20191213_1339'),
        ('cardapio', '0013_remove_tipoalimentacao_substituicoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlteracaoCardapioCEI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('data', models.DateField(verbose_name='Data')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observação')),
                ('foi_solicitado_fora_do_prazo', models.BooleanField(default=False, verbose_name='Solicitação foi criada em cima da hora (5 dias úteis ou menos)?')),
                ('status', django_xworkflows.models.StateField(max_length=37, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_VALIDADO', 'DRE_PEDIU_ESCOLA_REVISAR', 'DRE_NAO_VALIDOU_PEDIDO_ESCOLA', 'CODAE_AUTORIZADO', 'CODAE_QUESTIONADO', 'CODAE_NEGOU_PEDIDO', 'TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU', 'CANCELADO_AUTOMATICAMENTE']))),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('escola', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='escola.Escola')),
                ('motivo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cardapio.MotivoAlteracaoCardapio')),
                ('rastro_dre', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cardapio_alteracaocardapiocei_rastro_dre', to='escola.DiretoriaRegional')),
                ('rastro_escola', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cardapio_alteracaocardapiocei_rastro_escola', to='escola.Escola')),
                ('rastro_lote', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cardapio_alteracaocardapiocei_rastro_lote', to='escola.Lote')),
                ('rastro_terceirizada', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cardapio_alteracaocardapiocei_rastro_terceirizada', to='terceirizada.Terceirizada')),
            ],
            options={
                'verbose_name': 'Alteração de cardápio CEI',
                'verbose_name_plural': 'Alterações de cardápio CEI',
            },
            bases=(django_prometheus.models.ExportModelOperationsMixin('alteracao_cardapio_cei'), django_xworkflows.models.BaseWorkflowEnabled, sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel, sme_terceirizadas.dados_comuns.behaviors.Logs, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade, models.Model),
        ),
        migrations.CreateModel(
            name='SubstituicaoAlimentacaoNoPeriodoEscolarCEI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('alteracao_cardapio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substituicoes_cei_periodo_escolar', to='cardapio.AlteracaoCardapioCEI')),
                ('periodo_escolar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='substituicoes_cei_periodo_escolar', to='escola.PeriodoEscolar')),
                ('tipo_alimentacao_de', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substituicoes_cei_tipo_alimentacao_de', to='cardapio.ComboDoVinculoTipoAlimentacaoPeriodoTipoUE')),
                ('tipo_alimentacao_para', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='substituicoes_cei_tipo_alimentacao_para', to='cardapio.SubstituicaoDoComboDoVinculoTipoAlimentacaoPeriodoTipoUE')),
            ],
            options={
                'verbose_name': 'Substituições de alimentação CEI no período',
                'verbose_name_plural': 'Substituições de alimentação CEI no período',
            },
            bases=(django_prometheus.models.ExportModelOperationsMixin('substituicao_cei_alimentacao_periodo_escolar'), models.Model),
        ),
        migrations.CreateModel(
            name='FaixaEtariaSubstituicaoAlimentacaoCEI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('quantidade', models.PositiveSmallIntegerField()),
                ('faixa_etaria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='escola.FaixaEtaria')),
                ('substituicao_alimentacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faixas_etarias', to='cardapio.SubstituicaoAlimentacaoNoPeriodoEscolarCEI')),
            ],
            options={
                'verbose_name': 'Faixa Etária de substituição de alimentação CEI',
                'verbose_name_plural': 'Faixas Etárias de substituição de alimentação CEI',
            },
            bases=(django_prometheus.models.ExportModelOperationsMixin('faixa_etaria_substituicao_alimentacao_cei'), models.Model),
        ),
    ]
