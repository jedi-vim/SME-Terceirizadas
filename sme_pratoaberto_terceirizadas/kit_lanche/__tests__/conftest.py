import datetime

import pytest
from faker import Faker
from model_mommy import mommy

from .. import models
from ...dados_comuns.models import TemplateMensagem
from ...dados_comuns.models_abstract import TempoPasseio

fake = Faker('pt_BR')
fake.seed(420)


@pytest.fixture
def kit_lanche():
    itens = mommy.make(models.ItemKitLanche,
                       nome=fake.name(),
                       _quantity=3)
    return mommy.make(models.KitLanche, nome=fake.name(),
                      itens=itens)


@pytest.fixture
def item_kit_lanche():
    return mommy.make(models.ItemKitLanche,
                      nome=fake.name())


@pytest.fixture
def solicitacao_avulsa():
    mommy.make(TemplateMensagem, tipo=TemplateMensagem.SOLICITACAO_KIT_LANCHE_AVULSA)
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche, kits=kits, data=datetime.datetime(2000, 1, 1))
    escola = mommy.make('escola.Escola')
    return mommy.make(models.SolicitacaoKitLancheAvulsa,
                      local=fake.text()[:160],
                      quantidade_alunos=999,
                      solicitacao_kit_lanche=solicitacao_kit_lanche,
                      escola=escola)


@pytest.fixture
def solicitacao_unificada_lista_igual():
    mommy.make(TemplateMensagem, tipo=TemplateMensagem.SOLICITACAO_KIT_LANCHE_UNIFICADA)
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche,
                                        tempo_passeio=models.SolicitacaoKitLanche.OITO_OU_MAIS,
                                        kits=kits)
    dre = mommy.make('escola.DiretoriaRegional')
    return mommy.make(models.SolicitacaoKitLancheUnificada,
                      local=fake.text()[:160],
                      quantidade_max_alunos_por_escola=999,
                      lista_kit_lanche_igual=True,
                      solicitacao_kit_lanche=solicitacao_kit_lanche,
                      outro_motivo=fake.text(),
                      diretoria_regional=dre)


@pytest.fixture
def solicitacao_unificada_lotes_diferentes():
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche,
                                        tempo_passeio=models.SolicitacaoKitLanche.OITO_OU_MAIS,
                                        kits=kits)
    dre = mommy.make('escola.DiretoriaRegional', nome=fake.name())
    solicitacao_unificada = mommy.make(models.SolicitacaoKitLancheUnificada,
                                       local=fake.text()[:160],
                                       quantidade_max_alunos_por_escola=999,
                                       lista_kit_lanche_igual=True,
                                       solicitacao_kit_lanche=solicitacao_kit_lanche,
                                       outro_motivo=fake.text(),
                                       diretoria_regional=dre)
    lote_um = mommy.make('escola.Lote')
    escola_um = mommy.make('escola.Escola', lote=lote_um)
    escola_dois = mommy.make('escola.Escola', lote=lote_um)
    escola_tres = mommy.make('escola.Escola', lote=lote_um)
    mommy.make(models.EscolaQuantidade,
               escola=escola_um,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_dois,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_tres,
               solicitacao_unificada=solicitacao_unificada)
    lote_dois = mommy.make('escola.Lote')
    escola_quatro = mommy.make('escola.Escola', lote=lote_dois)
    escola_cinco = mommy.make('escola.Escola', lote=lote_dois)
    mommy.make(models.EscolaQuantidade,
               escola=escola_quatro,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_cinco,
               solicitacao_unificada=solicitacao_unificada)
    return solicitacao_unificada


@pytest.fixture
def solicitacao_unificada_lotes_iguais():
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche,
                                        tempo_passeio=models.SolicitacaoKitLanche.OITO_OU_MAIS,
                                        kits=kits)
    dre = mommy.make('escola.DiretoriaRegional', nome=fake.name())
    solicitacao_unificada = mommy.make(models.SolicitacaoKitLancheUnificada,
                                       local=fake.text()[:160],
                                       quantidade_max_alunos_por_escola=999,
                                       lista_kit_lanche_igual=True,
                                       solicitacao_kit_lanche=solicitacao_kit_lanche,
                                       outro_motivo=fake.text(),
                                       diretoria_regional=dre)
    lote_um = mommy.make('escola.Lote')
    escola_um = mommy.make('escola.Escola', lote=lote_um)
    escola_dois = mommy.make('escola.Escola', lote=lote_um)
    escola_tres = mommy.make('escola.Escola', lote=lote_um)
    escola_quatro = mommy.make('escola.Escola', lote=lote_um)
    escola_cinco = mommy.make('escola.Escola', lote=lote_um)
    mommy.make(models.EscolaQuantidade,
               escola=escola_um,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_dois,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_tres,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_quatro,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_cinco,
               solicitacao_unificada=solicitacao_unificada)
    return solicitacao_unificada


@pytest.fixture
def solicitacao():
    kits = mommy.make(models.KitLanche, nome=fake.name(), _quantity=3)
    return mommy.make(models.SolicitacaoKitLanche,
                      descricao=fake.text(),
                      motivo=fake.text(),
                      tempo_passeio=TempoPasseio.CINCO_A_SETE,
                      kits=kits)


@pytest.fixture(params=[
    (0, True),
    (1, True),
    (2, True),
])
def horarios_passeio(request):
    return request.param


erro_esperado_passeio = 'tempo de passeio deve ser qualquer uma das opções:'


@pytest.fixture(params=[
    ('0', erro_esperado_passeio),
    ('TESTE', erro_esperado_passeio),
    (3, erro_esperado_passeio),
])
def horarios_passeio_invalido(request):
    return request.param


@pytest.fixture(params=[
    # tempo passeio, qtd kits
    (0, 1),
    (1, 2),
    (2, 3),
])
def tempo_kits(request):
    return request.param


@pytest.fixture(params=[
    # data, tag
    ((2019, 9, 30), 'VENCIDO'),
    ((2019, 10, 1), 'VENCIDO'),
    ((2019, 10, 2), 'PRIORITARIO'),
    ((2019, 10, 3), 'PRIORITARIO'),
    ((2019, 10, 4), 'PRIORITARIO'),
    ((2019, 10, 5), 'PRIORITARIO'),
    ((2019, 10, 6), 'PRIORITARIO'),
    ((2019, 10, 7), 'LIMITE'),
    ((2019, 10, 8), 'LIMITE'),
    ((2019, 10, 9), 'LIMITE'),
    ((2019, 10, 10), 'REGULAR'),
    ((2019, 10, 11), 'REGULAR'),
    ((2019, 10, 12), 'REGULAR'),
    ((2019, 10, 13), 'REGULAR'),
])
def kits_avulsos_tageamentos(request):
    return request.param
