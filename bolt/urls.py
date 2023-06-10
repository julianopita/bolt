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
from core.views import Registrar
#CRUD Endereço
from core.views import cadastroEndereco, listagemEnderecos, alteraEndereco, excluiEndereco

#CRUD User
from core.views import registroCliente

#CRUD Vagas
from core.views import cadastroVaga, listagemVagas, alteraVaga, excluiVaga

#CRUD Pontos
from core.views import cadastroPonto, listagemPontos, alteraPonto, excluiPonto

#CRUD Carros
from core.views import cadastroCarro, listagemCarros, alteraCarro, excluiCarro

#CRUD Reservas
from core.views import cadastroReserva, listagemReservas, alteraReserva, excluiReserva

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/registrar/', Registrar.as_view(), name='url_registrar'),
    path('', home, name='url_principal'),
    path('accounts/registrar/', registroCliente, name='url_registrar'),
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
    path('listagemReserva/', listagemReservas, name='url_listagem_reservas'),
    path('alteraReserva/<int:id>/', alteraReserva, name='url_altera_reserva'),
    path('excluiReserva/<int:id>/', excluiReserva, name='url_exclui_reserva'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
