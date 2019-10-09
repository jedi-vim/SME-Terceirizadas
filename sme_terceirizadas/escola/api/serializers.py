from rest_framework import serializers
from ...terceirizada.models import Terceirizada
from ...terceirizada.api.serializers.serializers import (
    ContratoSimplesSerializer,
    NutricionistaSerializer
)
from ...dados_comuns.api.serializers import ContatoSerializer, EnderecoSerializer
from ..models import (
    Codae, DiretoriaRegional, Escola, FaixaIdadeEscolar,
    Lote, PeriodoEscolar, Subprefeitura, TipoGestao,
    TipoUnidadeEscolar
)
from ...cardapio.models import TipoAlimentacao
from ...perfil.api.serializers import PerfilSerializer
from ...perfil.models import Usuario
from ...terceirizada.api.serializers.serializers import TerceirizadaSimplesSerializer


class SubsticuicoesTipoAlimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAlimentacao
        exclude = ('id', 'substituicoes',)


class TipoAlimentacaoSerializer(serializers.ModelSerializer):
    substituicoes = SubsticuicoesTipoAlimentacaoSerializer(many=True)

    class Meta:
        model = TipoAlimentacao
        exclude = ('id',)


class PeriodoEscolarSerializer(serializers.ModelSerializer):
    tipos_alimentacao = TipoAlimentacaoSerializer(many=True)

    class Meta:
        model = PeriodoEscolar
        exclude = ('id',)


class PeriodoEscolarSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoEscolar
        exclude = ('id', 'tipos_alimentacao')


class TipoGestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGestao
        exclude = ('id',)


class SubprefeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subprefeitura
        exclude = ('id',)


class TipoUnidadeEscolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUnidadeEscolar
        exclude = ('id', 'cardapios')


class FaixaIdadeEscolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaixaIdadeEscolar
        exclude = ('id',)


class DiretoriaRegionalSimplissimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiretoriaRegional
        fields = ('uuid', 'nome')


class EscolaSimplissimaSerializer(serializers.ModelSerializer):
    lote = serializers.SerializerMethodField()

    def get_lote(self, obj):
        return f'{obj.lote.nome} - {obj.lote.iniciais}' if obj.lote else None

    class Meta:
        model = Escola
        fields = ('uuid', 'nome', 'codigo_eol', 'lote', 'quantidade_alunos')


class DiretoriaRegionalSimplesSerializer(serializers.ModelSerializer):
    escolas = EscolaSimplissimaSerializer(many=True)
    quantidade_alunos = serializers.IntegerField()

    class Meta:
        model = DiretoriaRegional
        exclude = ('id',)


class LoteSimplesSerializer(serializers.ModelSerializer):
    diretoria_regional = DiretoriaRegionalSimplissimaSerializer()
    tipo_gestao = TipoGestaoSerializer()
    escolas = EscolaSimplissimaSerializer(many=True)
    terceirizada = TerceirizadaSimplesSerializer()
    subprefeituras = SubprefeituraSerializer(many=True)

    class Meta:
        model = Lote
        exclude = ('id',)


class LoteNomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ('uuid', 'nome')


class EscolaSimplesSerializer(serializers.ModelSerializer):
    lote = LoteNomeSerializer()
    tipo_gestao = TipoGestaoSerializer()
    periodos_escolares = PeriodoEscolarSerializer(many=True)
    diretoria_regional = DiretoriaRegionalSimplissimaSerializer()

    class Meta:
        model = Escola
        fields = ('uuid', 'nome', 'codigo_eol', 'quantidade_alunos', 'periodos_escolares', 'lote', 'tipo_gestao',
                  'diretoria_regional')


class EscolaListagemSimplesSelializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = ('uuid', 'nome', 'codigo_eol')


class EscolaCompletaSerializer(serializers.ModelSerializer):
    diretoria_regional = DiretoriaRegionalSimplesSerializer()
    idades = FaixaIdadeEscolarSerializer(many=True)
    tipo_unidade = TipoUnidadeEscolarSerializer()
    tipo_gestao = TipoGestaoSerializer()
    periodos_escolares = PeriodoEscolarSerializer(many=True)
    lote = LoteSimplesSerializer()

    class Meta:
        model = Escola
        exclude = ('id',)


class DiretoriaRegionalCompletaSerializer(serializers.ModelSerializer):
    lotes = LoteSimplesSerializer(many=True)
    escolas = EscolaSimplesSerializer(many=True)

    class Meta:
        model = DiretoriaRegional
        exclude = ('id',)


class UsuarioDetalheSerializer(serializers.ModelSerializer):
    perfis = PerfilSerializer(many=True, read_only=True)
    escolas = EscolaSimplesSerializer(many=True)
    diretorias_regionais = DiretoriaRegionalSimplesSerializer(many=True)
    tipo_usuario = serializers.CharField()

    class Meta:
        model = Usuario
        fields = ('uuid', 'nome', 'email', 'registro_funcional', 'tipo_usuario',
                  'date_joined', 'perfis', 'escolas', 'diretorias_regionais')


class CODAESerializer(serializers.ModelSerializer):
    quantidade_alunos = serializers.IntegerField()

    class Meta:
        model = Codae
        fields = '__all__'


class TerceirizadaSerializer(serializers.ModelSerializer):
    nutricionistas = NutricionistaSerializer(many=True)
    contatos = ContatoSerializer(many=True)
    endereco = EnderecoSerializer()
    contratos = ContratoSimplesSerializer(many=True)
    lotes = LoteNomeSerializer(many=True)
    id_externo = serializers.CharField()

    class Meta:
        model = Terceirizada
        exclude = ('id', 'usuarios',)