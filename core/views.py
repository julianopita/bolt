from django.shortcuts import render, redirect
from core.forms import FormEndereco, FormVaga, FormCarro, FormPessoa, FormAdministrador
from core.forms import FormPrestador, FormCliente, FormPontoDeApoio, FormReserva, FormEvento, FormEventoCarro
from core.models import Endereco, Vaga, Carro, Pessoa, Administrador
from core.models import Prestador, Cliente, PontoDeApoio, Reserva, Evento, EventoCarro
from django.contrib.auth.decorators import login_required
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.views import generic
from users.forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


def home(request):
    contexto = {'home': 'home'}
    return render(request, 'core\index.html', contexto)


class Registrar(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registrar.html'


    def get_success_url(self):
        success_url = reverse_lazy('url_registro_cliente', kwargs={'id': self.object.pk})
        return success_url

    def post(self, request, *args, **kwargs):
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_group=Group.objects.get(name='Clientes')
            user.groups.add(user_group)
            return redirect(#success_url?)
        else:
            return render(request, self.template_name, {'form':form})



# CRUD Endereço

def cadastroEndereco(request):
    # verificar o if user is client etc.
    form = FormEndereco(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Endereço', 'txt_descricao': 'Cadastro de Endereço'}
    return render(request, 'core\cadastro.html', contexto)



def listagemEnderecos(request):
    if request.user.is_staff:
        if request.POST and request.POST['input_pesquisa']:
            dados = Endereco.objects.filter(placa__icontains=request.POST['input_pesquisa'])
        else:
            dados = Endereco.objects.all()
        contexto = {'dados': dados, 'text_input': 'Digite o CEP', 'listagem': 'listagem'}
        return render(request, 'core/listagem_enderecos.html', contexto)
    return render(request, 'aviso.html')


def alteraEndereco(request, id):
    if request.user.is_staff:  # verificar se usa
        obj = Endereco.objects.get(id=id)
        form = FormEndereco(request.POST or None, request.FILES or None, instance=obj)
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect('url_listagem_enderecos')
        contexto = {'form': form, 'txt_titulo': 'EditEndereco', 'txt_descrição': "Altera Endereço"}
        return render(request, 'core/cadastro.html', contexto)
    return render(request, 'aviso.html')


def excluiEndereco(request, id):  # alterar para isActive = false
    obj = Endereco.objects.get(id=id)
    contexto = {'txt_info': obj.cep, 'txt_url': '/listagemEnderecos/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listaEnderecos'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)

#CRUD Pessoa

def cadastroCliente(request):
    # verificar o if user is client etc.
    form = FormCliente(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Cliente', 'txt_descricao': 'Cadastro do Cliente'}
    return render(request, 'registration/registrar.html', contexto)


def registroCliente(request, id):
    #como receber o id? Como incorporar o user registration?
    #ReCaptchaField(widget=ReCaptchaV2Checkbox())
    #user_form = Registrar.as_view()
    endereco_form = FormEndereco(request.POST or None, request.FILES or None)
    cliente_form = FormCliente(request.POST or None, request.FILES or None)
    if all([endereco_form.is_valid() and cliente_form.is_valid()]):
        #usr = user_form
        end = endereco_form.save()
        cli = cliente_form.save(commit=False)
        cli.intaker=request.user
        cli.user_id = id
        #cli.user = usr
        cli.endereco = end
        cliente_form.save()
        return redirect('url_principal')
    contexto = {'endereco_form': endereco_form, 'cliente_form': cliente_form, 'txt_titulo': 'Cadastro Cliente', 'txt_descricao': 'Cadastro do Cliente'}
    return render(request, 'registration/registrar.html', contexto)
