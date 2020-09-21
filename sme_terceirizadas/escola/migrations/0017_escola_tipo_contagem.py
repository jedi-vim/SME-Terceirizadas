# Generated by Django 2.2.13 on 2020-09-21 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dieta_especial', '0015_tipocontagem'),
        ('escola', '0016_periodoescolar_horas_atendimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='escola',
            name='tipo_contagem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='escolas', to='dieta_especial.TipoContagem'),
        ),
    ]
