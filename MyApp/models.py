from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Giornata(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    ingresso = models.TimeField()
    uscita = models.TimeField()
    ore_lavorate = models.IntegerField()
    minuti_lavorati = models.IntegerField()
    minuti_pausa = models.IntegerField()

    class Meta:
        unique_together = ('user', 'data')  # Un utente può avere solo una 'Giornata' per ogni data

    def __str__(self):
        return str(self.data) + ' - Ingresso: ' + str(self.ingresso) + ' - Uscita: ' + str(self.uscita)

class Turno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ore_lavoro = models.IntegerField(default=0)  # Ore del turno
    minuti_lavoro = models.IntegerField(default=0)  # Minuti del turno
    minuti_pausa = models.IntegerField(default=0)  # Minuti di pausa

    def __str__(self):
        return f"Turno di {self.user.username}: {self.ore_lavoro} ore, {self.minuti_lavoro} minuti, pausa {self.minuti_pausa} minuti"