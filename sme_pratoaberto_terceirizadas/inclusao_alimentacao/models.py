from django.core.validators import MinValueValidator
from django.db import models

from ..dados_comuns.models_abstract import (
    Descritivel, IntervaloDeDia,
    Nomeavel, TemData, TemChaveExterna,
    DiasSemana
)


class QuantidadePorPeriodo(TemChaveExterna):
    numero_alunos = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    periodo_escolar = models.ForeignKey('escola.PeriodoEscolar', on_delete=models.DO_NOTHING)
    tipos_alimentacao = models.ManyToManyField('cardapio.TipoAlimentacao')

    def __str__(self):
        return "{} alunos para {} com {} tipo(s) de alimentação".format(
            self.numero_alunos, self.periodo_escolar,
            self.tipos_alimentacao.count())

    class Meta:
        verbose_name = "Quantidade por periodo"
        verbose_name_plural = "Quantidades por periodo"


class MotivoInclusaoContinua(Nomeavel, TemChaveExterna):
    """
        continuo -  mais educacao
        continuo-sp integral
        continuo - outro
    """

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Motivo de inclusao contínua"
        verbose_name_plural = "Motivos de inclusao contínua"


class InclusaoAlimentacaoContinua(IntervaloDeDia, Descritivel, TemChaveExterna, DiasSemana):
    outro_motivo = models.CharField("Outro motivo", blank=True, null=True, max_length=50)
    motivo = models.ForeignKey(MotivoInclusaoContinua, on_delete=models.DO_NOTHING)
    escola = models.ForeignKey('escola.Escola', on_delete=models.DO_NOTHING,
                               related_name='inclusoes_alimentacao_continua')
    quantidades_periodo = models.ManyToManyField(QuantidadePorPeriodo)

    def __str__(self):
        return "de {} até {} para {} para {}".format(
            self.data_inicial, self.data_final, self.escola,
            self.dias_semana_display())

    class Meta:
        verbose_name = "Inclusão de alimentação contínua"
        verbose_name_plural = "Inclusões de alimentação contínua"


class MotivoInclusaoNormal(Nomeavel, TemChaveExterna):
    """
        reposicao de aula
        dia de familia
        outro
    """

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Motivo de inclusao normal"
        verbose_name_plural = "Motivos de inclusao normais"


class InclusaoAlimentacaoNormal(TemData, TemChaveExterna):
    quantidade_periodo = models.ForeignKey(QuantidadePorPeriodo, on_delete=models.DO_NOTHING,
                                           blank=True, null=True)
    prioritario = models.BooleanField(default=False)
    motivo = models.ForeignKey(MotivoInclusaoNormal, on_delete=models.DO_NOTHING)
    outro_motivo = models.CharField("Outro motivo", blank=True, null=True, max_length=50)

    def __str__(self):
        if self.outro_motivo:
            return "Dia {} {} ".format(self.data, self.outro_motivo)
        return "Dia {} {} ".format(self.data, self.motivo)

    class Meta:
        verbose_name = "Inclusão de alimentação normal"
        verbose_name_plural = "Inclusões de alimentação normal"


class GrupoInclusaoAlimentacaoNormal(Descritivel, TemChaveExterna):
    escola = models.ForeignKey('escola.Escola', on_delete=models.DO_NOTHING,
                               related_name='grupos_inclusoes_normais')
    inclusoes = models.ManyToManyField(InclusaoAlimentacaoNormal)

    # TODO: status aqui.
    def __str__(self):
        return "{} pedindo {} inclusoes".format(self.escola, self.inclusoes.count())

    class Meta:
        verbose_name = "Grupo de inclusão de alimentação normal"
        verbose_name_plural = "Grupos de inclusão de alimentação normal"
