from rest_framework import status


# TODO Encontrar forma de testar com autenticação no JWT
def test_url_endpoint_painel_dre(client):
    response = client.get('/dre-pendentes-aprovacao/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def base_codae(client_autenticado, resource):
    endpoint = f'/codae-solicitacoes/{resource}/'
    response = client_autenticado.get(endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_url_endpoint_painel_codae_pendentes_aprovacao(client_autenticado):
    base_codae(client_autenticado, 'pendentes-aprovacao')


def test_url_endpoint_painel_codae_aprovados(client_autenticado):
    base_codae(client_autenticado, 'aprovados')


def test_url_endpoint_painel_codae_cancelados(client_autenticado):
    base_codae(client_autenticado, 'cancelados')


def test_url_endpoint_painel_codae_solicitacoes_revisao(client_autenticado):
    base_codae(client_autenticado, 'solicitacoes-revisao')