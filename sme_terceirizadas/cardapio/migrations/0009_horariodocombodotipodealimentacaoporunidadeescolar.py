# Generated by Django 2.2.8 on 2019-12-24 01:46

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0004_auto_20191210_1045'),
        ('cardapio', '0008_vinculotipoalimentacaocomperiodoescolaretipounidadeescolar_ativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorarioDoComboDoTipoDeAlimentacaoPorUnidadeEscolar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('hora_inicial', models.TimeField()),
                ('hora_final', models.TimeField()),
                ('combo_tipos_alimentacao', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cardapio.ComboDoVinculoTipoAlimentacaoPeriodoTipoUE')),
                ('escola', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='escola.Escola')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
