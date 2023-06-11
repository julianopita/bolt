from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from core.models import Endereco, Vaga, Carro, Pessoa, Administrador
from core.models import Prestador, Cliente, PontoDeApoio, Reserva, Evento, EventoCarro

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nome de usuário ou email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Senha'}))


class FormEndereco(ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'


class FormVaga(ModelForm):
    class Meta:
        model = Vaga
        fields = ('endereco', 'recarga')


class FormCarro(ModelForm):
    class Meta:
        model = Carro
        fields = ('placa', 'marca', 'modelo', 'cor', 'locacao', 'disponivel', 'vaga')


class FormPessoa(ModelForm):
    class Meta:
        model = Pessoa
        fields = ['user', 'nome', 'identificacao', 'telefone']


class FormAdministrador(ModelForm):
    class Meta:
        model = Administrador
        fields = ['nome', 'identificacao', 'telefone', 'matricula', 'cargo']


class FormPrestador(ModelForm):
    class Meta:
        model = Prestador
        fields = ['nome', 'identificacao', 'telefone', 'registro', 'especialidade']


class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'identificacao', 'telefone', 'dataNascimento']


class FormPontoDeApoio(ModelForm):
    class Meta:
        model = PontoDeApoio
        fields = ('nome', 'endereco', 'terceirizado')


class FormReserva(ModelForm):
    class Meta:
        model = Reserva
        fields = ('dataInicio', 'dataFim', 'carro')


class FormEvento(ModelForm):
    class Meta:
        model = Evento
        fields = ('nome', 'tipo', 'criticidade')


class FormEventoCarro(ModelForm):
    class Meta:
        model = EventoCarro
        fields = ('carro', 'evento', 'dataInicio', 'dataFim', 'resolvido')
