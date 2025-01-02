from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

now = datetime.now().replace(second=0, microsecond=0)

# Create your models here.
class Ingresso(forms.Form):
    durata_turno_ore = forms.IntegerField(label='Durata turno ore',
                                          required=False,
                                          initial=8,
                                          validators=[MinValueValidator(0), MaxValueValidator(23)])
    durata_turno_minuti = forms.IntegerField(label='Durata turno minuti',
                                             required=False,
                                             initial=0,
                                             validators=[MinValueValidator(0), MaxValueValidator(59)])
    durata_pausa_minuti = forms.IntegerField(label='Durata pausa minuti',
                                      initial=0,
                                      required=False,
                                      validators=[MinValueValidator(0), MaxValueValidator(180)])
    ingresso = forms.DateTimeField(
        label='Ingresso',
        required=False,
        initial=now,  # Data e ora iniziali
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',  # Bootstrap class
                'type': 'datetime-local',  # HTML5 datetime-local picker
            }
        )
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

