from django.db import models
from users.models import CustomUser
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone
from django.views import generic

User = get_user_model()


# Estende a classe base de usuário
class User(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='usuarioPadrao')


# Classes endereço alimenta várias outras classes
class Endereco(models.Model):
    rua = models.CharField(max_length=100, verbose_name='Rua')
    cidade = models.CharField(max_length=50, verbose_name='Cidade')
    numero = models.IntegerField(default=0, verbose_name='Número')
    bairro = models.CharField(max_length=50, verbose_name='Bairro')
    cep = models.IntegerField(default=0000000, verbose_name='CEP')

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}"

    class Meta:
        verbose_name_plural = 'Endereços'


class Vaga(models.Model):
    nome = models.CharField(default='Vaga', max_length=20, verbose_name='Placa')
    ocupado = models.BooleanField(default=False, verbose_name="Ocupado?")
    recarga = models.BooleanField(verbose_name="Possui recarga?")
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, verbose_name='Endereço')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')

    def delete(self):
        self.isActive = False
        self.save()

    def undelete(self):
        self.isActive = True
        self.save()

    def __str__(self):
        return f"{self.nome} - {self.id}"

    class Meta:
        verbose_name_plural = "Vagas"


# Classe dos carros
class Carro(models.Model):
    placa = models.CharField(max_length=20, verbose_name='Placa')
    marca = models.CharField(max_length=20, verbose_name='Marca')
    modelo = models.CharField(max_length=20, verbose_name='Modelo')
    cor = models.CharField(max_length=20, verbose_name='Cor')
    locacao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00, verbose_name='Valor')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')
    disponivel = models.BooleanField(default=True, blank=True, null=True, verbose_name='Disponível?')
    vaga = models.ForeignKey(Vaga, default=None, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Vaga')

    def delete(self):
       self.isActive = False
       self.vaga = None
       self.disponivel = False
       self.save()

    def undelete(self):
       self.isActive = True
       self.save()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = 'Carros'


# Classe geral de pessoas
class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    identificacao = models.IntegerField(default=0, verbose_name='Identificação')
    telefone = models.IntegerField(default=0, verbose_name='Telefone')
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, verbose_name='Endereço')
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name='User')  # verificar se é assim

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Pessoas'


# ver como pegar o nome da superclasse pessoa
class Administrador(Pessoa):
    matricula = models.IntegerField(default=0, verbose_name='Matrícula')
    cargo = models.CharField(max_length=100, verbose_name='Cargo')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')

    def delete(self):
        self.isActive = False
        self.save()

    def undelete(self):
        self.isActive = True
        self.save()

    def __str__(self):
        return f"{self.matricula}, {self.cargo}"

    class Meta:
        verbose_name_plural = 'Administradores'


class Prestador(Pessoa):
    registro = models.IntegerField(default=0, verbose_name='Registro')
    especialidade = models.CharField(max_length=50, verbose_name='Especialidade')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')

    def __str__(self):
        return f"{Pessoa.nome}, {self.registro}, {self.especialidade}"

    def delete(self):
        self.isActive = False
        self.save()

    def undelete(self):
        self.isActive = True
        self.save()

    class Meta:
        verbose_name_plural = 'Prestadores'


class Cliente(Pessoa):
    dataNascimento = models.DateField(verbose_name='Data de Nascimento')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')

    def __str__(self):
        return self.nome

    def delete(self):
        self.isActive = False
        self.save()

    def undelete(self):
        self.isActive = True
        self.save()

    class Meta:
        verbose_name_plural = 'Clientes'


# ________________________________________


# Classes dos pontos de recarga e de apoio


class PontoDeApoio(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    terceirizado = models.BooleanField(verbose_name="Terceirizado?")
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, verbose_name='Endereço')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')

    def __str__(self):
        return self.nome

    def delete(self):
        self.isActive = False
        self.save()

    def undelete(self):
        self.isActive = True
        self.save()

    class Meta:
        verbose_name_plural = "Pontos de Apoio"


class Reserva(models.Model):
    dataInicio = models.DateTimeField(verbose_name='Data de início')
    dataFim = models.DateTimeField(verbose_name='Data de fim', blank=True, null=True, default=None)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00, verbose_name='Valor')
    tempoReserva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00, verbose_name='Tempo de reserva')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, verbose_name='Cliente')
    carro = models.ForeignKey(Carro, default=None, null=True, on_delete=models.DO_NOTHING, verbose_name='Carro')

    def __str__(self):
        return f"{self.dataInicio} - {self.dataFim} - {self.valor}"

    def delete(self):
        self.isActive = False
        self.save()

    def undelete(self):
        self.isActive = True
        self.save()

    @property
    def status(self):
        now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        if self.dataFim == None and self.dataInicio > now:
            return 'Futuro'
        elif self.dataFim == None and self.dataInicio < now:
            return 'Presente'
        else:
            return 'Passado'

    class Meta:
        verbose_name_plural = "Reservas"


# Classes de eventos
class Evento(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do evento')
    tipo = models.CharField(max_length=50, verbose_name='Tipo')
    criticidade = models.CharField(max_length=50, verbose_name='Criticidade')
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')


    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Eventos"


class EventoCarro(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.DO_NOTHING, verbose_name='Carro')
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING, verbose_name='Evento')
    dataInicio = models.DateTimeField(verbose_name='Data de início')
    dataFim = models.DateTimeField(verbose_name='Data de fim', blank=True, null=True, default=None)
    resolvido = models.BooleanField(default=False, verbose_name="Resolvido?")
    isActive = models.BooleanField(default=True, verbose_name='Ativo?')

    def delete(self):
        self.isActive = False
        self.save()

    def undelete(self):
        self.isActive = True
        self.save()

    @property

    def status(self):
        now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        if self.dataFim == None and self.dataInicio > now:
            return 'Futuro'
        elif self.dataFim == None and self.dataInicio < now:
            return 'Presente'
        else:
            return 'Passado'
