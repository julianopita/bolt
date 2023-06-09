from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    STATUS = (
        ('cliente', 'cliente'),
        ('prestador', 'prestador'),
        ('administrador', 'administrador'),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='cliente')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email




