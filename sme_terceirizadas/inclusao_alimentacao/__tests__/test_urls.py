import pytest
from freezegun import freeze_time
from model_mommy import mommy
from rest_framework import status

from ...dados_comuns import constants
from ...dados_comuns.constants import (
    CODAE_AUTORIZA_PEDIDO,
    CODAE_NEGA_PEDIDO,
    CODAE_QUESTIONA_PEDIDO,
    DRE_INICIO_PEDIDO,
    DRE_NAO_VALIDA_PEDIDO,
    DRE_VALIDA_PEDIDO,
    ESCOLA_CANCELA,
    TERCEIRIZADA_RESPONDE_QUESTIONAMENTO,
    TERCEIRIZADA_TOMOU_CIENCIA
)
from ...dados_comuns.fluxo_status import PedidoAPartirDaEscolaWorkflow
from ..models import GrupoInclusaoAlimentacaoNormal, InclusaoAlimentacaoDaCEI

pytestmark = pytest.mark.django_db


def base_get_request(client_autenticado, resource):
    endpoint = f'/{resource}/'
    response = client_autenticado.get(endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_permissoes_grupo_inclusao_normal_viewset(client_autenticado_vinculo_escola_inclusao,
                                                  grupo_inclusao_alimentacao_normal,
                                                  grupo_inclusao_alimentacao_normal_outra_dre):
    # pode ver os dados de uma suspensão de alimentação da mesma escola
    response = client_autenticado_vinculo_escola_inclusao.get(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal.uuid}/'
    )
    assert response.status_code == status.HTTP_200_OK
    # Não pode ver dados de uma suspensão de alimentação de outra escola
    response = client_autenticado_vinculo_escola_inclusao.get(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_outra_dre.uuid}/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # não pode ver os dados de TODAS as suspensões de alimentação
    response = client_autenticado_vinculo_escola_inclusao.get(
        f'/grupos-inclusao-alimentacao-normal/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Você não tem permissão para executar essa ação.'}
    grupo_inclusao_alimentacao_normal.status = PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    grupo_inclusao_alimentacao_normal.save()
    response = client_autenticado_vinculo_escola_inclusao.delete(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal.uuid}/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Você só pode excluir quando o status for RASCUNHO.'}
    # pode deletar somente se for escola e se estiver como rascunho
    response = client_autenticado_vinculo_escola_inclusao.delete(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_outra_dre.uuid}/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    grupo_inclusao_alimentacao_normal.status = PedidoAPartirDaEscolaWorkflow.RASCUNHO
    grupo_inclusao_alimentacao_normal.save()
    response = client_autenticado_vinculo_escola_inclusao.delete(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal.uuid}/'
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_url_endpoint_grupos_inclusao_motivos_inclusao_normal(client_autenticado_vinculo_escola_inclusao):
    base_get_request(client_autenticado_vinculo_escola_inclusao, 'motivos-inclusao-normal')


def test_url_endpoint_grupos_inclusao_motivos_inclusao_continua(client_autenticado_vinculo_escola_inclusao):
    base_get_request(client_autenticado_vinculo_escola_inclusao, 'motivos-inclusao-continua')


def test_url_endpoint_inclusao_normal_inicio_fluxo(client_autenticado_vinculo_escola_inclusao,
                                                   grupo_inclusao_alimentacao_normal):
    assert grupo_inclusao_alimentacao_normal.status == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal.uuid}/{DRE_INICIO_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR


def test_url_endpoint_inclusao_normal_inicio_fluxo_erro(client_autenticado_vinculo_escola_inclusao,
                                                        grupo_inclusao_alimentacao_normal_dre_validar):
    assert grupo_inclusao_alimentacao_normal_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validar.uuid}/{DRE_INICIO_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'inicia_fluxo' isn't available from state 'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_normal_dre_valida(client_autenticado_vinculo_dre_inclusao,
                                                 grupo_inclusao_alimentacao_normal_dre_validar):
    assert grupo_inclusao_alimentacao_normal_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validar.uuid}/{DRE_VALIDA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO


def test_url_endpoint_inclusao_normal_dre_valida_erro(client_autenticado_vinculo_dre_inclusao,
                                                      grupo_inclusao_alimentacao_normal):
    assert grupo_inclusao_alimentacao_normal.status == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    assert GrupoInclusaoAlimentacaoNormal.get_solicitacoes_rascunho(
        grupo_inclusao_alimentacao_normal.criado_por).count() == 1
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal.uuid}/{DRE_VALIDA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'dre_valida' isn't available from state 'RASCUNHO'."}


def test_url_endpoint_inclusao_normal_dre_nao_valida(client_autenticado_vinculo_dre_inclusao,
                                                     grupo_inclusao_alimentacao_normal_dre_validar):
    assert grupo_inclusao_alimentacao_normal_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validar.uuid}/' +
        f'{DRE_NAO_VALIDA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.DRE_NAO_VALIDOU_PEDIDO_ESCOLA


def test_url_endpoint_inclusao_normal_dre_nao_valida_erro(client_autenticado_vinculo_dre_inclusao,
                                                          grupo_inclusao_alimentacao_normal):
    assert grupo_inclusao_alimentacao_normal.status == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal.uuid}/{DRE_NAO_VALIDA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'dre_nao_valida' isn't available from state 'RASCUNHO'."}


def test_url_endpoint_inclusao_normal_codae_autoriza(client_autenticado_vinculo_codae_inclusao,
                                                     grupo_inclusao_alimentacao_normal_dre_validado):
    assert grupo_inclusao_alimentacao_normal_dre_validado.status == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validado.uuid}/' +
        f'{CODAE_AUTORIZA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO


def test_url_endpoint_inclusao_normal_codae_autoriza_erro(client_autenticado_vinculo_codae_inclusao,
                                                          grupo_inclusao_alimentacao_normal_dre_validar):
    assert grupo_inclusao_alimentacao_normal_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validar.uuid}/' +
        f'{CODAE_AUTORIZA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'codae_autoriza_questionamento' isn't available from " +
                  f"state 'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_normal_codae_nega(client_autenticado_vinculo_codae_inclusao,
                                                 grupo_inclusao_alimentacao_normal_dre_validado):
    assert grupo_inclusao_alimentacao_normal_dre_validado.status == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validado.uuid}/' +
        f'{CODAE_NEGA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO


def test_url_endpoint_inclusao_normal_codae_nega_erro(client_autenticado_vinculo_codae_inclusao,
                                                      grupo_inclusao_alimentacao_normal_dre_validar):
    assert grupo_inclusao_alimentacao_normal_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validar.uuid}/' +
        f'{CODAE_NEGA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'codae_nega_questionamento' isn't available from state " +
                  f"'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_normal_codae_questiona(client_autenticado_vinculo_codae_inclusao,
                                                      grupo_inclusao_alimentacao_normal_dre_validado):
    assert grupo_inclusao_alimentacao_normal_dre_validado.status == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validado.uuid}/' +
        f'{CODAE_QUESTIONA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_QUESTIONADO


def test_url_endpoint_inclusao_normal_codae_questiona_erro(client_autenticado_vinculo_codae_inclusao,
                                                           grupo_inclusao_alimentacao_normal_dre_validar):
    assert grupo_inclusao_alimentacao_normal_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validar.uuid}/' +
        f'{CODAE_QUESTIONA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'codae_questiona' isn't available from state " +
                  f"'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_normal_terc_ciencia(client_autenticado_vinculo_terceirizada_inclusao,
                                                   grupo_inclusao_alimentacao_normal_codae_autorizado):
    assert grupo_inclusao_alimentacao_normal_codae_autorizado.status == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_codae_autorizado.uuid}/'
        f'{TERCEIRIZADA_TOMOU_CIENCIA}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA


def test_url_endpoint_inclusao_normal_relatorio(client_autenticado,
                                                grupo_inclusao_alimentacao_normal_codae_autorizado):
    response = client_autenticado.get(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_codae_autorizado.uuid}/'
        f'{constants.RELATORIO}/')
    id_externo = grupo_inclusao_alimentacao_normal_codae_autorizado.id_externo
    assert response.status_code == status.HTTP_200_OK
    assert response._headers['content-type'] == ('Content-Type', 'application/pdf')
    assert response._headers['content-disposition'] == (
        'Content-Disposition', f'filename="inclusao_alimentacao_{id_externo}.pdf"')
    assert 'PDF-1.5' in str(response.content)
    assert isinstance(response.content, bytes)


def test_url_endpoint_inclusao_normal_terc_ciencia_erro(client_autenticado_vinculo_terceirizada_inclusao,
                                                        grupo_inclusao_alimentacao_normal_dre_validar):
    assert grupo_inclusao_alimentacao_normal_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_dre_validar.uuid}/' +
        f'{TERCEIRIZADA_TOMOU_CIENCIA}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'terceirizada_toma_ciencia' isn't available from state " +
                  f"'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_normal_terc_responde_questionamento(client_autenticado_vinculo_terceirizada_inclusao,
                                                                   grupo_inclusao_alimentacao_normal_codae_questionado):
    assert grupo_inclusao_alimentacao_normal_codae_questionado.status == PedidoAPartirDaEscolaWorkflow.CODAE_QUESTIONADO
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_codae_questionado.uuid}/'
        f'{TERCEIRIZADA_RESPONDE_QUESTIONAMENTO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_codae_questionado.uuid}/' +
        f'{TERCEIRIZADA_RESPONDE_QUESTIONAMENTO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'terceirizada_responde_questionamento' isn't available " +
                  f"from state 'TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO'."}


@freeze_time('2018-12-01')
def test_url_endpoint_inclusao_normal_escola_cancela(client_autenticado_vinculo_escola_inclusao,
                                                     grupo_inclusao_alimentacao_normal_codae_autorizado):
    assert grupo_inclusao_alimentacao_normal_codae_autorizado.status == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_codae_autorizado.uuid}/'
        f'{ESCOLA_CANCELA}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.ESCOLA_CANCELOU
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/grupos-inclusao-alimentacao-normal/{grupo_inclusao_alimentacao_normal_codae_autorizado.uuid}/'
        f'{ESCOLA_CANCELA}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Erro de transição de estado: Já está cancelada'}


def test_permissoes_grupo_inclusao_continua_viewset(client_autenticado_vinculo_escola_inclusao,
                                                    inclusao_alimentacao_continua,
                                                    inclusao_alimentacao_continua_outra_dre):
    # pode ver os dados de uma suspensão de alimentação da mesma escola
    response = client_autenticado_vinculo_escola_inclusao.get(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua.uuid}/'
    )
    assert response.status_code == status.HTTP_200_OK
    # Não pode ver dados de uma suspensão de alimentação de outra escola
    response = client_autenticado_vinculo_escola_inclusao.get(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_outra_dre.uuid}/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # não pode ver os dados de TODAS as suspensões de alimentação
    response = client_autenticado_vinculo_escola_inclusao.get(
        f'/inclusoes-alimentacao-continua/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Você não tem permissão para executar essa ação.'}
    inclusao_alimentacao_continua.status = PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    inclusao_alimentacao_continua.save()
    response = client_autenticado_vinculo_escola_inclusao.delete(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua.uuid}/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Você só pode excluir quando o status for RASCUNHO.'}
    # pode deletar somente se for escola e se estiver como rascunho
    response = client_autenticado_vinculo_escola_inclusao.delete(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_outra_dre.uuid}/'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    inclusao_alimentacao_continua.status = PedidoAPartirDaEscolaWorkflow.RASCUNHO
    inclusao_alimentacao_continua.save()
    response = client_autenticado_vinculo_escola_inclusao.delete(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua.uuid}/'
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_url_endpoint_inclusao_continua_inicio_fluxo(client_autenticado_vinculo_escola_inclusao,
                                                     inclusao_alimentacao_continua):
    assert inclusao_alimentacao_continua.status == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua.uuid}/{DRE_INICIO_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR


def test_url_endpoint_inclusao_continua_inicio_fluxo_erro(client_autenticado_vinculo_escola_inclusao,
                                                          inclusao_alimentacao_continua_dre_validar):
    assert inclusao_alimentacao_continua_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validar.uuid}/{DRE_INICIO_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'inicia_fluxo' isn't available from state 'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_continua_dre_valida(client_autenticado_vinculo_dre_inclusao,
                                                   inclusao_alimentacao_continua_dre_validar):
    assert inclusao_alimentacao_continua_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validar.uuid}/{DRE_VALIDA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO


def test_url_endpoint_inclusao_continua_dre_valida_erro(client_autenticado_vinculo_dre_inclusao,
                                                        inclusao_alimentacao_continua):
    assert inclusao_alimentacao_continua.status == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua.uuid}/{DRE_VALIDA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'dre_valida' isn't available from state 'RASCUNHO'."}


def test_url_endpoint_inclusao_continua_dre_nao_valida(client_autenticado_vinculo_dre_inclusao,
                                                       inclusao_alimentacao_continua_dre_validar):
    assert inclusao_alimentacao_continua_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validar.uuid}/{DRE_NAO_VALIDA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.DRE_NAO_VALIDOU_PEDIDO_ESCOLA


def test_url_endpoint_inclusao_continua_dre_nao_valida_erro(client_autenticado_vinculo_dre_inclusao,
                                                            inclusao_alimentacao_continua_dre_validado):
    assert inclusao_alimentacao_continua_dre_validado.status == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado_vinculo_dre_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validado.uuid}/{DRE_NAO_VALIDA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'dre_nao_valida' isn't available from state 'DRE_VALIDADO'."}


def test_url_endpoint_inclusao_continua_codae_autoriza(client_autenticado_vinculo_codae_inclusao,
                                                       inclusao_alimentacao_continua_dre_validado):
    assert inclusao_alimentacao_continua_dre_validado.status == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validado.uuid}/{CODAE_AUTORIZA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO


def test_url_endpoint_inclusao_continua_codae_autoriza_erro(client_autenticado_vinculo_codae_inclusao,
                                                            inclusao_alimentacao_continua_dre_validar):
    assert inclusao_alimentacao_continua_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validar.uuid}/{CODAE_AUTORIZA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'codae_autoriza_questionamento' isn't available from " +
                  f"state 'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_continua_codae_nega(client_autenticado_vinculo_codae_inclusao,
                                                   inclusao_alimentacao_continua_dre_validado):
    assert inclusao_alimentacao_continua_dre_validado.status == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validado.uuid}/{CODAE_NEGA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO


def test_url_endpoint_inclusao_continua_codae_nega_erro(client_autenticado_vinculo_codae_inclusao,
                                                        inclusao_alimentacao_continua_dre_validar):
    assert inclusao_alimentacao_continua_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validar.uuid}/{CODAE_NEGA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'codae_nega_questionamento' isn't available from state " +
                  f"'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_continua_codae_questiona(client_autenticado_vinculo_codae_inclusao,
                                                        inclusao_alimentacao_continua_dre_validado):
    assert inclusao_alimentacao_continua_dre_validado.status == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validado.uuid}/{CODAE_QUESTIONA_PEDIDO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_QUESTIONADO


def test_url_endpoint_inclusao_continua_codae_questiona_erro(client_autenticado_vinculo_codae_inclusao,
                                                             inclusao_alimentacao_continua_dre_validar):
    assert inclusao_alimentacao_continua_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_codae_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validar.uuid}/{CODAE_QUESTIONA_PEDIDO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'codae_questiona' isn't available from state " +
                  f"'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_continua_terc_ciencia(client_autenticado_vinculo_terceirizada_inclusao,
                                                     inclusao_alimentacao_continua_codae_autorizado):
    assert inclusao_alimentacao_continua_codae_autorizado.status == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_codae_autorizado.uuid}/'
        f'{TERCEIRIZADA_TOMOU_CIENCIA}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA


def test_url_endpoint_inclusao_continua_terc_ciencia_erro(client_autenticado_vinculo_terceirizada_inclusao,
                                                          inclusao_alimentacao_continua_dre_validar):
    assert inclusao_alimentacao_continua_dre_validar.status == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_dre_validar.uuid}/' +
        f'{TERCEIRIZADA_TOMOU_CIENCIA}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'terceirizada_toma_ciencia' isn't available from state " +
                  f"'DRE_A_VALIDAR'."}


def test_url_endpoint_inclusao_continua_terc_responde_questionamento(client_autenticado_vinculo_terceirizada_inclusao,
                                                                     inclusao_alimentacao_continua_codae_questionado):
    assert inclusao_alimentacao_continua_codae_questionado.status == PedidoAPartirDaEscolaWorkflow.CODAE_QUESTIONADO
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_codae_questionado.uuid}/'
        f'{TERCEIRIZADA_RESPONDE_QUESTIONAMENTO}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO
    response = client_autenticado_vinculo_terceirizada_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_codae_questionado.uuid}/'
        f'{TERCEIRIZADA_RESPONDE_QUESTIONAMENTO}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'terceirizada_responde_questionamento' isn't available " +
                  f"from state 'TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO'."}


@freeze_time('2018-12-01')
def test_url_endpoint_inclusao_continua_escola_cancela(client_autenticado_vinculo_escola_inclusao,
                                                       inclusao_alimentacao_continua_codae_autorizado):
    assert inclusao_alimentacao_continua_codae_autorizado.status == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_codae_autorizado.uuid}/'
        f'{ESCOLA_CANCELA}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == PedidoAPartirDaEscolaWorkflow.ESCOLA_CANCELOU
    response = client_autenticado_vinculo_escola_inclusao.patch(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_codae_autorizado.uuid}/'
        f'{ESCOLA_CANCELA}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Erro de transição de estado: Já está cancelada'}


def test_url_endpoint_inclusao_continua_relatorio(client_autenticado,
                                                  inclusao_alimentacao_continua_codae_autorizado):
    response = client_autenticado.get(
        f'/inclusoes-alimentacao-continua/{inclusao_alimentacao_continua_codae_autorizado.uuid}/'
        f'{constants.RELATORIO}/')
    id_externo = inclusao_alimentacao_continua_codae_autorizado.id_externo
    assert response.status_code == status.HTTP_200_OK
    assert response._headers['content-type'] == ('Content-Type', 'application/pdf')
    assert response._headers['content-disposition'] == (
        'Content-Disposition', f'filename="inclusao_alimentacao_continua_{id_externo}.pdf"')
    assert 'PDF-1.5' in str(response.content)
    assert isinstance(response.content, bytes)


def test_url_endpoint_inclusao_cei_relatorio(client_autenticado_vinculo_escola_cei_inclusao):
    inclusao_alimentacao = mommy.make(InclusaoAlimentacaoDaCEI)
    response = client_autenticado_vinculo_escola_cei_inclusao.get(
        f'/inclusoes-alimentacao-da-cei/{inclusao_alimentacao.uuid}/{constants.RELATORIO}/')
    id_externo = inclusao_alimentacao.id_externo
    assert response.status_code == status.HTTP_200_OK
    assert response._headers['content-type'] == ('Content-Type', 'application/pdf')
    assert response._headers['content-disposition'] == (
        'Content-Disposition', f'filename="inclusao_alimentacao_{id_externo}.pdf"')
    assert 'PDF-1.5' in str(response.content)
    assert isinstance(response.content, bytes)
