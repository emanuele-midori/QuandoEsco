from django.http import HttpResponse
from django.shortcuts import render

from MyApp.models import Ingresso


# Create your views here.
def homepage(request):
    ora_uscita = 0
    minuti_uscita = 0
    if request.method == 'POST':
        form = Ingresso(request.POST)
        if form.is_valid():
            durata_turno_ore = form.cleaned_data['durata_turno_ore']
            durata_turno_minuti = form.cleaned_data['durata_turno_minuti']
            ora_ingresso = form.cleaned_data['ingresso'].hour
            minuti_ingresso = form.cleaned_data['ingresso'].minute
            minuti_pausa = form.cleaned_data['minuti_pausa']

            print("Durata turno ore:", durata_turno_ore)
            print("Durata turno minuti:", durata_turno_minuti)
            print("Ora di Ingresso:", ora_ingresso)
            print("Minuti di Ingresso:", minuti_ingresso)
            print("Minuti di Pausa:", minuti_pausa)

            # Calcola orario_uscita e minuti_uscita (esempio semplice)
            if (ora_ingresso is not None and minuti_ingresso is not None and minuti_pausa is not None):
                # Ora ingresso + Ore turno

                ora_uscita_temp = ora_ingresso + durata_turno_ore

                minuti_uscita_temp = minuti_ingresso + durata_turno_minuti + minuti_pausa

                if (minuti_uscita_temp < 60):
                    ora_uscita = ora_uscita_temp
                    minuti_uscita = minuti_uscita_temp
                elif (minuti_uscita_temp == 60):
                    ora_uscita = ora_uscita_temp + 1
                    minuti_uscita = 0
                else:
                    # Calcolo delle ore e dei minuti restanti
                    ore_aggiuntive = minuti_uscita_temp // 60
                    ora_uscita = ora_uscita_temp + ore_aggiuntive
                    minuti_uscita = minuti_uscita_temp % 60

                if ora_uscita > 23:
                    ora_uscita -= 24

    else:
        print('Form non popolato')
        form = Ingresso()

    print("Ora di Uscita:", ora_uscita)
    print("Minuti di Uscita:", minuti_uscita)

    uscita = Uscita(ora_uscita, minuti_uscita)

    return render(request,
                  'homepage.html',
                  { 'form': form,
                            'uscita': uscita})

class Uscita:
    def __init__(self, ora_uscita, minuti_uscita):
        self.ora_uscita = ora_uscita
        self.minuti_uscita = minuti_uscita