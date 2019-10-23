# Generated by Django 2.2.6 on 2019-10-22 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0007_auto_20191008_1829'),
        ('terceirizada', '0006_auto_20191008_1819'),
        ('kit_lanche', '0010_auto_20191008_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacaokitlancheavulsa',
            name='rastro_dre',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='kit_lanche_solicitacaokitlancheavulsa_rastro_dre', to='escola.DiretoriaRegional'),
        ),
        migrations.AddField(
            model_name='solicitacaokitlancheavulsa',
            name='rastro_escola',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='kit_lanche_solicitacaokitlancheavulsa_rastro_escola', to='escola.Escola'),
        ),
        migrations.AddField(
            model_name='solicitacaokitlancheavulsa',
            name='rastro_lote',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='kit_lanche_solicitacaokitlancheavulsa_rastro_lote', to='escola.Lote'),
        ),
        migrations.AddField(
            model_name='solicitacaokitlancheavulsa',
            name='rastro_terceirizada',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='kit_lanche_solicitacaokitlancheavulsa_rastro_terceirizada', to='terceirizada.Terceirizada'),
        ),
    ]
