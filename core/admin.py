from django.contrib import admin
from core.models import Endereco, Vaga, Carro, Pessoa, Administrador
from core.models import Prestador, Cliente, PontoDeApoio, Reserva, Evento, EventoCarro


admin.site.register(Endereco)
admin.site.register(Vaga)
admin.site.register(Carro)
admin.site.register(Pessoa)
admin.site.register(Administrador)
admin.site.register(Prestador)
admin.site.register(Cliente)
admin.site.register(PontoDeApoio)
admin.site.register(Reserva)
admin.site.register(Evento)
admin.site.register(EventoCarro)
