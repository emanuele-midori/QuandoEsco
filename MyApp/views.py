from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from MyApp.forms import Ingresso, RegisterForm, LoginForm, GiornataForm
from MyApp.models import Giornata


# Create your views here.
def registrazione(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registrazione.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registrazione completata correttamente!')
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'registrazione.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Ciao {username.title()}, bentornato!')
                return redirect('homepage')

        # form is not valid or user is not authenticated
        messages.error(request, f'Username o password non validi')
        return render(request, 'login.html', {'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'Utente disconnesso correttamente.')
    return redirect('login')

@login_required()
def homepage(request):
    # Ottieni l'utente loggato
    user = request.user

    # Recupera le ultime 5 giornate dell'utente in ordine cronologico discendente
    giornate = Giornata.objects.filter(user=user).order_by('-data')[:5]

    # Passa le giornate al template
    return render(request, 'homepage.html', {
        'user': user,
        'giornate': giornate,
    })

@login_required
def calcola_uscita(request):
    data_uscita = datetime.now()
    messaggio_info = "Compila il form e premi il pulsante \'Quando Esco?\'"
    messaggio_success = None
    messaggio_danger = None
    messaggio_warning = None
    scroll_to_bottom = False

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
            #differenza_minuti -= 60
            print("Differenza minuti: ", differenza_minuti)

            if differenza_minuti <= 0:
                messaggio_success = "Cosa fai ancora qui? E' ora di andare a casa!"
                messaggio_info = None
                messaggio_danger = None
                messaggio_warning = None
            elif 0 < differenza_minuti <= 60:
                messaggio_success = "Manca poco, tieni duro!"
                messaggio_info = None
                messaggio_danger = None
                messaggio_warning = None
            elif 60 < differenza_minuti <= 240:
                messaggio_warning = "Ne hai ancora per un pò, buon lavoro!"
                messaggio_success = None
                messaggio_info = None
                messaggio_danger = None
            else:
                messaggio_danger = "La giornata è ancora lunga, datti da fare!"
                messaggio_warning = None
                messaggio_success = None
                messaggio_info = None

            scroll_to_bottom = True

    else:
        print('Form non popolato')
        form = Ingresso()

    return render(request,
                  'calcola_uscita.html',
                  { 'form': form,
                            'uscita': data_uscita,
                            'messaggio_info': messaggio_info,
                            'messaggio_warning':messaggio_warning,
                            'messaggio_danger': messaggio_danger,
                            'messaggio_success': messaggio_success,
                            'scroll_to_bottom': scroll_to_bottom,  # Variabile per trigger dello scroll
                    })

@login_required()
def salva_giornata(request):
    if request.method == 'GET':
        print('GET')
        context = {'form': GiornataForm()}
        return render(request, 'salva_giornata.html', context)
    elif request.method == 'POST':
        print('POST')
        form = GiornataForm(request.POST)
        if form.is_valid():
            print('FORM VALID')
            # Controlla se esiste già un record per l'utente e la data
            user = request.user
            data = form.cleaned_data['data']
            if Giornata.objects.filter(user=user, data=data).exists():
                messages.error(request, f"Esiste già un record per il giorno {data}!")
                return redirect('salva_giornata')  # Ritorna al form con l'errore

            # Aggiunge l'utente user presente nella request all'oggetto giornata prima di salvarlo
            giornata = form.save(commit=False)  # Non salvare ancora nel database
            # calcolo ore di lavoro
            ingresso = form.cleaned_data['ingresso']
            uscita = form.cleaned_data['uscita']
            minuti_pausa = form.cleaned_data['minuti_pausa']

            # Crea due oggetti datetime combinando la data con i time
            ingresso_datetime = datetime.combine(data, ingresso)
            uscita_datetime = datetime.combine(data, uscita)

            #uscita deve essere successiva a ingresso
            # Verifica se l'uscita è successiva all'ingresso
            if uscita_datetime <= ingresso_datetime:
                print("Errore: l'uscita deve essere successiva all'ingresso!")
                messages.warning(request, f"Errore: l'uscita deve essere successiva all'ingresso.")
                return render(request, 'salva_giornata.html', {'form': form})

            # Calcola la differenza in minuti totali
            differenza_minuti = int((uscita_datetime - ingresso_datetime).total_seconds() / 60)

            # Sottrai i minuti di pausa
            differenza_effettiva_minuti = differenza_minuti - minuti_pausa

            #la differenza in minuti tra uscita e ingresso deve essere maggiore dei minuti di pausa
            if differenza_effettiva_minuti <=0:
                print("Errore: la pausa non può durare più del turno di lavoro!.")
                messages.warning(request, f"Errore: la pausa non può durare più del turno di lavoro!.")
                return render(request, 'salva_giornata.html', {'form': form})

            # Calcola ore e minuti
            ore_lavorate, minuti_lavorati = divmod(differenza_effettiva_minuti, 60)

            print(f"Differenza effettiva: {ore_lavorate} ore e {minuti_lavorati} minuti")

            giornata.user = request.user  # Assegna l'utente loggato
            giornata.ore_lavorate = ore_lavorate
            giornata.minuti_lavorati = minuti_lavorati
            giornata.save()  # Salva l'oggetto con l'utente
            messages.success(request, f"Giornata di lavoro salvata per il giorno {data} "
                                      f"<br>Ingresso: {ingresso.strftime('%H:%M')}, "
                                      f"<br>Uscita: {uscita.strftime('%H:%M')}, "
                                      f"<br>Ore Lavorate: {ore_lavorate} h, "
                                      f"<br>Minuti Lavorati: {minuti_lavorati} min, "
                                      f"<br>Minuti di Pausa: {minuti_pausa} min ")
            print(f"Differenza effettiva: {ore_lavorate} ore e {minuti_lavorati} minuti")

            return redirect('salva_giornata')
        else:
            print('FORM NOT VALID')
            print(form.errors)  # Stampa errori di validazione per debug
            messages.warning(request, f"Form non valido!")
            return render(request, 'salva_giornata.html', {'form': form})
