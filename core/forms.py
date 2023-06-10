
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
        fields = '__all__'


class FormCarro(ModelForm):


    class Meta:
        model = Carro
        fields = '__all__'


class FormPessoa(ModelForm):


    class Meta:
        model = Pessoa
        fields = ['user','nome', 'identificacao', 'telefone']


class FormAdministrador(ModelForm):


    class Meta:
        model = Administrador
        fields = '__all__'


class FormPrestador(ModelForm):


    class Meta:
        model = Prestador
        fields = '__all__'


class FormCliente(ModelForm):


    class Meta:
        model = Cliente
        exclude = ('endereco', 'user', 'isActive')
        fields = '__all__'


class FormPontoDeApoio(ModelForm):


    class Meta:
        model = PontoDeApoio
        fields = '__all__'


class FormReserva(ModelForm):


    class Meta:
        model = Reserva
        fields = '__all__'


class FormEvento(ModelForm):


    class Meta:
        model = Evento
        fields = '__all__'


class FormEventoCarro(ModelForm):


    class Meta:
        model = EventoCarro
        fields = '__all__'
