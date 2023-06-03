from django.shortcuts import render, redirect
from core.forms import FormEndereco, FormVaga, FormCarro, FormPessoa, FormAdministrador
from core.forms import FormPrestador, FormCliente, FormPontoDeApoio, FormReserva, FormEvento, FormEventoCarro
from core.models import Endereco, Vaga, Carro, Pessoa, Administrador
from core.models import Prestador, Cliente, PontoDeApoio, Reserva, Evento, EventoCarro
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

def home(request):
    contexto = {'home':'home'}
    return render(request, 'core\index.html', contexto)

class Registrar(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('url_principal')
    template_name = 'registration/registrar.html'

#CRUD Endereço

def cadastroEndereco(request):
    #verificar o if user is client etc.
    form = FormEndereco(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo':'Cadastro Endereço', 'txt_descricao':'Cadastro de Endereço'}
    return render(request, 'core\cadastro.html', contexto)
    return render(request, 'aviso.html')

def listagemEnderecos(request):
    if request.user.is_staff:
        if request.POST and request.POST['input_pesquisa']:
            dados = Endereco.objects.filter(placa__icontains=request.POST['input_pesquisa'])
        else:
            dados = Endereco.objects.all()
        contexto = {'dados': dados, 'text_input': 'Digite o CEP','listagem':'listagem'}
        return render(request, 'core/listagem_enderecos.html', contexto)
    return render(request, 'aviso.html')

def alteraEndereco(request):
    if request.user.is_staff: #verificar se usa
        obj = Endereco.objects.get(id=id)
        form = FormEndereco(request.POST or None, request.FILES or None, instance=obj)
        if request.POST:
            if form.is_valid():
                form.save()
                return redirect('url_listagem_endereco')
        contexto = {'form': form, 'txt_titulo': 'EditEndereco', 'tct_descrição': "Altera Endereço"}
        return render(request, 'core/cadastro.html', contexto)
    return render(request, 'aviso.html')

def excluiEndereco(request, id):
    obj = Endereco.objects.get(id=id)
    contexto = {'txt_info': obj.cep, 'txt_url': '/listagemEnderecos/'}
    if request.POST:
        obj.delete()
        contexto.update({'txt_tipo': 'listaEnderecos'})
        return render(request, 'core/aviso_exclusao.html', contexto)
    else:
        return render(request, 'core/confirma_exclusao.html', contexto)

