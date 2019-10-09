import pytest

pytestmark = pytest.mark.django_db


def test_modelo_edital(edital):
    assert edital.uuid is not None
    assert edital.tipo_contratacao is not None
    assert edital.numero is not None
    assert edital.processo is not None
    assert edital.numero is not None
    assert edital.objeto is not None
    assert edital.contratos is not None


def test_modelo_contrato(contrato):
    assert contrato.uuid is not None
    assert contrato.numero is not None
    assert contrato.processo is not None
    assert contrato.data_proposta is not None
    assert contrato.lotes is not None
    assert contrato.terceirizada is not None
    assert contrato.vigencias is not None
    assert contrato.diretorias_regionais is not None


def test_modelo_vigencia_contrato(vigencia_contrato):
    assert vigencia_contrato.uuid is not None
    assert vigencia_contrato.data_inicial is not None
    assert vigencia_contrato.data_final is not None