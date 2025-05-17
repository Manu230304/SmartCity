from contextlib import nullcontext

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render

from SmartCity.models import *


# Create your views here.

def registrazione(request):


    lista_municipalita = Municipalita.objects.all()
    context = {
        'lista_municipalita': lista_municipalita,
        'ruoli': Utente.Ruoli,
        'livelli': Urbanista.Livelli,
        'qualifiche': Urbanista.QUALIFICHE_URBANISTA,
        'occupazioni': Cittadino.OCCUPAZIONI,
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
            if check_password(password, utente.password):
                print("Accesso Riuscito")
                return render(request, 'login.html')  # Puoi modificare questa pagina in base alle necessità
            else:
                # Password errata
                return render(request, 'login.html', {"error_message": "Password errata"})
        else:
            # Utente non trovato
            return render(request, 'login.html', {"error_message": "Utente non esistente"})

    # GET: Visualizza il form di login
    return render(request, 'login.html')
