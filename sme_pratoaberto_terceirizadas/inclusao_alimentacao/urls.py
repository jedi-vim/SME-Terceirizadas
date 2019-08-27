from django.urls import path, include
from rest_framework import routers

from .api import viewsets

router = routers.DefaultRouter()

router.register('motivos-inclusao-continua', viewsets.MotivoInclusaoContinuaViewSet,
                basename='motivo-inclusao-continua')
router.register('motivos-inclusao-normal', viewsets.MotivoInclusaoNormalViewSet,
                basename='motivo-inclusao-normal')
router.register('grupos-inclusao-alimentacao-normal', viewsets.GrupoInclusaoAlimentacaoNormalViewSet,
                basename='grupo-inclusao-alimentacao-normal')
router.register('inclusoes-alimentacao-continua', viewsets.InclusaoAlimentacaoContinuaViewSet,
                basename='inclusao-alimentacao-continua')

urlpatterns = [
    path('', include(router.urls))
]
