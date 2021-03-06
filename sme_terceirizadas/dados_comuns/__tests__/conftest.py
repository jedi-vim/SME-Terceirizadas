import datetime

import pytest
from faker import Faker
from model_mommy import mommy

from ...escola import models
from ..models import TemplateMensagem

fake = Faker('pt_BR')
fake.seed(420)


@pytest.fixture(scope='function', params=[
    # dia, dias antecedencia, esperado
    # dia fake do teste: "2019-05-22"
    (datetime.date(2019, 5, 27), 2, True),
    (datetime.date(2019, 5, 25), 2, True),
    (datetime.date(2019, 5, 30), 5, True),
    (datetime.date(2019, 5, 28), 3, True),
])
def dias_teste_antecedencia(request):
    return request.param


@pytest.fixture(scope='function', params=[
    # dia, dias antecedencia, esperado
    # dia fake do teste: "2019-05-22"
    (datetime.date(2019, 5, 27), 5, 'Deve pedir com pelo menos 5 dias úteis de antecedência'),
    (datetime.date(2019, 5, 28), 5, 'Deve pedir com pelo menos 5 dias úteis de antecedência'),
    (datetime.date(2019, 5, 23), 2, 'Deve pedir com pelo menos 2 dias úteis de antecedência'),
    (datetime.date(2019, 5, 21), 2, 'Deve pedir com pelo menos 2 dias úteis de antecedência'),
])
def dias_teste_antecedencia_erro(request):
    return request.param


@pytest.fixture(scope='function', params=[
    # dia, esperado
    (datetime.date(2019, 12, 23), True),
    (datetime.date(2019, 12, 24), True),
    (datetime.date(2019, 12, 26), True),
    (datetime.date(2019, 12, 27), True),

])
def dias_uteis(request):
    return request.param


esperado = 'Não é dia útil em São Paulo'


@pytest.fixture(scope='function', params=[
    # dia, esperado
    (datetime.date(2019, 12, 25), esperado),  # natal
    (datetime.date(2019, 1, 1), esperado),  # ano novo
    (datetime.date(2019, 7, 9), esperado),  # Revolução Constitucionalista
    (datetime.date(2019, 9, 7), esperado),  # independencia
    (datetime.date(2019, 1, 25), esperado),  # aniversario sp

])
def dias_nao_uteis(request):
    return request.param


@pytest.fixture(scope='function', params=[
    # dia,  esperado
    # dia fake do teste: "2019-05-22"
    (datetime.date(2019, 5, 22), True),
    (datetime.date(2019, 5, 27), True),
    (datetime.date(2019, 5, 28), True),
    (datetime.date(2019, 5, 23), True),
])
def dias_futuros(request):
    return request.param


dia_passado_esperado = 'Não pode ser no passado'


@pytest.fixture(scope='function', params=[
    # dia,  esperado
    # dia fake do teste: "2019-05-22"
    (datetime.date(2019, 5, 21), dia_passado_esperado),
    (datetime.date(2019, 5, 20), dia_passado_esperado),
    (datetime.date(2018, 12, 12), dia_passado_esperado),
])
def dias_passados(request):
    return request.param


@pytest.fixture(scope='function', params=[
    # dia,  esperado
    # dia fake do teste: "2019-07-10" -> qua
    (2, datetime.date(2019, 7, 12)),  # sex
    (3, datetime.date(2019, 7, 15)),  # seg
    (5, datetime.date(2019, 7, 17)),  # qua
])
def dias_uteis_apos(request):
    return request.param


@pytest.fixture(scope='function', params=[
    # model-params-dict, esperado
    (
        {'_model': 'TemplateMensagem',
         'assunto': 'Inversão de cardápio',
         'template_html': '<p><span style="color: rgb(133,135,150);background-color:'
                          ' rgb(255,255,255);font-size: 16px;">Ola @nome, a Inversão de'
                          ' cardápio #@id pedida por @criado_por está em @status. '
                          'Acesse: @link</span></p>'
         },
        '<p><span style="color: rgb(133,135,150);background-color:'
        ' rgb(255,255,255);font-size: 16px;">Ola fulano, a Inversão de'
        ' cardápio #FAKE_id_externo pedida por FAKE_criado_por está em FAKE_status. '
        'Acesse: http:teste.com</span></p>'
    ),
])
def template_mensagem(request):
    return request.param


@pytest.fixture
def template_mensagem_obj():
    return mommy.make(TemplateMensagem, tipo=TemplateMensagem.ALTERACAO_CARDAPIO)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def validators_models_object():
    return mommy.make('dados_comuns.TemplateMensagem', assunto='TESTE')


@pytest.fixture
def validators_valor_str():
    return {
        'texto': 'Nome',
        'none': None
    }


@pytest.fixture
def escola():
    return mommy.make(models.Escola,
                      nome=fake.name(),
                      codigo_eol=fake.name()[:6])


@pytest.fixture(scope='function', params=[
    # dia do cardápio
    (datetime.date(2019, 5, 18)),
    (datetime.date(2019, 5, 19)),
    (datetime.date(2019, 5, 25)),
    (datetime.date(2019, 5, 26)),
    (datetime.date(2018, 6, 1)),
])
def dias_sem_cardapio(request):
    return request.param


@pytest.fixture(params=[
    (datetime.date(datetime.datetime.now().year - 1, 5, 26),
     'Inversão de dia de cardapio deve ser solicitada no ano corrente'),
    (datetime.date(datetime.datetime.now().year + 1, 1, 1),
     'Inversão de dia de cardapio deve ser solicitada no ano corrente'),
    (datetime.date(datetime.datetime.now().year + 2, 12, 1),
     'Inversão de dia de cardapio deve ser solicitada no ano corrente')
])
def data_inversao_ano_diferente(request):
    return request.param


@pytest.fixture(params=[
    (datetime.date(2019, 5, 26), True),
    (datetime.date(2019, 1, 1), True),
    (datetime.date(2019, 12, 31), True)
])
def data_inversao_mesmo_ano(request):
    return request.param


@pytest.fixture
def client_autenticado_coordenador_codae(client, django_user_model):
    email, password, rf, cpf = ('cogestor_1@sme.prefeitura.sp.gov.br', 'adminadmin', '0000001', '44426575052')
    user = django_user_model.objects.create_user(password=password, email=email, registro_funcional=rf, cpf=cpf)
    client.login(email=email, password=password)

    codae = mommy.make('Codae', nome='CODAE', uuid='b00b2cf4-286d-45ba-a18b-9ffe4e8d8dfd')

    perfil_coordenador = mommy.make('Perfil', nome='COORDENADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA', ativo=True,
                                    uuid='41c20c8b-7e57-41ed-9433-ccb92e8afaf1')
    mommy.make('Lote', uuid='143c2550-8bf0-46b4-b001-27965cfcd107')
    hoje = datetime.date.today()
    mommy.make('Vinculo', usuario=user, instituicao=codae, perfil=perfil_coordenador,
               data_inicial=hoje, ativo=True)

    return client
