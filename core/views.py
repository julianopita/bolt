import decimal

from django.shortcuts import render, redirect

from core.forms import FormEndereco, FormVaga, FormCarro, FormPessoa, FormAdministrador
from core.forms import FormPrestador, FormCliente, FormPontoDeApoio, FormReserva, FormEvento, FormEventoCarro
from core.models import Endereco, Vaga, Carro, Pessoa, Administrador
from core.models import Prestador, Cliente, PontoDeApoio, Reserva, Evento, EventoCarro
from django.contrib.auth.decorators import login_required, user_passes_test
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.views import generic
from users.forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from datetime import datetime

User = get_user_model()


def checkGroupAdmin(user):
    return user.groups.filter(name='Administradores').exists()


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


# CRUD Pessoas e usuários


def registroCliente(request):
    # ReCaptchaField(widget=ReCaptchaV2Checkbox())
    user_form = CustomUserCreationForm(request.POST)
    endereco_form = FormEndereco(request.POST)
    pessoa_form = FormCliente(request.POST or None, request.FILES or None)
    if all([user_form.is_valid() and endereco_form.is_valid() and pessoa_form.is_valid()]):
        usr = user_form.save(commit=False)
        end = endereco_form.save()
        cli = pessoa_form.save(commit=False)
        cli.intaker = request.user
        cli.user = usr
        cli.endereco = end
        user_form.save()
        pessoa_form.save()
        user_group = Group.objects.get(name='Clientes')
        usr.groups.add(user_group)
        return redirect('url_principal')
    contexto = {'user_form': user_form, 'endereco_form': endereco_form, 'pessoa_form': pessoa_form,
                'txt_titulo': 'Cadastro Cliente', 'txt_descricao': 'Cadastro do Cliente'}
    return render(request, 'registration/registrar.html', contexto)


def listagemClientes(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Cliente.objects.filter(pessoa__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Cliente.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome', 'listagem': 'listagem'}
    return render(request, 'core/listagem_clientes.html', contexto)


def alteraCliente(request, id):
    obj = Cliente.objects.get(id=id)
    form = FormCliente(request.POST or None, instance=obj)
    #form_extra = FormEndereco(request.POST or None, instance=obj)
    if request.POST:
        if form.is_valid():# and form_extra.is_valid():
            form.save()
            #form_extra.save()
            return redirect('url_listagem_clientes')
    contexto = {'form': form, 'txt_titulo': 'EditCliente', 'txt_descrição': "Altera Cliente"}
    return render(request, 'core/cadastro.html', contexto)


def excluiCliente(request, id):
    obj = Cliente.objects.get(id=id)
    contexto = {'txt_info': obj.nome, 'txt_url': '/accounts/listagemClientes/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemClientes'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


def registroPrestador(request):
    # ReCaptchaField(widget=ReCaptchaV2Checkbox())
    user_form = CustomUserCreationForm(request.POST)
    endereco_form = FormEndereco(request.POST)
    pessoa_form = FormPrestador(request.POST or None, request.FILES or None)
    if all([user_form.is_valid() and endereco_form.is_valid() and pessoa_form.is_valid()]):
        usr = user_form.save(commit=False)
        end = endereco_form.save()
        pre = pessoa_form.save(commit=False)
        pre.intaker = request.user
        pre.user = usr
        pre.endereco = end
        user_form.save()
        pessoa_form.save()
        user_group = Group.objects.get(name='Prestadores')
        usr.groups.add(user_group)
        return redirect('url_principal')
    contexto = {'user_form': user_form, 'endereco_form': endereco_form, 'pessoa_form': pessoa_form,
                'txt_titulo': 'Cadastro Prestador', 'txt_descricao': 'Cadastro do Prestador de Serviços'}
    return render(request, 'registration/registrar.html', contexto)


def listagemPrestadores(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Prestador.objects.filter(pessoa__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Prestador.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome', 'listagem': 'listagem'}
    return render(request, 'core/listagem_prestadores.html', contexto)


def alteraPrestador(request, id):
    obj = Prestador.objects.get(id=id)
    form = FormPrestador(request.POST or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('url_listagem_prestadores')
    contexto = {'form': form, 'txt_titulo': 'EditPrestador', 'txt_descrição': "Altera Prestador"}
    return render(request, 'core/cadastro.html', contexto)


def excluiPrestador(request, id):
    obj = Prestador.objects.get(id=id)
    contexto = {'txt_info': obj.nome, 'txt_url': '/accounts/listagemPrestadores/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemPrestadores'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


def registroAdministrador(request):
    # ReCaptchaField(widget=ReCaptchaV2Checkbox())
    user_form = CustomUserCreationForm(request.POST)
    endereco_form = FormEndereco(request.POST)
    pessoa_form = FormAdministrador(request.POST or None, request.FILES or None)
    if all([user_form.is_valid() and endereco_form.is_valid() and pessoa_form.is_valid()]):
        usr = user_form.save(commit=False)
        end = endereco_form.save()
        pre = pessoa_form.save(commit=False)
        pre.intaker = request.user
        pre.user = usr
        pre.endereco = end
        user_form.save()
        pessoa_form.save()
        user_group = Group.objects.get(name='Administradores')
        usr.groups.add(user_group)
        return redirect('url_principal')
    contexto = {'user_form': user_form, 'endereco_form': endereco_form, 'pessoa_form': pessoa_form,
                'txt_titulo': 'Cadastro Administrador', 'txt_descricao': 'Cadastro do Administrador'}
    return render(request, 'registration/registrar.html', contexto)


def listagemAdministradores(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Administrador.objects.filter(pessoa__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Administrador.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome', 'listagem': 'listagem'}
    return render(request, 'core/listagem_administradores.html', contexto)


def alteraAdministrador(request, id):
    obj = Administrador.objects.get(id=id)
    form = FormAdministrador(request.POST or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('url_listagem_administradores')
    contexto = {'form': form, 'txt_titulo': 'EditAdm', 'txt_descrição': "Altera Administrador"}
    return render(request, 'core/cadastro.html', contexto)


def excluiAdministrador(request, id):
    obj = Administrador.objects.get(id=id)
    contexto = {'txt_info': obj.nome, 'txt_url': '/accounts/listagemAdministradores/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemAdministradores'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


# criar alterar e deletar

# CRUD Vagas

def cadastroVaga(request):
    # verificar if usergroup is administrador
    form = FormVaga(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Vaga', 'txt_descricao': 'Cadastro de Vaga'}
    return render(request, 'core\cadastro.html', contexto)


def listagemVagas(request):
    # if request.user.is_staff:
    if request.POST and request.POST['input_pesquisa']:
        dados = Vaga.objects.filter(endereco__cep__icontains=request.POST['input_pesquisa'])
    else:
        dados = Vaga.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o CEP', 'listagem': 'listagem'}
    return render(request, 'core/listagem_vagas.html', contexto)


# return render(request, 'aviso.html')

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


# CRUD PontoDeApoio

def cadastroPonto(request):
    # verificar if usergroup is administrador
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


# CRUD Carro
@login_required
@user_passes_test(checkGroupAdmin)
def cadastroCarro(request):
    form = FormCarro(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Carro', 'txt_descricao': 'Cadastro de Carros'}
    return render(request, 'core\cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemCarros(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Carro.objects.filter(placa__icontains=request.POST['input_pesquisa'])
    else:
        dados = Carro.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite a placa', 'listagem': 'listagem'}
    return render(request, 'core/listagem_carros.html', contexto)


# return render(request, 'aviso.html')

@login_required
@user_passes_test(checkGroupAdmin)
def alteraCarro(request, id):
    obj = Carro.objects.get(id=id)
    form = FormCarro(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do carro alterados com sucesso!')
            return redirect('url_listagem_carros')
    contexto = {'form': form, 'txt_titulo': 'EditCarro', 'txt_descrição': "Altera Carros"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def excluiCarro(request, id):
    obj = Carro.objects.get(id=id)
    contexto = {'txt_info': obj.placa, 'txt_url': '/listagemCarros/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemCarros'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


# CRUD Reserva
@login_required
def cadastroReserva(request):
    form = FormReserva(request.POST)
    if form.is_valid():
        rsr = form.save(commit=False)
        if rsr.dataFim:
            timediff = rsr.dataFim - rsr.dataInicio
            timehours = (((timediff.total_seconds() / 60) / 60) / 24)
            rsr.tempoReserva = timehours
            rsr.valor = rsr.carro.locacao * decimal.Decimal(timehours)
        rsr.cliente = Cliente.objects.get(id=request.user.id)
        form.save()
        return redirect('url_principal')
    contexto = {'form': form,
                'txt_titulo': 'Cadastro Reserva', 'txt_descricao': 'Cadastro da Reserva'}
    return render(request, 'core/cadastro.html', contexto)


@login_required
def listagemReservas(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Reserva.objects.filter(cliente__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Reserva.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome do usuário', 'listagem': 'listagem'}
    return render(request, 'core/listagem_reservas.html', contexto)


# return render(request, 'aviso.html')

@login_required
def alteraReserva(request, id):
    obj = Reserva.objects.get(id=id)
    form = FormReserva(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da reserva alterados com sucesso!')
            return redirect('url_listagem_reservas')
    contexto = {'form': form, 'txt_titulo': 'EditReserva', 'txt_descrição': "Altera Reservas"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
def excluiReserva(request, id):
    obj = Reserva.objects.get(id=id)
    contexto = {'txt_info': obj.cliente.nome, 'txt_url': '/listagemReservas/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemReservas'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


# CRUD Evento
@login_required
@user_passes_test(checkGroupAdmin)
def cadastroEvento(request):
    form = FormEvento(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Evento', 'txt_descricao': 'Cadastro de Eventos'}
    return render(request, 'core\cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemEventos(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Evento.objects.filter(nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Evento.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome do evento', 'listagem': 'listagem'}
    return render(request, 'core/listagem_eventos.html', contexto)


# return render(request, 'aviso.html')

@login_required
@user_passes_test(checkGroupAdmin)
def alteraEvento(request, id):
    obj = Evento.objects.get(id=id)
    form = FormEvento(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do evento alterados com sucesso!')
            return redirect('url_listagem_eventos')
    contexto = {'form': form, 'txt_titulo': 'EditEvento', 'txt_descrição': "Altera Eventos"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def excluiEvento(request, id):
    obj = Evento.objects.get(id=id)
    contexto = {'txt_info': obj.nome, 'txt_url': '/listagemEventos/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemEventos'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def cadastroEventoCarro(request):
    form = FormEventoCarro(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro EventoCarro', 'txt_descricao': 'Cadastro de Eventos com Carros'}
    return render(request, 'core\cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemEventoCarros(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = EventoCarro.objects.filter(carro__placa__icontains=request.POST['input_pesquisa'])
    else:
        dados = EventoCarro.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite a placa do carro', 'listagem': 'listagem'}
    return render(request, 'core/listagem_evento_carros.html', contexto)


# return render(request, 'aviso.html')

@login_required
@user_passes_test(checkGroupAdmin)
def alteraEventoCarro(request, id):
    obj = EventoCarro.objects.get(id=id)
    form = FormEventoCarro(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do evento com o carro alterados com sucesso!')
            return redirect('url_listagem_evento_carros')
    contexto = {'form': form, 'txt_titulo': 'EditEvento', 'txt_descrição': "Altera Eventos com Carros"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def excluiEventoCarro(request, id):
    obj = EventoCarro.objects.get(id=id)
    contexto = {'txt_info': obj.id, 'txt_url': '/listagemEventoCarros/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemEventoCarros'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)
