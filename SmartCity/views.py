from contextlib import nullcontext
from operator import truediv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.template.defaultfilters import length

import ProgettoBasi
from SmartCity.models import *


# Create your views here.

def controlloPassword(password):

    caratteriSpeciali = ['*', '$', '!','#']

    numero = False
    carattereSpeciale = False
    letteraMinuscola = False
    letteraMaiuscola = False
    lunghezza = False

    for lettera in password:
        if 'a' <= lettera <= 'z':
            letteraMinuscola = True
        if 'A' <= lettera <= 'Z':
            letteraMaiuscola = True
        if '0' <= lettera <= '9':
            numero = True
        if lettera in caratteriSpeciali:
            carattereSpeciale = True
        if length(password) >= 12:
            lunghezza = True

    if numero and  carattereSpeciale and letteraMinuscola and lunghezza and letteraMaiuscola:
        return True
    else:
        return False

def aggiungi_progetto(request):

    email = request.session.get('utente_email')

    if not email:
        return redirect('login')
    lista_municipalita = Municipalita.objects.all()

    context = {
        'lista_municipalita': lista_municipalita,
        'stati': Progetto.STATO
    }

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descrizione = request.POST.get('descrizione')
        budget = request.POST.get('budget')
        data_inizio = request.POST.get('data_inizio')
        data_fine = request.POST.get('data_fine')
        municipalita_codice_postale = request.POST.get('municipalita')
        municipalita = Municipalita.objects.get(codice_postale=municipalita_codice_postale)


        progetto = Progetto(nome = nome, descrizione =descrizione, budget=budget, data_inizio=data_inizio, codice_postale=municipalita, urbanista_id=email)
        progetto.save()
        print("Progetto Aggiunto")

    return render(request, 'aggiungi_progetto.html', context)



def salva_bio(request):
    if request.method == 'POST':
        email = request.session.get('utente_email')
        utente = Utente.objects.get(email=email)
        urbanista = Urbanista.objects.get(utente=utente)
        bio = request.POST.get('bio')
        context = {

            'success': "Bio aggiornata!"
        }
        if not email:
            return redirect('login')

        urbanista.bio = bio
        urbanista.save()

        return render(request, 'home_urbanista.html', context)
def logout_view(request):
    request.session.flush()  # Cancella tutta la sessione
    return redirect('login')  # Torna alla pagina di login
def home_cittadino(request):
    email = request.session.get('utente_email')

    if not email:
        return redirect('login')

    utente = Utente.objects.get(email=email)
    cittadino = Cittadino.objects.get(utente=utente)

    context = {
        'utente': utente,
        'cittadino': cittadino
    }
    return render(request, 'home_cittadino.html', context)


def profilo_urbanista(request):
    email = request.session.get('utente_email')
    if not email:
        return redirect('login')

    utente = Utente.objects.get(email=email)
    urbanista = Urbanista.objects.get(utente=utente)
    lista_progetti = Progetto.objects.filter(urbanista=urbanista)
    context = {
        'lista_progetti': lista_progetti,
        'utente': utente,
        'urbanista': urbanista
    }
    return render(request, 'profilo_urbanista.html', context)
def home_urbanista(request):
    email = request.session.get('utente_email')
    if not email:
        return redirect('login')


    utente = Utente.objects.get(email=email)
    urbanista = Urbanista.objects.get(utente=utente)
    lista_progetti = Progetto.objects.filter(urbanista=urbanista)
    context = {
        'lista_progetti': lista_progetti,
        'utente': utente,
        'urbanista': urbanista
    }

    return render(request, 'home_urbanista.html', context)

def registrazione(request):


    lista_municipalita = Municipalita.objects.all()
    context = {
        'lista_municipalita': lista_municipalita,
        'ruoli': Utente.Ruoli,
        'livelli': Urbanista.Livelli,
        'qualifiche': Urbanista.QUALIFICHE_URBANISTA,
        'occupazioni': Cittadino.OCCUPAZIONI,
        'specializzazioni': TecnicoComunale.SPECIALIZZAZIONI_TECNICO
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordConfermata = request.POST.get('confirmPassword')
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        municipalita_codice_postale = request.POST.get('codice_postale')
        ruolo = request.POST.get('ruolo')
        municipalita = Municipalita.objects.get(codice_postale=municipalita_codice_postale)

        if not email or not password or not passwordConfermata or not nome or not cognome or not municipalita_codice_postale:
            context['error_message'] = "Tutti i campi devono essere compilati."
            return render(request, 'registrazione.html', context)

        if not controlloPassword(password):
            context['error_message'] = "La password deve essere lunga almeno 12 caratteri e contenere almeno: una lettera maiuscola, una minuscola, un numero e un carattere speciale."
            return render(request, 'registrazione.html', context)

        if Utente.objects.filter(email=email).exists():
            context['error_message'] = "Utente già registrato"
            return render(request, 'registrazione.html', context)

        if (password != passwordConfermata):
            context['error_message'] = "Le due password non coincidono"
            return render(request, 'registrazione.html', context)



        elif(ruolo == 'cittadino'):

            data_di_nascita = request.POST.get('dataNascita')
            aggiornamentoEmail = request.POST.get('aggiornamentiEmail')
            hashed_password = make_password(password)
            occupazione = request.POST.get('occupazione')
            notifiche_email = aggiornamentoEmail == 'on' # Diventa True o False. In Django le checkbox di html vengono passate con 'on' se vengono spuntate

            # notifiche_ email = aggiornamentiEmail == 'on' è l'equivalente di:
            # if aggiornamentoEmail == 'on':
            #    notifiche_email = True
            # else:
            #   notifiche_email = False


            utente = Utente(nome=nome, cognome=cognome, email=email, password=hashed_password, codice_postale=municipalita, ruolo=ruolo)
            utente.save()
            cittadino = Cittadino(utente=utente, data_nascita=data_di_nascita, occupazione=occupazione, notifiche_email=notifiche_email)
            cittadino.save()
            context['success'] = "Registrazione avvenuta con successo"
            return render(request, 'login.html', context)



        elif (ruolo == 'urbanista'):

            livello = request.POST.get('livello')
            qualifica = request.POST.get('qualifica')

            hashed_password = make_password(password)
            utente = Utente(nome=nome, cognome=cognome,email=email, password=hashed_password, codice_postale=municipalita,  ruolo=ruolo)
            utente.save()
            urbanista = Urbanista(utente=utente, tipo=livello, qualifica=qualifica)
            urbanista.save()
            context['success'] = "Registrazione avvenuta con successo"
            return render(request, 'login.html', context)

        elif(ruolo == 'tecnico'):

            specializzazione = request.POST.get('specializzazione')
            numero_matricola = request.POST.get('matricola')
            emailUfficio = request.POST.get('emailUfficio')
            telefono_ufficio = request.POST.get('telefono')

            hashed_password = make_password(password)
            utente = Utente(nome=nome, cognome=cognome,email=email, password=hashed_password, codice_postale=municipalita,  ruolo=ruolo)
            utente.save()

            if not telefono_ufficio:
                tecnico = TecnicoComunale(utente = utente,specializzazione = specializzazione, numero_matricola=numero_matricola, email_ufficio= emailUfficio)
                tecnico.save()
                context['success'] = "Registrazione avvenuta con successo"
                return render(request, 'login.html', context)
            else:
                tecnico = TecnicoComunale(utente=utente, specializzazione=specializzazione, numero_matricola=numero_matricola, email_ufficio=emailUfficio, telefono_ufficio=telefono_ufficio)
                tecnico.save()
                context['success'] = "Registrazione avvenuta con successo"
                return render(request, 'login.html', context)

    return render(request, 'registrazione.html', context)

def homepage(request):
    return render(request, 'homepage.html')
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Controlla se l'utente esiste in base all'email
        if Utente.objects.filter(email=email).exists():
            utente = Utente.objects.get(email=email)  # Recupera l'istanza dell'utente

            # Verifica la password hashata
            if check_password(password, utente.password) and utente.ruolo == 'cittadino':
                request.session['utente_email'] = utente.email

                # Reindirizza alla home del cittadino
                return redirect('home_cittadino')

            elif check_password(password, utente.password) and utente.ruolo == 'urbanista':
                request.session['utente_email'] = utente.email
                return redirect('home_urbanista')

            else:
                # Password errata
                return render(request, 'login.html', {"error_message": "Password errata"})
        else:
            # Utente non trovato
            return render(request, 'login.html', {"error_message": "Utente non esistente"})

    # GET: Visualizza il form di login
    return render(request, 'login.html')
