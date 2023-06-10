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
from core.views import cadastroCliente, registroCliente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registrar/', Registrar.as_view(), name='url_registrar'),
    path('', home, name='url_principal'),
    #path('cadastroCliente/', cadastroCliente, name='url_cadastro_cliente'),
    path('cadastroCliente/', registroCliente, name='url_registro_cliente'),
    path('cadastroEndereco/', cadastroEndereco, name='url_cadastro_endereco'),
    path('listagemEnderecos/', listagemEnderecos, name='url_listagem_enderecos'),
    path('alteraEndereco/<int:id>/', alteraEndereco, name='url_altera_endereco'),
    path('excluiEndereco/<int:id>/', excluiEndereco, name='url_exclui_endereco'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
