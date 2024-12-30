from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django import forms


# Create your models here.
class Ingresso(forms.Form):
    durata_turno_ore = forms.IntegerField(label='Ore durata turno',
                                          required=False,
                                          validators=[MinValueValidator(1), MaxValueValidator(12)])
    durata_turno_minuti = forms.IntegerField(label='Minuti durata turno',
                                             required=False,
                                             validators=[MinValueValidator(0), MaxValueValidator(59)])
    ora_ingresso = forms.IntegerField(label='Ora ingresso',
                                      required=False,
                                      validators=[MinValueValidator(0), MaxValueValidator(23)])
    minuti_ingresso = forms.IntegerField(label='Minuti ingresso',
                                         required=False,
                                         validators=[MinValueValidator(0), MaxValueValidator(59)])
    minuti_pausa = forms.IntegerField(label='Minuti pausa',
                                      required=False,
                                      validators=[MinValueValidator(0), MaxValueValidator(180)])

    def __str__(self):
        return ('Durata turno ore: ' + str(self.durata_turno_ore) +
                '\ndurata turno minuti: ' + str(self.durata_turno_minuti) +
                '\nIngresso: ' + str(self.ora_ingresso) + ' e ' + str(self.minuti_ingresso) +
                '\nPausa: ' + str(self.minuti_pausa))

class Uscita(models.Model):
    ora_uscita = models.IntegerField()
    minuti_uscita = models.IntegerField()

    def __str__(self):
        return ('Uscita: ' + str(self.ora_uscita) + ' e ' + str(self.minuti_uscita))