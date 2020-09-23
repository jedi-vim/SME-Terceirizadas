# Generated by Django 2.2.13 on 2020-08-26 13:27

import uuid

import django.db.models.deletion
import django_xworkflows.models
from django.conf import settings
from django.db import migrations, models

import sme_terceirizadas.dados_comuns.behaviors


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0015_auto_20200313_1521'),
        ('terceirizada', '0003_auto_20191213_1339'),
        ('dados_comuns', '0019_auto_20200826_1327'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dieta_especial', '0013_auto_20200826_1327'),
        ('produto', '0041_reclamacaodeproduto_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='aditivos',
            field=models.TextField(blank=True, verbose_name='Aditivos'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='eh_para_alunos_com_dieta',
            field=models.BooleanField(default=False, verbose_name='É para alunos com dieta especial'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='outras_informacoes',
            field=models.TextField(blank=True, verbose_name='Outras Informações'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tem_aditivos_alergenicos',
            field=models.BooleanField(default=False, verbose_name='Tem aditivos alergênicos'),
        ),
        migrations.AlterField(
            model_name='protocolodedietaespecial',
            name='nome',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='reclamacaodeproduto',
            name='status',
            field=django_xworkflows.models.StateField(max_length=32, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='AGUARDANDO_AVALIACAO', name='ReclamacaoProdutoWorkflow', states=['AGUARDANDO_AVALIACAO', 'AGUARDANDO_RESPOSTA_TERCEIRIZADA', 'RESPONDIDO_TERCEIRIZADA', 'CODAE_ACEITOU', 'CODAE_RECUSOU', 'CODAE_RESPONDEU'])),
        ),
        migrations.CreateModel(
            name='SolicitacaoCadastroProdutoDieta',
            fields=[
                ('fluxosolicitacaocadastroproduto_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dados_comuns.FluxoSolicitacaoCadastroProduto')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nome_produto', models.CharField(max_length=150)),
                ('marca_produto', models.CharField(blank=True, max_length=150)),
                ('fabricante_produto', models.CharField(blank=True, max_length=150)),
                ('info_produto', models.TextField()),
                ('aluno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_cadastro_produto', to='escola.Aluno')),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('escola', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_cadastro_produto', to='escola.Escola')),
                ('solicitacao_dieta_especial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_cadastro_produto', to='dieta_especial.SolicitacaoDietaEspecial')),
                ('terceirizada', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_cadastro_produto', to='terceirizada.Terceirizada')),
            ],
            options={
                'abstract': False,
            },
            bases=('dados_comuns.fluxosolicitacaocadastroproduto', sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel, models.Model),
        ),
    ]