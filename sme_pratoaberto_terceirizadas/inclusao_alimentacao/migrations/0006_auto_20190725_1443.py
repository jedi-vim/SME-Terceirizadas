# Generated by Django 2.0.13 on 2019-07-25 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inclusao_alimentacao', '0005_inclusaoalimentacaocontinua_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantidadeporperiodo',
            name='grupo_inclusao_normal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quantidades_por_periodo', to='inclusao_alimentacao.GrupoInclusaoAlimentacaoNormal'),
        ),
        migrations.AlterField(
            model_name='quantidadeporperiodo',
            name='inclusao_alimentacao_continua',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quantidades_por_periodo', to='inclusao_alimentacao.InclusaoAlimentacaoContinua'),
        ),
    ]