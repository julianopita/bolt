from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from core.models import Endereco, Vaga, Carro, Pessoa, Administrador
from core.models import Prestador, Cliente, PontoDeApoio, Reserva, Evento, EventoCarro


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nome de usuário ou email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Senha'}))

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())



class FormEndereco(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Endereco
        fields = '__all__'


class FormVaga(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Vaga
        fields = '__all__'


class FormCarro(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Carro
        fields = '__all__'


class FormPessoa(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Pessoa
        fields = '__all__'


class FormAdministrador(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Administrador
        fields = '__all__'


class FormPrestador(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Prestador
        fields = '__all__'


class FormCliente(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Cliente
        fields = '__all__'


class FormPontoDeApoio(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = PontoDeApoio
        fields = '__all__'


class FormReserva(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Reserva
        fields = '__all__'


class FormEvento(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Evento
        fields = '__all__'


class FormEventoCarro(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = EventoCarro
        fields = '__all__'
