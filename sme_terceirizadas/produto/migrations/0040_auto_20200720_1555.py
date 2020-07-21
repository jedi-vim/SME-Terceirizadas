# Generated by Django 2.2.13 on 2020-07-20 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0015_auto_20200313_1521'),
        ('produto', '0039_auto_20200701_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reclamacaodeproduto',
            name='vinculo',
        ),
        migrations.AddField(
            model_name='reclamacaodeproduto',
            name='escola',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reclamacoes', to='escola.Escola'),
        ),
    ]