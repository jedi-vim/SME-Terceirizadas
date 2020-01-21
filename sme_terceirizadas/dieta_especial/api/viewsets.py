from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ...dados_comuns import constants
from ...dados_comuns.utils import convert_base64_to_contentfile
from ...relatorios.relatorios import relatorio_dieta_especial
from ..forms import AutorizaDietaEspecialForm, NegaDietaEspecialForm
from ..models import AlergiaIntolerancia, Anexo, ClassificacaoDieta, MotivoNegacao, SolicitacaoDietaEspecial, TipoDieta
from .serializers import (
    AlergiaIntoleranciaSerializer,
    ClassificacaoDietaSerializer,
    MotivoNegacaoSerializer,
    SolicitacaoDietaEspecialCreateSerializer,
    SolicitacaoDietaEspecialSerializer,
    TipoDietaSerializer
)


class SolicitacaoDietaEspecialViewSet(mixins.RetrieveModelMixin,
                                      mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      GenericViewSet):
    lookup_field = 'uuid'
    queryset = SolicitacaoDietaEspecial.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SolicitacaoDietaEspecialCreateSerializer
        return SolicitacaoDietaEspecialSerializer

    @action(detail=True, methods=['post'])
    def autorizar(self, request, uuid=None):
        solicitacao = self.get_object()
        form = AutorizaDietaEspecialForm(request.data, instance=solicitacao)

        if not form.is_valid():
            return Response(form.errors)

        form.save()

        for p in request.data['protocolos']:
            data = convert_base64_to_contentfile(p.get('base64'))
            Anexo.objects.create(
                solicitacao_dieta_especial=solicitacao, arquivo=data, nome=p.get('nome', ''), eh_laudo_medico=False
            )

        solicitacao.codae_autoriza(user=request.user)

        solicitacao.save()

        return Response({'mensagem': 'Autorização de dieta especial realizada com sucesso'})

    @action(detail=True, methods=['post'])
    def negar(self, request, uuid=None):
        solicitacao = self.get_object()
        form = NegaDietaEspecialForm(request.data, instance=solicitacao)

        if not form.is_valid():
            return Response(form.errors)

        solicitacao.codae_nega(user=request.user)

        return Response({'mensagem': 'Solicitação de Dieta Especial Negada'})

    @action(detail=True, methods=['post'])
    def tomar_ciencia(self, request, uuid=None):
        solicitacao = self.get_object()

        solicitacao.terceirizada_toma_ciencia(user=request.user)

        return Response({'mensagem': 'Ciente da solicitação de dieta especial'})

    @action(detail=True, url_path=constants.RELATORIO,
            methods=['get'])
    def relatorio(self, request, uuid=None):
        return relatorio_dieta_especial(request, solicitacao=self.get_object())


class AlergiaIntoleranciaViewSet(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 GenericViewSet):
    queryset = AlergiaIntolerancia.objects.all()
    serializer_class = AlergiaIntoleranciaSerializer
    pagination_class = None


class ClassificacaoDietaViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                GenericViewSet):
    queryset = ClassificacaoDieta.objects.all()
    serializer_class = ClassificacaoDietaSerializer
    pagination_class = None


class MotivoNegacaoViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           GenericViewSet):
    queryset = MotivoNegacao.objects.all()
    serializer_class = MotivoNegacaoSerializer
    pagination_class = None


class TipoDietaViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = TipoDieta.objects.all()
    serializer_class = TipoDietaSerializer
    pagination_class = None
