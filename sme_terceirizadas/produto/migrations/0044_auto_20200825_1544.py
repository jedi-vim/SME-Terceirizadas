# Generated by Django 2.2.13 on 2020-08-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0043_solicitacaocadastroprodutodieta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaocadastroprodutodieta',
            name='fabricante_produto',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='solicitacaocadastroprodutodieta',
            name='marca_produto',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
