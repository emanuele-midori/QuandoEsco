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
            return redirect('login')
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
                return redirect('calcola_uscita')

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
                            'messaggio_success': messaggio_success})

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
            giornata.user = request.user  # Assegna l'utente loggato
            giornata.save()  # Salva l'oggetto con l'utente
            return redirect('salva_giornata')
        else:
            print('FORM NOT VALID')
            print(form.errors)  # Stampa errori di validazione per debug
            return render(request, 'salva_giornata.html', {'form': form})
