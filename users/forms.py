from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import CustomUser

class CustomUserCreationForm(ModelForm):

     class Meta:
         model = CustomUser
         fields = ('email', 'password')

# class CustomUserCreationForm(UserCreationForm):
#
#     class Meta:
#         model = CustomUser
#         fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)