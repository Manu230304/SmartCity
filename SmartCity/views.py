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
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordConfermata = request.POST.get('confirmPassword')
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        municipalita_codice_postale = request.POST.get('codice_postale')
        ruolo = request.POST.get('ruolo')

        if not email or not password or not passwordConfermata or not nome or not cognome or not municipalita_codice_postale:
            context['error_message'] = "Tutti i campi devono essere compilati."
            return render(request, 'registrazione.html', context)


        if Utente.objects.filter(email=email).exists():
            context['error_message'] = "Utente già registrato"
            return render(request, 'registrazione.html', context)

        elif (password != passwordConfermata):
            context['error_message'] = "Le due password non coincidono"
            return render(request, 'registrazione.html', context)


        else:

            municipalita = Municipalita.objects.get(codice_postale=municipalita_codice_postale)
            hashed_password = make_password(password)
            utente = Utente(Nome=nome, Cognome=cognome,email=email, password=hashed_password, municipalita_id=municipalita_codice_postale,  ruolo=ruolo)
            utente.save()
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
