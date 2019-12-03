import base64
import uuid
from mimetypes import guess_extension

from django.core.files.base import ContentFile
from drf_base64.serializers import ModelSerializer
from rest_framework import serializers

from .validators import deve_ter_extensao_valida
from ..models import Anexo, SolicitacaoDietaEspecial
from ...dados_comuns.api.serializers import LogSolicitacoesUsuarioSerializer
from ...dados_comuns.validators import deve_ser_no_passado
from ...escola.api.serializers import EscolaSimplesSerializer


class AnexoCreateSerializer(serializers.ModelSerializer):
    arquivo = serializers.CharField()
    nome = serializers.CharField()

    def validate_nome(self, nome):
        deve_ter_extensao_valida(nome)
        return nome

    class Meta:
        model = Anexo
        fields = ('arquivo', 'nome')


class AnexoSerializer(ModelSerializer):
    nome = serializers.CharField()

    def validate_nome(self, nome):
        deve_ter_extensao_valida(nome)
        return nome

    class Meta:
        model = Anexo
        fields = ('arquivo', 'nome')


class SolicitacaoDietaEspecialCreateSerializer(serializers.ModelSerializer):
    anexos = serializers.ListField(
        child=AnexoCreateSerializer(), required=True
    )

    def validate_anexos(self, anexos):
        if not anexos:
            raise serializers.ValidationError('Anexos não pode ser vazio')
        return anexos

    def validate_data_nascimento_aluno(self, data_nascimento_aluno):
        deve_ser_no_passado(data_nascimento_aluno)
        return data_nascimento_aluno

    def create(self, validated_data):
        validated_data['criado_por'] = self.context['request'].user
        anexos = validated_data.pop('anexos', [])
        solicitacao = SolicitacaoDietaEspecial.objects.create(**validated_data)

        for anexo in anexos:
            format, imgstr = anexo.get('arquivo').split(';base64,')
            ext = guess_extension(format[5:])
            data = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4()) + ext)
            anexo.pop('nome')
            Anexo.objects.create(
                solicitacao_dieta_especial=solicitacao, arquivo=data
            )

        solicitacao.inicia_fluxo(user=self.context['request'].user)
        return solicitacao

    class Meta:
        model = SolicitacaoDietaEspecial
        fields = (
            'uuid',
            'codigo_eol_aluno',
            'nome_completo_aluno',
            'nome_completo_pescritor',
            'registro_funcional_pescritor',
            'data_nascimento_aluno',
            'observacoes',
            'criado_em',
            'anexos'
        )


class SolicitacaoDietaEspecialSerializer(serializers.ModelSerializer):
    anexos = serializers.ListField(
        child=AnexoSerializer(), required=True
    )
    escola = EscolaSimplesSerializer()
    logs = LogSolicitacoesUsuarioSerializer(many=True)
    status_solicitacao = serializers.CharField(
        source='status',
        required=False,
        read_only=True
    )
    id_externo = serializers.CharField()

    class Meta:
        model = SolicitacaoDietaEspecial
        fields = (
            'uuid',
            'codigo_eol_aluno',
            'nome_completo_aluno',
            'nome_completo_pescritor',
            'registro_funcional_pescritor',
            'data_nascimento_aluno',
            'observacoes',
            'criado_em',
            'anexos',
            'status_solicitacao',
            'escola',
            'logs',
            'id_externo'
        )
