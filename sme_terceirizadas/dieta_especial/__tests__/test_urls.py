import base64

from rest_framework import status

from ...dados_comuns.fluxo_status import DietaEspecialWorkflow
from ..constants import (
    ENDPOINT_ALERGIAS_INTOLERANCIAS,
    ENDPOINT_CLASSIFICACOES_DIETA,
    ENDPOINT_MOTIVOS_NEGACAO,
    ENDPOINT_TIPOS_DIETA_ESPECIAL
)
from ..models import AlergiaIntolerancia, Anexo, ClassificacaoDieta, MotivoNegacao, SolicitacaoDietaEspecial, TipoDieta


def endpoint_lista(client_autenticado, endpoint, quantidade):
    response = client_autenticado.get(f'/{endpoint}/')
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json) == quantidade


def test_url_endpoint_lista_alergias_intolerancias(client_autenticado,
                                                   alergias_intolerancias):
    endpoint_lista(
        client_autenticado,
        ENDPOINT_ALERGIAS_INTOLERANCIAS,
        quantidade=2
    )


def test_url_endpoint_lista_classificacoes_dieta(client_autenticado,
                                                 classificacoes_dieta):
    endpoint_lista(
        client_autenticado,
        ENDPOINT_CLASSIFICACOES_DIETA,
        quantidade=3
    )


def test_url_endpoint_lista_motivos_negacao(client_autenticado,
                                            motivos_negacao):
    endpoint_lista(
        client_autenticado,
        ENDPOINT_MOTIVOS_NEGACAO,
        quantidade=4
    )


def test_url_endpoint_lista_tipos_dieta(client_autenticado,
                                        tipos_dieta):
    endpoint_lista(
        client_autenticado,
        ENDPOINT_TIPOS_DIETA_ESPECIAL,
        quantidade=5
    )


def endpoint_detalhe(client_autenticado, endpoint, modelo, tem_nome=False):
    obj = modelo.objects.first()
    response = client_autenticado.get(f'/{endpoint}/{obj.id}/')
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert obj.descricao == json['descricao']
    if tem_nome:
        assert obj.nome == json['nome']


def test_url_endpoint_detalhe_alergias_intolerancias(client_autenticado,
                                                     alergias_intolerancias):
    endpoint_detalhe(
        client_autenticado,
        ENDPOINT_ALERGIAS_INTOLERANCIAS,
        AlergiaIntolerancia
    )


def test_url_endpoint_detalhe_classificacoes_dieta(client_autenticado,
                                                   classificacoes_dieta):
    endpoint_detalhe(
        client_autenticado,
        ENDPOINT_CLASSIFICACOES_DIETA,
        ClassificacaoDieta,
        tem_nome=True
    )


def test_url_endpoint_detalhe_motivos_negacao(client_autenticado,
                                              motivos_negacao):
    endpoint_detalhe(
        client_autenticado,
        ENDPOINT_MOTIVOS_NEGACAO,
        MotivoNegacao
    )


def test_url_endpoint_detalhe_tipos_dieta(client_autenticado,
                                          tipos_dieta):
    endpoint_detalhe(
        client_autenticado,
        ENDPOINT_TIPOS_DIETA_ESPECIAL,
        TipoDieta
    )


def test_url_criar_dieta(client_autenticado_vinculo_escola):
    payload = {'observacoes': '<p>dsadsadasd</p>\n',
               'aluno_json': {
                   'codigo_eol': '6',
                   'nome': 'ADRIANO RIBEIRO MINANTE',
                   'data_nascimento': '01/07/1982'
               },
               'nome_completo_pescritor': 'fffdasdasdasd',
               'registro_funcional_pescritor': 'aasddd',
               'anexos': [{
                   'arquivo': 'data:image/png;base64,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',  # noqa
                   'nome': 'Captura de tela de 2020-01-16 10-17-02.png'}]
               }
    response = client_autenticado_vinculo_escola.post(
        f'/solicitacoes-dieta-especial/',
        content_type='application/json',
        data=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = client_autenticado_vinculo_escola.post(
        f'/solicitacoes-dieta-especial/',
        content_type='application/json',
        data=payload
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == ['Aluno já possui Solicitação de Dieta Especial pendente']


def test_url_criar_dieta_erro_sem_anexos(client_autenticado_vinculo_escola):
    payload = {'observacoes': '<p>dsadsadasd</p>\n',
               'aluno_json': {
                   'codigo_eol': '6',
                   'nome': 'ADRIANO RIBEIRO MINANTE',
                   'data_nascimento': '01/07/1982'
               },
               'nome_completo_pescritor': 'fffdasdasdasd',
               'registro_funcional_pescritor': 'aasddd',
               'anexos': []
               }
    response = client_autenticado_vinculo_escola.post(
        f'/solicitacoes-dieta-especial/',
        content_type='application/json',
        data=payload
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'anexos': ['Anexos não pode ser vazio']}


def test_url_criar_dieta_erro_anexo_muito_grande(client_autenticado_vinculo_escola):
    with open('sme_terceirizadas/static/files/teste_tamanho.pdf', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
    payload = {'observacoes': '<p>dsadsadasd</p>\n',
               'aluno_json': {
                   'codigo_eol': '6',
                   'nome': 'ADRIANO RIBEIRO MINANTE',
                   'data_nascimento': '01/07/1982'
               },
               'nome_completo_pescritor': 'fffdasdasdasd',
               'registro_funcional_pescritor': 'aasddd',
               'anexos': [{
                   'arquivo': 'data:application/pdf;base64,' + encoded_string.decode('utf-8'),
                   'nome': 'oi.pdf'}]
               }
    response = client_autenticado_vinculo_escola.post(
        f'/solicitacoes-dieta-especial/',
        content_type='application/json',
        data=payload
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'anexos': ['O tamanho máximo de um arquivo é 10MB']}


def test_url_criar_dieta_erro_aluno_falta_atributo(client_autenticado_vinculo_escola):
    payload = {'observacoes': '<p>dsadsadasd</p>\n',
               'aluno_json': {
                   'nome': 'ADRIANO RIBEIRO MINANTE',
                   'data_nascimento': '01/07/1982'
               },
               'nome_completo_pescritor': 'fffdasdasdasd',
               'registro_funcional_pescritor': 'aasddd',
               'anexos': [{
                   'arquivo': 'data:image/png;base64,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',  # noqa
                   'nome': 'oi.pdf'}]
               }
    response = client_autenticado_vinculo_escola.post(
        f'/solicitacoes-dieta-especial/',
        content_type='application/json',
        data=payload
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'aluno_json': [f'deve ter atributo codigo_eol']}


def test_url_endpoint_autorizar_dieta(client_autenticado,
                                      solicitacao_dieta_especial_a_autorizar,
                                      alergias_intolerancias,
                                      classificacoes_dieta):
    obj = SolicitacaoDietaEspecial.objects.first()
    data = {
        'classificacao': classificacoes_dieta[0].id,
        'alergias_intolerancias': [
            alergias_intolerancias[0].id
        ],
        'registro_funcional_nutricionista':
            'ELABORADO por USUARIO NUTRICIONISTA CODAE - CRN null',
        'protocolos': [
            {
                'nome': 'Teste',
                'base64': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAaQAAAGkCAIAAADxLsZiAAAFyklEQVR4nOzWUZHbYBA' +
                          'GwThlHsYmEEIhEMImBgshJHL6rZtuAvs9Te17Zv4A/HZ/Vw8AuIPYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgB' +
                          'CWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJY' +
                          'gckiB2QIHZAgtgBCe/VAx7svI7VEyjaPvvqCY/kswMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7I' +
                          'AEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgAS' +
                          'xAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLED' +
                          'EsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxJeM3PPpfM67jkEPMv22' +
                          'W+44rMDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7I' +
                          'AEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgAS' +
                          'xAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLED' +
                          'EsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IeM3M6g1PdV7H6gkUbZ999YRH8tkBCWIHJIgdkCB2QILYAQliB' +
                          'ySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJI' +
                          'gdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2' +
                          'QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAg' +
                          'dkCC2AEJr5lZvQHgx/nsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7' +
                          'IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgA' +
                          'SxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLE' +
                          'DEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsg4b16AF/kvI7VE/6/7bOvnsBX8NkBCWIHJIgdkCB2QILY' +
                          'AQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBC' +
                          'WIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYg' +
                          'ckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliByS' +
                          'IHZAgdkCC2AEJYgckvGZm9QaAH+ezAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQ' +
                          'OyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEv4FAAD//' +
                          'xmNHVuA/EwlAAAAAElFTkSuQmCC'
            }
        ]
    }
    response = client_autenticado.post(
        f'/solicitacoes-dieta-especial/{obj.uuid}/autorizar/',
        content_type='application/json',
        data=data
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['mensagem'] == 'Autorização de dieta especial realizada com sucesso'

    obj.refresh_from_db()

    assert obj.status == DietaEspecialWorkflow.CODAE_AUTORIZADO
    assert obj.registro_funcional_nutricionista == data['registro_funcional_nutricionista']
    for ai in obj.alergias_intolerancias.all():
        assert ai.id in data['alergias_intolerancias']
    assert obj.classificacao.id == data['classificacao']

    anexos = Anexo.objects.filter(solicitacao_dieta_especial=obj)
    assert anexos.count() == 1

    anexo = anexos.first()
    assert anexo.nome == data['protocolos'][0]['nome']


def test_url_endpoint_negar_dieta(client_autenticado,
                                  solicitacao_dieta_especial_a_autorizar,
                                  motivos_negacao):
    obj = SolicitacaoDietaEspecial.objects.first()
    data = {
        'justificativa_negacao': 'Uma justificativa fajuta',
        'motivo_negacao': motivos_negacao[0].id,
        'registro_funcional_nutricionista':
            'ELABORADO por USUARIO NUTRICIONISTA CODAE - CRN null'
    }
    response = client_autenticado.post(
        f'/solicitacoes-dieta-especial/{obj.uuid}/negar/',
        content_type='application/json',
        data=data
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['mensagem'] == 'Solicitação de Dieta Especial Negada'

    obj.refresh_from_db()

    assert obj.status == DietaEspecialWorkflow.CODAE_NEGOU_PEDIDO
    assert obj.justificativa_negacao == data['justificativa_negacao']
    assert obj.motivo_negacao.id == data['motivo_negacao']
    assert obj.registro_funcional_nutricionista == data['registro_funcional_nutricionista']


def test_url_endpoint_tomar_ciencia_dieta(client_autenticado,
                                          solicitacao_dieta_especial_autorizada):
    obj = SolicitacaoDietaEspecial.objects.first()
    response = client_autenticado.post(
        f'/solicitacoes-dieta-especial/{obj.uuid}/tomar_ciencia/',
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['mensagem'] == 'Ciente da solicitação de dieta especial'

    obj.refresh_from_db()

    assert obj.status == DietaEspecialWorkflow.TERCEIRIZADA_TOMOU_CIENCIA


def test_url_endpoint_escola_solicita_inativacao_dieta(client_autenticado,
                                                       solicitacao_dieta_especial_autorizada):
    obj = SolicitacaoDietaEspecial.objects.first()
    data = {
        'justificativa': '<p>alta pelo médico</p>',
        'anexos': []
    }
    response = client_autenticado.patch(
        f'/solicitacoes-dieta-especial/{obj.uuid}/escola-solicita-inativacao/',
        content_type='application/json',
        data=data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': f'anexos não pode ser vazio'}
    data = {
        'justificativa':
            '<p>alta pelo médico</p>',
        'anexos': [
            {
                'nome': 'Teste',
                'arquivo': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAaQAAAGkCAIAAADxLsZiAAAFyklEQVR4nOzWUZHbYBA' +
                           'GwThlHsYmEEIhEMImBgshJHL6rZtuAvs9Te17Zv4A/HZ/Vw8AuIPYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgB' +
                           'CWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJY' +
                           'gckiB2QIHZAgtgBCe/VAx7svI7VEyjaPvvqCY/kswMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7I' +
                           'AEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgAS' +
                           'xAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLED' +
                           'EsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxJeM3PPpfM67jkEPMv22' +
                           'W+44rMDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7I' +
                           'AEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgAS' +
                           'xAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLED' +
                           'EsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IeM3M6g1PdV7H6gkUbZ999YRH8tkBCWIHJIgdkCB2QILYAQliB' +
                           'ySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJI' +
                           'gdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2' +
                           'QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAg' +
                           'dkCC2AEJr5lZvQHgx/nsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7' +
                           'IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgA' +
                           'SxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLE' +
                           'DEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsg4b16AF/kvI7VE/6/7bOvnsBX8NkBCWIHJIgdkCB2QILY' +
                           'AQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBC' +
                           'WIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYg' +
                           'ckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliBySIHZAgdkCC2AEJYgckiB2QIHZAgtgBCWIHJIgdkCB2QILYAQliByS' +
                           'IHZAgdkCC2AEJYgckvGZm9QaAH+ezAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQ' +
                           'OyBB7IAEsQMSxA5IEDsgQeyABLEDEsQOSBA7IEHsgASxAxLEDkgQOyBB7IAEsQMSxA5IEDsgQeyABLEDEv4FAAD//' +
                           'xmNHVuA/EwlAAAAAElFTkSuQmCC'
            }
        ]
    }
    response = client_autenticado.patch(
        f'/solicitacoes-dieta-especial/{obj.uuid}/escola-solicita-inativacao/',
        content_type='application/json',
        data=data
    )

    assert response.status_code == status.HTTP_200_OK
    obj.refresh_from_db()
    assert obj.status == DietaEspecialWorkflow.ESCOLA_SOLICITOU_INATIVACAO
    response = client_autenticado.patch(
        f'/solicitacoes-dieta-especial/{obj.uuid}/escola-solicita-inativacao/',
        content_type='application/json',
        data=data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'inicia_fluxo_inativacao' isn't available from state " +
                  "'ESCOLA_SOLICITOU_INATIVACAO'."}


def test_url_endpoint_codae_autoriza_inativacao_dieta(client_autenticado,
                                                      solicitacao_dieta_especial_escola_solicitou_inativacao):
    obj = SolicitacaoDietaEspecial.objects.first()
    response = client_autenticado.patch(
        f'/solicitacoes-dieta-especial/{obj.uuid}/codae-autoriza-inativacao/',
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_200_OK
    obj.refresh_from_db()
    assert obj.status == DietaEspecialWorkflow.CODAE_AUTORIZOU_INATIVACAO
    response = client_autenticado.patch(
        f'/solicitacoes-dieta-especial/{obj.uuid}/codae-autoriza-inativacao/',
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': f"Erro de transição de estado: Transition 'codae_autoriza_inativacao' isn't available from state " +
                  "'CODAE_AUTORIZOU_INATIVACAO'."}
