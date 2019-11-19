import environ
import requests
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from ...dados_comuns.behaviors import TemChaveExterna
from ...dados_comuns.constants import (
    ADMINISTRADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA,
    COORDENADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA,
    DJANGO_EOL_API_TOKEN,
    DJANGO_EOL_API_URL
)
from ...dados_comuns.tasks import envia_email_unico_task
from ...dados_comuns.utils import url_configs
from ...eol_servico.utils import EolException
from ..models import Perfil, Vinculo

env = environ.Env()


# Thanks to https://github.com/jmfederico/django-use-email-as-username


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):
    """An abstract base class implementing a fully featured User model with admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        envia_email_unico_task.delay(assunto=subject, corpo=message, email=self.email)


class Usuario(SimpleEmailConfirmationUserMixin, CustomAbstractUser, TemChaveExterna):
    """Classe de autenticacao do django, ela tem muitos perfis."""

    nome = models.CharField(_('name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    cpf = models.CharField(_('CPF'), max_length=11, unique=True, validators=[MinLengthValidator(11)])
    registro_funcional = models.CharField(_('RF'), max_length=7, unique=True, validators=[MinLengthValidator(7)])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # type: ignore

    @property
    def vinculos(self):
        return self.vinculos

    @property
    def vinculo_atual(self):
        if self.vinculos.filter(Q(data_inicial=None, data_final=None, ativo=False) |  # noqa W504 esperando ativacao
                                Q(data_inicial__isnull=False, data_final=None, ativo=True)).exists():
            return self.vinculos.get(
                Q(data_inicial=None, data_final=None, ativo=False) |  # noqa W504 esperando ativacao
                Q(data_inicial__isnull=False, data_final=None, ativo=True))
        return None

    @property
    def tipo_usuario(self):
        tipo_usuario = 'indefinido'
        if self.vinculo_atual:
            tipo_usuario = self.vinculo_atual.content_type.model
            if tipo_usuario == 'codae':
                if self.vinculo_atual.perfil.nome in [COORDENADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA,
                                                      ADMINISTRADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA]:
                    tipo_usuario = 'gestao_alimentacao_terceirizada'
                else:
                    tipo_usuario = 'dieta_especial'
        return tipo_usuario

    @property
    def pode_efetuar_cadastro(self):
        # TODO: passar isso para o app EOL serviço
        headers = {'Authorization': f'Token {DJANGO_EOL_API_TOKEN}'}
        r = requests.get(f'{DJANGO_EOL_API_URL}/cargos/{self.registro_funcional}', headers=headers)
        response = r.json()
        if not isinstance(response, dict):
            raise EolException(f'{response}')
        diretor_de_escola = False
        for result in response['results']:
            if result['cargo'] == 'DIRETOR DE ESCOLA':
                diretor_de_escola = True
                break
        vinculo_aguardando_ativacao = self.vinculo_atual.status == Vinculo.STATUS_AGUARDANDO_ATIVACAO
        return diretor_de_escola or vinculo_aguardando_ativacao

    def enviar_email_confirmacao(self):
        self.add_email_if_not_exists(self.email)
        content = {'uuid': self.uuid, 'confirmation_key': self.confirmation_key}
        self.email_user(
            subject='Confirme seu e-mail - SIGPAE',
            message=f'Clique neste link para confirmar seu e-mail no SIGPAE \n'
            f': {url_configs("CONFIRMAR_EMAIL", content)}',
        )

    def enviar_email_recuperacao_senha(self):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        content = {'uuid': self.uuid, 'confirmation_key': token}
        self.email_user(
            subject='Email de recuperação de senha',
            message=f'Clique neste link para criar uma nova senha no SIGPAE \n'
            f': {url_configs("RECUPERAR_SENHA", content)}',
        )

    def atualiza_senha(self, senha, token):
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(self, token):
            self.set_password(senha)
            self.save()
            return True
        return False

    def criar_vinculo_administrador(self, escola, nome_perfil):
        perfil = Perfil.objects.get(nome=nome_perfil)
        Vinculo.objects.create(
            instituicao=escola,
            perfil=perfil,
            usuario=self,
            ativo=False
        )
