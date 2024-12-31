from datetime import datetime, timedelta
from django.shortcuts import render

from MyApp.models import Ingresso


# Create your views here.
def homepage(request):
    data_uscita = datetime.now()
    messaggio_info = "Compila il form e premi il pulsante \'Quando Esco?\'"
    messaggio_success = None
    messaggio_danger = None
    messaggio_warning = None

    if request.method == 'POST':
        form = Ingresso(request.POST)
        if form.is_valid():
            durata_turno_ore = form.cleaned_data['durata_turno_ore']
            durata_turno_minuti = form.cleaned_data['durata_turno_minuti']
            data_ingresso = form.cleaned_data['ingresso']
            minuti_pausa = form.cleaned_data['durata_pausa_minuti']

            print("Durata turno ore:", durata_turno_ore)
            print("Durata turno minuti:", durata_turno_minuti)
            print("Durata pausa minuti:", minuti_pausa)

            durata = timedelta(hours=durata_turno_ore, minutes=durata_turno_minuti + minuti_pausa)
            data_uscita = data_ingresso + durata

            print("Ingresso: ", data_ingresso)
            print("Uscita: ", data_uscita)

            now = datetime.now()

            print("Now: ", now)
            # Converto uscita e now in timestamp
            now_timestamp = now.timestamp()
            data_uscita_timestamp = data_uscita.timestamp()
            #Differenza in minuti:
            differenza_minuti = (data_uscita_timestamp  - now_timestamp) / 60
            differenza_minuti -= 60
            print("Differenza minuti: ", differenza_minuti)

            if differenza_minuti <= 0:
                messaggio_success = "Cosa fai ancora qui? E' ora di andare a casa!"
                messaggio_info = None
                messaggio_danger = None
                messaggio_warning = None
            elif differenza_minuti > 0 and differenza_minuti <= 60:
                messaggio_success = "Manca poco, tieni duro!"
                messaggio_info = None
                messaggio_danger = None
                messaggio_warning = None
            elif differenza_minuti > 60 and differenza_minuti <= 240:
                messaggio_warning = "Ne hai ancora per un pò, buon lavoro!"
                messaggio_success = None
                messaggio_info = None
                messaggio_danger = None
            else:
                messaggio_danger = "La giornata è ancora lunga, datti da fare!"
                messaggio_warning = None
                messaggio_success = None
                messaggio_info = None

    else:
        print('Form non popolato')
        form = Ingresso()

    return render(request,
                  'homepage.html',
                  { 'form': form,
                            'uscita': data_uscita,
                            'messaggio_info': messaggio_info,
                            'messaggio_warning':messaggio_warning,
                            'messaggio_danger': messaggio_danger,
                            'messaggio_success': messaggio_success})

