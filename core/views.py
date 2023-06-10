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

    # def post(self, request, *args, **kwargs):
    #     form=CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.save()
    #         user_group=Group.objects.get(name='Clientes')
    #         user.groups.add(user_group)
    #         return redirect(#success_url?)
    #     else:
    #         return render(request, self.template_name, {'form':form})



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


def registroCliente(request):
    #ReCaptchaField(widget=ReCaptchaV2Checkbox())
    user_form = CustomUserCreationForm(request.POST)
    endereco_form = FormEndereco(request.POST)
    cliente_form = FormCliente(request.POST or None, request.FILES or None)
    if all([user_form.is_valid() and endereco_form.is_valid() and cliente_form.is_valid()]):
        usr = user_form.save(commit=False)
        end = endereco_form.save()
        cli = cliente_form.save(commit=False)
        cli.intaker=request.user
        cli.user= usr
        cli.endereco = end
        user_form.save()
        cliente_form.save()
        user_group = Group.objects.get(name='Clientes')
        usr.groups.add(user_group)
        return redirect('url_principal')
    contexto = {'user_form' : user_form, 'endereco_form': endereco_form, 'cliente_form': cliente_form, 'txt_titulo': 'Cadastro Cliente', 'txt_descricao': 'Cadastro do Cliente'}
    return render(request, 'registration/registrar.html', contexto)

#criar alterar e deletar

#CRUD Vagas

def cadastroVaga(request):
    #verificar if usergroup is administrador
    form = FormVaga(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Vaga', 'txt_descricao': 'Cadastro de Vaga'}
    return render(request, 'core\cadastro.html', contexto)

def listagemVagas(request):
    #if request.user.is_staff:
        if request.POST and request.POST['input_pesquisa']:
            dados = Vaga.objects.filter(endereco__cep__icontains=request.POST['input_pesquisa'])
        else:
            dados = Vaga.objects.all()
        contexto = {'dados': dados, 'text_input': 'Digite o CEP', 'listagem': 'listagem'}
        return render(request, 'core/listagem_vagas.html', contexto)
    #return render(request, 'aviso.html')

def alteraVaga(request, id):
    if request.user.is_staff:  # verificar se usa
        obj = Vaga.objects.get(id=id)
        form = FormVaga(request.POST, instance=obj)
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect('url_listagem_vagas')
        contexto = {'form': form, 'txt_titulo': 'EditVaga', 'txt_descrição': "Altera Vagas"}
        return render(request, 'core/cadastro.html', contexto)
    return render(request, 'aviso.html')

def excluiVaga(request, id):
    obj = Vaga.objects.get(id=id)
    contexto = {'txt_info': obj.endereco.rua, 'txt_url': '/listagemVagas/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemVagas'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)

#CRUD PontoDeApoio

def cadastroPonto(request):
    #verificar if usergroup is administrador
    form = FormPontoDeApoio(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Pontos de Apoio', 'txt_descricao': 'Cadastro de Pontos de Apoio'}
    return render(request, 'core\cadastro.html', contexto)

def listagemPontos(request):
    # if request.user.is_staff:
        if request.POST and request.POST['input_pesquisa']:
            dados = PontoDeApoio.objects.filter(endereco__cep__icontains=request.POST['input_pesquisa'])
        else:
            dados = PontoDeApoio.objects.all()
            dados_compl = Vaga.objects.all()
        contexto = {'dados': dados, 'dados_compl': dados_compl, 'text_input': 'Digite o CEP', 'listagem': 'listagem'}
        return render(request, 'core/listagem_pontos.html', contexto)
    # return render(request, 'aviso.html')

def alteraPonto(request, id):
    if request.user.is_staff:  # verificar se usa
        obj = PontoDeApoio.objects.get(id=id)
        form = FormPontoDeApoio(request.POST, instance=obj)
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect('url_listagem_pontos')
        contexto = {'form': form, 'txt_titulo': 'EditPonto', 'txt_descrição': "Altera Pontos de Apoio"}
        return render(request, 'core/cadastro.html', contexto)
    return render(request, 'aviso.html')

def excluiPonto(request, id):
    obj = PontoDeApoio.objects.get(id=id)
    contexto = {'txt_info': obj.endereco.rua, 'txt_url': '/listagemPontos/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemPontos'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)

#CRUD Carro

def cadastroCarro(request):
    #verificar if usergroup is administrador
    form = FormCarro(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Carro', 'txt_descricao': 'Cadastro de Carros'}
    return render(request, 'core\cadastro.html', contexto)

def listagemCarros(request):
    pass

def alteraCarro(request, id):
    pass

def excluiCarro(request, id):
    pass