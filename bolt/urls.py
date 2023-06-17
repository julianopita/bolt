"""
URL configuration for bolt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import home
from django.conf.urls.static import static
from django.conf import settings

#CRUD Endereço
from core.views import cadastroEndereco, listagemEnderecos, alteraEndereco, excluiEndereco

#CRUD User
from core.views import registroCliente, listagemClientes, alteraCliente, excluiCliente
from core.views import registroPrestador,listagemPrestadores, alteraPrestador, excluiPrestador
from core.views import registroAdministrador,listagemAdministradores, alteraAdministrador, excluiAdministrador

#CRUD Vagas
from core.views import cadastroVaga, listagemVagas, alteraVaga, excluiVaga

#CRUD Pontos
from core.views import cadastroPonto, listagemPontos, alteraPonto, excluiPonto

#CRUD Carros
from core.views import cadastroCarro, listagemCarros, alteraCarro, excluiCarro

#CRUD Reservas
from core.views import cadastroReserva, listagemReservas, alteraReserva, excluiReserva

#CRUD Eventos
from core.views import cadastroEvento, listagemEventos, alteraEvento, excluiEvento

#CRUD EventoCarro
from core.views import cadastroEventoCarro, listagemEventoCarros, alteraEventoCarro, excluiEventoCarro

#funcionalidades
from core.views import CarrosDisponiveis, CarroReserva, usuarioListagemReservas

#Dados usuário
from core.views import listagemDadosCliente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home, name='url_principal'),
    path('accounts/registrarCliente/', registroCliente, name='url_registrar_cliente'),
    path('accounts/listagemClientes/', listagemClientes, name='url_listagem_clientes'),
    path('accounts/alteraCliente/<int:id>/', alteraCliente, name='url_altera_cliente'),
    path('accounts/excluiCliente/<int:id>/', excluiCliente, name='url_exclui_cliente'),
    path('accounts/registrarPrestador/', registroPrestador, name='url_registrar_prestador'),
    path('accounts/listagemPrestadores/', listagemPrestadores, name='url_listagem_prestadores'),
    path('accounts/alteraPrestador/<int:id>/', alteraPrestador, name='url_altera_prestador'),
    path('accounts/excluiPrestador/<int:id>/', excluiPrestador, name='url_exclui_prestador'),
    path('accounts/registrarAdministrador/', registroAdministrador, name='url_registrar_administrador'),
    path('accounts/listagemAdministradores/', listagemAdministradores, name='url_listagem_administradores'),
    path('accounts/alteraAdministrador/<int:id>/', alteraAdministrador, name='url_altera_administrador'),
    path('accounts/excluiAdministrador/<int:id>/', excluiAdministrador, name='url_exclui_administrador'),
    path('cadastroEndereco/', cadastroEndereco, name='url_cadastro_endereco'),
    path('listagemEnderecos/', listagemEnderecos, name='url_listagem_enderecos'),
    path('alteraEndereco/<int:id>/', alteraEndereco, name='url_altera_endereco'),
    path('excluiEndereco/<int:id>/', excluiEndereco, name='url_exclui_endereco'),
    path('cadastroVaga/', cadastroVaga, name='url_cadastro_vaga'),
    path('listagemVagas/', listagemVagas, name='url_listagem_vagas'),
    path('alteraVaga/<int:id>/', alteraVaga, name='url_altera_vaga'),
    path('excluiVaga/<int:id>/', excluiVaga, name='url_exclui_vaga'),
    path('cadastroPonto/', cadastroPonto, name='url_cadastro_ponto'),
    path('listagemPontos/', listagemPontos, name='url_listagem_pontos'),
    path('alteraPonto/<int:id>/', alteraPonto, name='url_altera_ponto'),
    path('excluiPonto/<int:id>/', excluiPonto, name='url_exclui_ponto'),
    path('cadastroCarro/', cadastroCarro, name='url_cadastro_carro'),
    path('listagemCarros/', listagemCarros, name='url_listagem_carros'),
    path('alteraCarro/<int:id>/', alteraCarro, name='url_altera_carro'),
    path('excluiCarro/<int:id>/', excluiCarro, name='url_exclui_carro'),
    path('cadastroReserva/', cadastroReserva, name='url_cadastro_reserva'),
    path('listagemReservas/', listagemReservas, name='url_listagem_reservas'),
    path('alteraReserva/<int:id>/', alteraReserva, name='url_altera_reserva'),
    path('excluiReserva/<int:id>/', excluiReserva, name='url_exclui_reserva'),
    path('cadastroEvento/', cadastroEvento, name='url_cadastro_evento'),
    path('listagemEventos/', listagemEventos, name='url_listagem_eventos'),
    path('alteraEvento/<int:id>/', alteraEvento, name='url_altera_evento'),
    path('excluiEvento/<int:id>/', excluiEvento, name='url_exclui_evento'),
    path('cadastroEventoCarro/', cadastroEventoCarro, name='url_cadastro_evento_carro'),
    path('listagemEventoCarros/', listagemEventoCarros, name='url_listagem_evento_carros'),
    path('alteraEventoCarro/<int:id>/', alteraEventoCarro, name='url_altera_evento_carro'),
    path('excluiEventoCarro/<int:id>/', excluiEventoCarro, name='url_exclui_evento_carro'),
    #funcionalidades
    path('CarrosDisponiveis/<str:regiao>/', CarrosDisponiveis, name='url_carros_disponiveis'),
    path('CarroReserva/<int:id>/', CarroReserva, name='url_carro_reserva'),
    path('usuarioListagemReservas/', usuarioListagemReservas, name='url_usuario_listagem_reservas'),
    #dados do usuario pelo usuario
    path('listagemMeusDados/', listagemDadosCliente, name='url_listagem_dados_cliente'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
