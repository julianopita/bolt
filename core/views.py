import decimal
from django.http import JsonResponse
from django.shortcuts import render, redirect
from core.forms import FormEndereco, FormVaga, FormCarro, FormPessoa, FormAdministrador
from core.forms import FormPrestador, FormCliente, FormPontoDeApoio, FormReserva, FormEvento, FormEventoCarro, \
    FormCarroReserva
from core.models import Endereco, Vaga, Carro, Pessoa, Administrador
from core.models import Prestador, Cliente, PontoDeApoio, Reserva, Evento, EventoCarro
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from users.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages

User = get_user_model()


def home(request):
    if request.POST and request.POST['input_pesquisa'] and request.POST['input_pesquisa'] != 'None':
        cidade_selecionada = request.POST['input_pesquisa']
        return redirect('url_carros_disponiveis', cidade_selecionada)
    else:
        cidade_selecionada = 'None'

    carros = Carro.objects.filter(disponivel=True)

    cidades = set(Vaga.objects.prefetch_related().all().values_list('endereco__cidade'))

    contexto = {'home': 'home', 'carros': carros, 'cidades': cidades, 'cidade_selecionada': cidade_selecionada}
    return render(request, 'core/index.html', contexto)


# Controle de acesso
def checkGroupAdmin(user):
    return user.groups.filter(name='Administradores').exists()


def checkGroupPrestador(user):
    return user.groups.filter(name='Prestadores').exists()


def checkUserId(request):
    return request.user.id


# Registro de usuario
class Registrar(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registrar.html'

    def get_success_url(self):
        success_url = reverse_lazy('url_registro_cliente', kwargs={'id': self.object.pk})
        return success_url


# CRUD Endereço

@login_required
@user_passes_test(checkGroupAdmin)
def cadastroEndereco(request):
    # verificar o if user is client etc.
    form = FormEndereco(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Endereço', 'txt_descricao': 'Cadastro de Endereço'}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemEnderecos(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Endereco.objects.filter(placa__icontains=request.POST['input_pesquisa'])
    else:
        dados = Endereco.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o CEP', 'listagem': 'listagem'}
    return render(request, 'core/listagem_enderecos.html', contexto)


@login_required
def alteraEndereco(request, id):
    obj = Endereco.objects.get(id=id)
    form = FormEndereco(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('url_listagem_enderecos')
    contexto = {'form': form, 'txt_titulo': 'EditEndereco', 'txt_descrição': "Altera Endereço"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
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
                'txt_titulo': 'Cadastro Cliente', 'txt_descricao': 'Cadastro do Cliente',
                'grupo': 'Cliente'}
    return render(request, 'registration/registrar.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemClientes(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Cliente.objects.filter(pessoa__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Cliente.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome', 'listagem': 'listagem'}
    return render(request, 'core/listagem_clientes.html', contexto)


@login_required
def alteraCliente(request, id):
    obj = Cliente.objects.get(id=id)
    form = FormCliente(request.POST or None, instance=obj)
    # form_extra = FormEndereco(request.POST or None, instance=obj)
    if request.POST:
        if form.is_valid():  # and form_extra.is_valid():
            form.save()
            # form_extra.save()
            return redirect('url_listagem_clientes')
    contexto = {'form': form, 'txt_titulo': 'EditCliente', 'txt_descrição': "Altera Cliente"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def excluiCliente(request, id):
    obj = Cliente.objects.get(id=id)
    contexto = {'txt_info': obj.nome, 'txt_url': '/accounts/listagemClientes/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemClientes'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
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
                'txt_titulo': 'Cadastro Prestador', 'txt_descricao': 'Cadastro do Prestador de Serviços',
                'grupo': 'Prestador'}
    return render(request, 'registration/registrar.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemPrestadores(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Prestador.objects.filter(pessoa__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Prestador.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome', 'listagem': 'listagem'}
    return render(request, 'core/listagem_prestadores.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def alteraPrestador(request, id):
    obj = Prestador.objects.get(id=id)
    form = FormPrestador(request.POST or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('url_listagem_prestadores')
    contexto = {'form': form, 'txt_titulo': 'EditPrestador', 'txt_descrição': "Altera Prestador"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def excluiPrestador(request, id):
    obj = Prestador.objects.get(id=id)
    contexto = {'txt_info': obj.nome, 'txt_url': '/accounts/listagemPrestadores/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemPrestadores'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
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
                'txt_titulo': 'Cadastro Administrador', 'txt_descricao': 'Cadastro do Administrador',
                'grupo': 'Administrador'}
    return render(request, 'registration/registrar.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemAdministradores(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Administrador.objects.filter(pessoa__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Administrador.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome', 'listagem': 'listagem'}
    return render(request, 'core/listagem_administradores.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def alteraAdministrador(request, id):
    obj = Administrador.objects.get(id=id)
    form = FormAdministrador(request.POST or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('url_listagem_administradores')
    contexto = {'form': form, 'txt_titulo': 'EditAdm', 'txt_descrição': "Altera Administrador"}
    return render(request, 'core/cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def excluiAdministrador(request, id):
    obj = Administrador.objects.get(id=id)
    contexto = {'txt_info': obj.nome, 'txt_url': '/accounts/listagemAdministradores/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemAdministradores'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


# CRUD Vagas
@login_required
@user_passes_test(checkGroupAdmin)
def cadastroVaga(request):
    form = FormVaga(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Vaga', 'txt_descricao': 'Cadastro de Vaga'}
    return render(request, 'core\cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def listagemVagas(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Vaga.objects.filter(endereco__cep__icontains=request.POST['input_pesquisa'])
    else:
        dados = Vaga.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o CEP', 'listagem': 'listagem'}
    return render(request, 'core/listagem_vagas.html', contexto)


# return render(request, 'aviso.html')
@login_required
@user_passes_test(checkGroupAdmin)
def alteraVaga(request, id):
        obj = Vaga.objects.get(id=id)
        form = FormVaga(request.POST, instance=obj)
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect('url_listagem_vagas')
        contexto = {'form': form, 'txt_titulo': 'EditVaga', 'txt_descrição': "Altera Vagas"}
        return render(request, 'core/cadastro.html', contexto)



@login_required
@user_passes_test(checkGroupAdmin)
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
@login_required
@user_passes_test(checkGroupAdmin)
def cadastroPonto(request):
    form = FormPontoDeApoio(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Pontos de Apoio', 'txt_descricao': 'Cadastro de Pontos de Apoio'}
    return render(request, 'core\cadastro.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
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
@login_required
@user_passes_test(checkGroupAdmin)
def alteraPonto(request, id):
        obj = PontoDeApoio.objects.get(id=id)
        form = FormPontoDeApoio(request.POST, instance=obj)
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect('url_listagem_pontos')
        contexto = {'form': form, 'txt_titulo': 'EditPonto', 'txt_descrição': "Altera Pontos de Apoio"}
        return render(request, 'core/cadastro.html', contexto)



@login_required
@user_passes_test(checkGroupAdmin)
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
@user_passes_test(checkGroupAdmin)
def listagemReservas(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Reserva.objects.filter(cliente__nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Reserva.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome do usuário', 'listagem': 'listagem'}
    return render(request, 'core/listagem_reservas.html', contexto)



@login_required
@user_passes_test(checkGroupAdmin)
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
@user_passes_test(checkGroupAdmin)
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
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
def cadastroEvento(request):
    form = FormEvento(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro Evento', 'txt_descricao': 'Cadastro de Eventos'}
    return render(request, 'core\cadastro.html', contexto)


@login_required
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
def listagemEventos(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = Evento.objects.filter(nome__icontains=request.POST['input_pesquisa'])
    else:
        dados = Evento.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite o nome do evento', 'listagem': 'listagem'}
    return render(request, 'core/listagem_eventos.html', contexto)


# return render(request, 'aviso.html')

@login_required
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
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
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
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
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
def cadastroEventoCarro(request):
    form = FormEventoCarro(request.POST)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo': 'Cadastro EventoCarro', 'txt_descricao': 'Cadastro de Eventos com Carros'}
    return render(request, 'core\cadastro.html', contexto)


@login_required
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
def listagemEventoCarros(request):
    if request.POST and request.POST['input_pesquisa']:
        dados = EventoCarro.objects.filter(carro__placa__icontains=request.POST['input_pesquisa'])
    else:
        dados = EventoCarro.objects.all()
    contexto = {'dados': dados, 'text_input': 'Digite a placa do carro', 'listagem': 'listagem'}
    return render(request, 'core/listagem_evento_carros.html', contexto)



@login_required
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
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
@user_passes_test(lambda u: checkGroupAdmin or checkGroupPrestador)
def excluiEventoCarro(request, id):
    obj = EventoCarro.objects.get(id=id)
    contexto = {'txt_info': obj.id, 'txt_url': '/listagemEventoCarros/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listagemEventoCarros'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)


# Casos funcionais - 001

def CarrosDisponiveis(request, regiao):
    # Na implementacao real recebe latitude e longitude do usuário em formato de dicionário
    # Usuário indica na interface 001 a região onde quer ver
    # A partir do endereço ou do clique no mapa, a funcao recupera latitude e longitude - não implementado:
    # No exemplo vamos substituir por duas cidades

    # if request.POST:
    # A partir do endereço ou do clique no mapa, a funcao recupera latitude e longitude - não implementado:
    # No exemplo vamos substituir por duas cidades hardcoded. Utilizar latitude e longitude demanda alterações no banco de dados

    # carros_prox = carros.objects.filter(vaga__coordinates__distance_lte=(locale, D(km=4)))
    if request.POST and request.POST['input_pesquisa'] == 'None':
        return redirect('url_principal')

    if request.POST and request.POST['input_pesquisa']:
        cidade_selecionada = request.POST['input_pesquisa']
        return redirect('url_carros_disponiveis', cidade_selecionada)
    elif request.POST and request.POST['input_pesquisa'] != 'None':
        cidade_selecionada = request.POST['input_pesquisa']
        carros = Carro.objects.filter(vaga__endereco__cidade=cidade_selecionada)
    else:
        cidade_selecionada = regiao
        carros = Carro.objects.filter(vaga__endereco__cidade=cidade_selecionada)

    cidades = set(Vaga.objects.prefetch_related().all().values_list('endereco__cidade'))
    contexto = {'carros': carros, 'cidades': cidades, 'cidade_selecionada': cidade_selecionada,
                'text_input': 'Digite a região onde quer procurar carros'}
    return render(request, 'core/index.html', contexto)


@login_required
def CarroReserva(request, id):
    form = FormCarroReserva(request.POST)
    dados = Carro.objects.get(id=id)
    if form.is_valid():
        rsr = form.save(commit=False)
        if rsr.dataFim:
            timediff = rsr.dataFim - rsr.dataInicio
            timehours = (((timediff.total_seconds() / 60) / 60) / 24)
            rsr.tempoReserva = timehours
            rsr.valor = rsr.carro.locacao * decimal.Decimal(timehours)
        rsr.cliente = Cliente.objects.get(user__id=request.user.id)
        rsr.carro = Carro.objects.get(id=id)
        form.save()
        # form_carro.save()
        return redirect('url_principal')
    contexto = {'form': form, 'dados': dados,
                'txt_titulo': 'ReservaCarro', 'txt_descricao': 'Reserva de carro'}
    return render(request, 'core/cadastro_carro_reserva.html', contexto)


@login_required
def usuarioListagemReservas(request):
    dados = Reserva.objects.filter(cliente__user__id__exact=request.user.id)
    contexto = {'dados': dados, 'text_input': 'Digite o numero da reserva'}
    return render(request, 'core/listagem_reservas.html', contexto)


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


# Dados clientes
@login_required
def listagemDadosCliente(request):
    dados = Cliente.objects.filter(user__id__exact=request.user.id)
    contexto = {'dados': dados, 'text_input': 'Digite o numero da reserva'}
    return render(request, 'core/listagem_clientes.html', contexto)


@login_required
@user_passes_test(checkGroupAdmin)
def alteraCliente(request, id):
    obj = Cliente.objects.get(id=id)
    form = FormCliente(request.POST or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('url_listagem_clientes')
    contexto = {'form': form, 'txt_titulo': 'EditCliente', 'txt_descrição': "Altera Cliente"}
    return render(request, 'core/cadastro.html', contexto)
