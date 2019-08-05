from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from xworkflows import InvalidTransitionError

from sme_pratoaberto_terceirizadas.cardapio.api.serializers.serializers import MotivoSuspensaoSerializer
from .permissions import (
    PodeIniciarAlteracaoCardapioPermission
)
from .serializers.serializers import (
    CardapioSerializer, TipoAlimentacaoSerializer,
    InversaoCardapioSerializer, AlteracaoCardapioSerializer,
    GrupoSuspensaoAlimentacaoSerializer)
from .serializers.serializers import MotivoAlteracaoCardapioSerializer
from .serializers.serializers_create import (
    InversaoCardapioSerializerCreate, CardapioCreateSerializer,
    AlteracaoCardapioSerializerCreate,
    GrupoSuspensaoAlimentacaoCreateSerializer)
from ..models import (
    Cardapio, TipoAlimentacao, InversaoCardapio,
    AlteracaoCardapio, GrupoSuspensaoAlimentacao, MotivoSuspensao
)
from ..models import MotivoAlteracaoCardapio


class CardapioViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = CardapioSerializer
    queryset = Cardapio.objects.all().order_by('data')

    # TODO: permitir deletar somente se o status for do inicial...
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CardapioCreateSerializer
        return CardapioSerializer


class TipoAlimentacaoViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = TipoAlimentacaoSerializer
    queryset = TipoAlimentacao.objects.all()


class InversaoCardapioViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = InversaoCardapio.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InversaoCardapioSerializerCreate
        return InversaoCardapioSerializer


class GrupoSuspensaoAlimentacaoSerializerViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = GrupoSuspensaoAlimentacao.objects.all()
    serializer_class = GrupoSuspensaoAlimentacaoSerializer

    @action(detail=False)
    def meus_rascunhos(self, request):
        usuario = request.user
        grupos_suspensao = GrupoSuspensaoAlimentacao.objects.filter(
            criado_por=usuario,
            status=GrupoSuspensaoAlimentacao.workflow_class.RASCUNHO
        )
        page = self.paginate_queryset(grupos_suspensao)
        serializer = GrupoSuspensaoAlimentacaoSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GrupoSuspensaoAlimentacaoCreateSerializer
        return GrupoSuspensaoAlimentacaoSerializer


class AlteracoesCardapioViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = AlteracaoCardapio.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AlteracaoCardapioSerializerCreate
        return AlteracaoCardapioSerializer

    @action(detail=True, permission_classes=[PodeIniciarAlteracaoCardapioPermission], methods=['patch'])
    def inicio_de_pedido(self, request, uuid=None):
        alimentacao_normal = self.get_object()
        try:
            alimentacao_normal.inicia_fluxo(user=request.user)
            serializer = self.get_serializer(alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))


class MotivosAlteracaoCardapioViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    queryset = MotivoAlteracaoCardapio.objects.all()
    serializer_class = MotivoAlteracaoCardapioSerializer


class AlteracoesCardapioRascunhoViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    queryset = AlteracaoCardapio.objects.filter(status="RASCUNHO")
    serializer_class = AlteracaoCardapioSerializer


class MotivosSuspensaoCardapioViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    queryset = MotivoSuspensao.objects.all()
    serializer_class = MotivoSuspensaoSerializer
