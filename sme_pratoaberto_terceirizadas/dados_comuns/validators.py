import datetime

from rest_framework import serializers
from traitlets import Any
from workalendar.america import BrazilSaoPauloCity
from django.db import models

from .utils import eh_dia_util, obter_dias_uteis_apos_hoje

calendario = BrazilSaoPauloCity()


def nao_pode_ser_no_passado(data: datetime.date):
    if data < datetime.date.today():
        raise serializers.ValidationError('Não pode ser no passado')
    return True


def deve_pedir_com_antecedencia(dia: datetime.date, dias: int = 2):
    prox_dia_util = obter_dias_uteis_apos_hoje(quantidade_dias=dias)
    if dia < prox_dia_util:
        raise serializers.ValidationError(f'Deve pedir com pelo menos {dias} dias úteis de antecedência')
    return True


def deve_existir_cardapio(escola, data: datetime.date):
    if not escola.get_cardapio(data):
        raise serializers.ValidationError(f'Escola não possui cardápio para esse dia: {data}')
    return True


def dia_util(data: datetime.date):
    if not eh_dia_util(data):
        raise serializers.ValidationError('Não é dia útil em São Paulo')
    return True


def verificar_se_existe(obj_model, **kwargs) -> bool:
    try:
        if not issubclass(obj_model, models.Model):
            raise TypeError('obj_model deve ser um "django models class"')
    except TypeError:
        raise TypeError('obj_model deve ser um "django models class"')
    existe = obj_model.objects.filter(**kwargs).exists()
    return existe


def objeto_nao_deve_ter_duplicidade(obj_model, mensagem='Objeto já existe', **kwargs, ):
    qtd = obj_model.objects.filter(**kwargs).count()
    if qtd:
        raise serializers.ValidationError(mensagem)


def nao_pode_ser_feriado(data: datetime.date, mensagem='Não pode ser no feriado'):
    if calendario.is_holiday(data):
        raise serializers.ValidationError(mensagem)


def nao_pode_ser_nulo(valor: Any, mensagem='Não pode ser nulo'):
    if not valor:
        raise serializers.ValidationError(mensagem)


def deve_ser_deste_tipo(valor: Any, tipo=str, mensagem='Deve ser do tipo texto'):
    if type(valor) is not tipo:
        raise serializers.ValidationError(mensagem)
