from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    STATUS = (
        ('cliente', 'cliente'),
        ('prestador', 'prestador'),
        ('administrador', 'administrador'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='cliente')
    description = models.TextField("Descrição", max_length=600, default='', blank=True)

    def __str__(self):
        return self.username


