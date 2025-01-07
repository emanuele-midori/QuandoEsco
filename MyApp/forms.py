from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from MyApp.models import Giornata

now = datetime.now().replace(second=0, microsecond=0)

# Create your forms here.
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


class GiornataForm(forms.ModelForm):
    class Meta:
        model = Giornata
        fields = ['data', 'ingresso', 'uscita', 'minuti_pausa']
        labels = {
            'data': 'Data',
            'ingresso': 'Ora di ingresso',
            'uscita': 'Ora di uscita',
            'minuti_pausa': 'Minuti di pausa',
        }
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ingresso': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'uscita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'minuti_pausa': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ModificaGiornataForm(forms.ModelForm):
    class Meta:
        model = Giornata
        fields = ['ingresso', 'uscita', 'minuti_pausa']
        labels = {
            'ingresso': 'Ora di ingresso',
            'uscita': 'Ora di uscita',
            'minuti_pausa': 'Minuti di pausa',
        }
        widgets = {
            'ingresso': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'uscita': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'minuti_pausa': forms.NumberInput(attrs={'class': 'form-control'}),
        }