import datetime

from django.db import models
from django.db.models import Q

from ..dados_comuns.constants import DAQUI_A_30_DIAS, DAQUI_A_7_DIAS
from ..dados_comuns.fluxo_status import (
    InformativoPartindoDaEscolaWorkflow, PedidoAPartirDaDiretoriaRegionalWorkflow,
    PedidoAPartirDaEscolaWorkflow
)
from ..dados_comuns.models import LogSolicitacoesUsuario
from ..dados_comuns.models_abstract import TemPrioridade


class SolicitacoesDestaSemanaManager(models.Manager):
    def get_queryset(self):
        hoje = datetime.date.today()
        data_limite_inicial = hoje
        data_limite_final = hoje + datetime.timedelta(7)
        return super(SolicitacoesDestaSemanaManager, self).get_queryset(
        ).filter(data_doc__range=(data_limite_inicial, data_limite_final))


class SolicitacoesDesteMesManager(models.Manager):
    def get_queryset(self):
        hoje = datetime.date.today()
        data_limite_inicial = hoje
        data_limite_final = hoje + datetime.timedelta(31)
        return super(SolicitacoesDesteMesManager, self).get_queryset(
        ).filter(data_doc__range=(data_limite_inicial, data_limite_final))


class MoldeConsolidado(models.Model, TemPrioridade):
    uuid = models.UUIDField(editable=False)
    escola_uuid = models.UUIDField(editable=False)
    lote = models.CharField(max_length=50)
    dre_uuid = models.UUIDField(editable=False)
    dre_nome = models.CharField(max_length=200)
    terceirizada_uuid = models.UUIDField(editable=False)
    criado_em = models.DateTimeField()
    data_doc = models.DateField()
    tipo_doc = models.CharField(max_length=30)
    desc_doc = models.CharField(max_length=50)
    status_evento = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=32)

    objects = models.Manager()
    filtro_7_dias = SolicitacoesDestaSemanaManager()
    filtro_30_dias = SolicitacoesDesteMesManager()

    @classmethod
    def get_pendentes_autorizacao(cls, **kwargs):
        raise NotImplementedError('Precisa implementar')

    @classmethod
    def get_autorizados(cls, **kwargs):
        raise NotImplementedError('Precisa implementar')

    @classmethod
    def get_negados(cls, **kwargs):
        raise NotImplementedError('Precisa implementar')

    @classmethod
    def get_cancelados(cls, **kwargs):
        raise NotImplementedError('Precisa implementar')

    @property
    def data(self):
        return self.data_doc

    @classmethod
    def _get_manager(cls, kwargs):
        filtro = kwargs.get('filtro')
        manager = cls.objects
        if filtro == DAQUI_A_7_DIAS:
            manager = cls.filtro_7_dias
        elif filtro == DAQUI_A_30_DIAS:
            manager = cls.filtro_30_dias
        return manager

    class Meta:
        managed = False
        db_table = 'solicitacoes_consolidadas'
        abstract = True


class SolicitacoesCODAE(MoldeConsolidado):

    @classmethod
    def get_pendentes_autorizacao(cls, **kwargs):
        manager = cls._get_manager(kwargs)
        return manager.filter(
            status_evento=LogSolicitacoesUsuario.DRE_VALIDOU,
            status=PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_autorizados(cls, **kwargs):
        return cls.objects.filter(
            status_evento__in=[LogSolicitacoesUsuario.CODAE_AUTORIZOU,
                               LogSolicitacoesUsuario.TERCEIRIZADA_TOMOU_CIENCIA],
            status__in=[PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO,
                        PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA]
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_negados(cls, **kwargs):
        return cls.objects.filter(
            status_evento=LogSolicitacoesUsuario.CODAE_NEGOU,
            status=PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_cancelados(cls, **kwargs):
        return cls.objects.filter(
            status_evento__in=[LogSolicitacoesUsuario.DRE_CANCELOU,
                               LogSolicitacoesUsuario.ESCOLA_CANCELOU],
            status__in=[PedidoAPartirDaEscolaWorkflow.ESCOLA_CANCELOU,
                        PedidoAPartirDaDiretoriaRegionalWorkflow.DRE_CANCELOU],
        ).order_by('uuid', '-criado_em').distinct('uuid')


class SolicitacoesEscola(MoldeConsolidado):

    @classmethod
    def get_pendentes_autorizacao(cls, **kwargs):
        escola_uuid = kwargs.get('escola_uuid')
        return cls.objects.filter(
            escola_uuid=escola_uuid
        ).filter(
            status__in=[PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR,
                        PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO,
                        InformativoPartindoDaEscolaWorkflow.INFORMADO],
            status_evento__in=[LogSolicitacoesUsuario.INICIO_FLUXO,
                               LogSolicitacoesUsuario.DRE_VALIDOU,
                               LogSolicitacoesUsuario.INICIO_FLUXO]
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_autorizados(cls, **kwargs):
        escola_uuid = kwargs.get('escola_uuid')
        return cls.objects.filter(
            escola_uuid=escola_uuid
        ).filter(
            Q(status_evento=LogSolicitacoesUsuario.CODAE_AUTORIZOU,
              status=PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO) |  # noqa W504
            Q(status_evento=LogSolicitacoesUsuario.TERCEIRIZADA_TOMOU_CIENCIA,
              status=PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA)
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_negados(cls, **kwargs):
        escola_uuid = kwargs.get('escola_uuid')
        return cls.objects.filter(
            status_evento=LogSolicitacoesUsuario.CODAE_NEGOU,
            status=PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO,
            escola_uuid=escola_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_cancelados(cls, **kwargs):
        escola_uuid = kwargs.get('escola_uuid')
        return cls.objects.filter(
            status_evento=LogSolicitacoesUsuario.ESCOLA_CANCELOU,
            status=PedidoAPartirDaEscolaWorkflow.ESCOLA_CANCELOU,
            escola_uuid=escola_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')


class SolicitacoesDRE(MoldeConsolidado):

    @classmethod
    def get_pendentes_autorizacao(cls, **kwargs):
        dre_uuid = kwargs.get('dre_uuid')
        return cls.objects.filter(
            status__in=[PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_A_AUTORIZAR,
                        PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO],
            status_evento__in=[LogSolicitacoesUsuario.DRE_VALIDOU,
                               LogSolicitacoesUsuario.INICIO_FLUXO],
            dre_uuid=dre_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_pendentes_validacao(cls, **kwargs):
        dre_uuid = kwargs.get('dre_uuid')
        manager = cls._get_manager(kwargs)
        return manager.filter(
            status=PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR,
            status_evento=LogSolicitacoesUsuario.INICIO_FLUXO,
            dre_uuid=dre_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_autorizados(cls, **kwargs):
        dre_uuid = kwargs.get('dre_uuid')
        return cls.objects.filter(
            status_evento__in=[LogSolicitacoesUsuario.CODAE_AUTORIZOU,
                               LogSolicitacoesUsuario.TERCEIRIZADA_TOMOU_CIENCIA],
            status__in=[PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_AUTORIZADO,
                        PedidoAPartirDaDiretoriaRegionalWorkflow.TERCEIRIZADA_TOMOU_CIENCIA,
                        PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO,
                        PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA],
            dre_uuid=dre_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_negados(cls, **kwargs):
        dre_uuid = kwargs.get('dre_uuid')
        return cls.objects.filter(
            status_evento__in=[LogSolicitacoesUsuario.CODAE_NEGOU,
                               LogSolicitacoesUsuario.DRE_NAO_VALIDOU],
            status__in=[PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_NEGOU_PEDIDO,
                        PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO,
                        PedidoAPartirDaEscolaWorkflow.DRE_NAO_VALIDOU_PEDIDO_ESCOLA, ],
            dre_uuid=dre_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_cancelados(cls, **kwargs):
        dre_uuid = kwargs.get('dre_uuid')
        return cls.objects.filter(
            status_evento__in=[LogSolicitacoesUsuario.DRE_CANCELOU,
                               LogSolicitacoesUsuario.ESCOLA_CANCELOU],
            status__in=[PedidoAPartirDaDiretoriaRegionalWorkflow.DRE_CANCELOU,
                        PedidoAPartirDaEscolaWorkflow.ESCOLA_CANCELOU],
            dre_uuid=dre_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')


class SolicitacoesTerceirizada(MoldeConsolidado):

    @classmethod
    def get_pendentes_autorizacao(cls, **kwargs):
        terceirizada_uuid = kwargs.get('terceirizada_uuid')
        return cls.objects.filter(
            status__in=[PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_A_AUTORIZAR,
                        PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO],
            status_evento__in=[LogSolicitacoesUsuario.DRE_VALIDOU,
                               LogSolicitacoesUsuario.INICIO_FLUXO],
            terceirizada_uuid=terceirizada_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_autorizados(cls, **kwargs):
        terceirizada_uuid = kwargs.get('terceirizada_uuid')
        return cls.objects.filter(
            status_evento__in=[LogSolicitacoesUsuario.CODAE_AUTORIZOU,
                               LogSolicitacoesUsuario.TERCEIRIZADA_TOMOU_CIENCIA],
            status__in=[PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO,
                        PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA],
            terceirizada_uuid=terceirizada_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_negados(cls, **kwargs):
        terceirizada_uuid = kwargs.get('terceirizada_uuid')
        return cls.objects.filter(
            status_evento=LogSolicitacoesUsuario.CODAE_NEGOU,
            status=PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO,
            terceirizada_uuid=terceirizada_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')

    @classmethod
    def get_cancelados(cls, **kwargs):
        terceirizada_uuid = kwargs.get('terceirizada_uuid')
        return cls.objects.filter(
            status_evento__in=[LogSolicitacoesUsuario.DRE_CANCELOU,
                               LogSolicitacoesUsuario.ESCOLA_CANCELOU],
            status__in=[PedidoAPartirDaEscolaWorkflow.ESCOLA_CANCELOU,
                        PedidoAPartirDaDiretoriaRegionalWorkflow.DRE_CANCELOU],
            terceirizada_uuid=terceirizada_uuid
        ).order_by('uuid', '-criado_em').distinct('uuid')
