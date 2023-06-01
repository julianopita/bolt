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
    return render(request, 'core\index.html')

class Registrar(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('url_principal')
    template_name = 'registration/registrar.html'

#CRUD Endereço

def cadastroEndereco(request):
    form = FormEndereco(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'txt_titulo':'Cadastro Endereço', 'txt_descricao':'Cadastro de Endereço'}
    return render(request, 'core\cadastro.html', contexto)
    #return render(request, 'aviso.html')