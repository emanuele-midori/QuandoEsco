from datetime import time

from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms


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
    ingresso = forms.TimeField(label='Ingresso',
                               required = False,
                               initial= time(8, 0),
                               widget=forms.TimeInput(
                                    attrs={
                                        'class': 'form-control',  # Bootstrap class
                                        'type': 'time',  # HTML5 time picker
                                        }
                                    )
                               )
    minuti_pausa = forms.IntegerField(label='Durata pausa minuti',
                                      initial= 0,
                                      required=False,
                                      validators=[MinValueValidator(0), MaxValueValidator(180)])

    def __str__(self):
        return ('Durata turno ore: ' + str(self.durata_turno_ore) +
                '\ndurata turno minuti: ' + str(self.durata_turno_minuti) +
                '\nIngresso: ' + str(self.ingresso.hour) + ' e ' + str(self.ingresso.minutes) +
                '\nPausa: ' + str(self.minuti_pausa))