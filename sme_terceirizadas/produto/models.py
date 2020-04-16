from django.db import models

from ..dados_comuns.behaviors import (  # noqa I101
    Ativavel,
    CriadoEm,
    CriadoPor,
    Nomeavel,
    TemChaveExterna,
    TemIdentificadorExternoAmigavel
)


class ProtocoloDeDietaEspecial(Ativavel, CriadoEm, CriadoPor, Nomeavel, TemChaveExterna):

    def __str__(self):
        return self.nome


class Fabricante(Nomeavel, TemChaveExterna):

    def __str__(self):
        return self.nome


class Marca(Nomeavel, TemChaveExterna):

    def __str__(self):
        return self.nome


class ImagemDoProduto(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.DO_NOTHING)
    arquivo = models.FileField()


class Produto(Ativavel, CriadoEm, CriadoPor, Nomeavel, TemChaveExterna):
    eh_para_alunos_com_dieta = models.BooleanField(default=False)
    protocolos = models.ManyToManyField('ProtocoloDeDietaEspecial',
                                        related_name='protocolos',
                                        help_text='Protocolos do produto.',
                                        blank=True,
                                        )
    detalhes_da_dieta = models.TextField()

    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.DO_NOTHING)
    componentes = models.CharField('Componentes do Produto', blank=True, max_length=100)

    tem_aditivos_alergenicos = models.BooleanField(default=False)
    aditivos = models.TextField()

    tipo = models.CharField('Tipo do Produto', blank=True, max_length=50)
    embalagem = models.CharField('Embalagem Primária', blank=True, max_length=100)
    prazo_validade = models.CharField('Prazo de validade', blank=True, max_length=100)
    info_armazenamento = models.CharField('Informações de Armazenamento',
                                          blank=True, max_length=100)
    outras_informacoes = models.TextField()
    numero_registro = models.CharField('Registro do órgão competente', blank=True, max_length=100)


class TipoDeInformacaoNutricional(Nomeavel, TemChaveExterna):
    def __str__(self):
        return self.nome


class InformacaoNutricional(TemChaveExterna, Nomeavel):
    quantidade_porcao = models.CharField('Quantidade por Porção', blank=True, max_length=10)
    valor_diario = models.CharField('%VD(*)', blank=True, max_length=3)
    tipo_nutricional = models.ForeignKey(TipoDeInformacaoNutricional, on_delete=models.DO_NOTHING)


class InformacoesNutricionaisDoProduto(TemChaveExterna):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    informacoes_nutricionais = models.ManyToManyField(InformacaoNutricional,
                                                      related_name='informacoes_nutricionais')
    porcao = models.CharField(blank=True, max_length=50)
    unidade_caseira = models.CharField(blank=True, max_length=50)
