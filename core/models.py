from django.db import models
from django.contrib.auth.models import User


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
    ocupado = models.BooleanField(verbose_name="Ocupado?")
    recarga = models.BooleanField(verbose_name="Possui recarga?")
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, verbose_name='Endereço')

    def __str__(self):
        return self._check_id_field()

    class Meta:
        verbose_name_plural = "Vagas"


# Classe dos carros
class Carro(models.Model):
    placa = models.CharField(max_length=7, verbose_name='Placa')
    marca = models.CharField(max_length=20, verbose_name='Marca')
    modelo = models.CharField(max_length=20, verbose_name='Modelo')
    cor = models.CharField(max_length=20, verbose_name='Cor')
    vaga = models.ForeignKey(Vaga, on_delete=models.DO_NOTHING, verbose_name='Vaga')

    def __str__(self):
        return self.placa

    class Meta:
        verbose_name_plural = 'Carros'


# Classe geral de pessoas
class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(max_length=50, verbose_name='Email')
    identificacao = models.IntegerField(default=0, verbose_name='Identificação')
    telefone = models.IntegerField(default=0, verbose_name='Identificação')
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, verbose_name='Endereço')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='User')  # verificar se é assim

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Pessoas'


# ver como pegar o nome da superclasse pessoa
class Administrador(Pessoa):
    matricula = models.IntegerField(default=0, verbose_name='Matrícula')
    cargo = models.CharField(max_length=100, verbose_name='Nome')

    def __str__(self):
        return f"{self.matricula}, {self.cargo}"

    class Meta:
        verbose_name_plural = 'Administradores'


class Prestador(Pessoa):
    registro = models.IntegerField(default=0, verbose_name='Registro')
    especialidade = models.CharField(max_length=50, verbose_name='Especialidade')

    def __str__(self):
        return f"{Pessoa.nome}, {self.registro}, {self.especialidade}"

    class Meta:
        verbose_name_plural = 'Prestadores'


class Cliente(Pessoa):
    dataNascimento = models.DateField(verbose_name='Data de Nascimento')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Clientes'


# ________________________________________


# Classes dos pontos de recarga e de apoio


class PontoDeApoio(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    terceirizado = models.BooleanField(verbose_name="Terceirizado?")
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, verbose_name='Endereço')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Pontos de Apoio"


class Reserva(models.Model):
    dataInicio = models.DateTimeField(verbose_name='Data de início')
    dataFim = models.DateTimeField(verbose_name='Data de fim')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    tempoReserva = models.TimeField(verbose_name='Tempo de reserva')

    def __str__(self):
        return f"{self.dataInicio} - {self.dataFim} - {self.valor}"

    class Meta:
        verbose_name_plural = "Reservas"

# Classes de eventos
class Evento (models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do evento')
    tipo = models.CharField(max_length=50, verbose_name='Tipo')
    criticidade = models.CharField(max_length=50, verbose_name='Criticidade')

    def __str__(self):
        return {self.nome}

    class Meta:
        verbose_name_plural = "Eventos"

class EventoCarro (models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.DO_NOTHING, verbose_name='Carro')
    evento = models.ForeignKey(Evento, on_delete=models.DO_NOTHING, verbose_name='Evento')
    dataInicio = models.DateTimeField(verbose_name='Data de início')
    dataFim = models.DateTimeField(verbose_name='Data de fim')
    resolvido = models.BooleanField(verbose_name="Resolvido?")
