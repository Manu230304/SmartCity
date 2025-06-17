from contextlib import nullcontext
from operator import truediv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import length
from django.contrib import messages
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

    email = request.session.get('cittadino_email')

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
        immagine = request.FILES.get('immagine')

        if immagine:
         progetto = Progetto(nome = nome, descrizione =descrizione, budget=budget, data_inizio=data_inizio, data_fine = data_fine,codice_postale=municipalita, urbanista_id=email, immagine=immagine)
         progetto.save()
         print("Progetto Aggiunto")
        else:
            progetto = Progetto(nome=nome, descrizione=descrizione, budget=budget, data_inizio=data_inizio, data_fine = data_fine, codice_postale=municipalita, urbanista_id=email)
            progetto.save()

    return render(request, 'aggiungi_progetto.html', context)



def salva_bio(request):
    if request.method == 'POST':
        email = request.session.get('cittadino_email')
        cittadino = Cittadino.objects.get(email=email)
        urbanista = Urbanista.objects.get(cittadino=cittadino)
        bio = request.POST.get('bio')
        context = {

            'success': "Bio aggiornata!"
        }
        if not email:
            return redirect('login')

        urbanista.bio = bio
        urbanista.save()

    return redirect("home_urbanista")

def logout_view(request):
    request.session.flush()  # Cancella tutta la sessione
    return redirect('login')  # Torna alla pagina di login
def homepage_cittadino(request):
    email = request.session.get('cittadino_email')

    if not email:
        return redirect('login')

    cittadino = Cittadino.objects.get(email=email)

    context = {
        'cittadino': cittadino,

    }


    return render(request, 'homepage_cittadino.html', context)


def profilo_urbanista(request):
    email = request.session.get('cittadino_email')
    if not email:
        return redirect('login')

    cittadino = Cittadino.objects.get(email=email)
    urbanista = Urbanista.objects.get(cittadino=cittadino)
    context = {
        'cittadino': cittadino,
        'urbanista': urbanista
    }
    return render(request, 'profilo_urbanista.html', context)
def home_urbanista(request):
    email = request.session.get('cittadino_email')
    if not email:
        return redirect('login')


    cittadino = Cittadino.objects.get(email=email)
    urbanista = Urbanista.objects.get(cittadino=cittadino)
    lista_progetti = Progetto.objects.filter(urbanista=urbanista)
    context = {
        'lista_progetti': lista_progetti,
        'cittadino': cittadino,
        'urbanista': urbanista
    }

    return render(request, 'home_urbanista.html', context)

def registrazione(request):


    lista_municipalita = Municipalita.objects.all()
    context = {
        'lista_municipalita': lista_municipalita,
        'ruoli': Cittadino.RUOLI,
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
        aggiornamentoEmail = request.POST.get('aggiornamentiEmail')
        notifiche_email = aggiornamentoEmail == 'on'
        hashed_password = make_password(password)
        data_nascita_str = request.POST.get('dataNascita')

        if not email or not password or not passwordConfermata or not nome or not cognome or not municipalita_codice_postale:
            context['error_message'] = "Tutti i campi devono essere compilati."
            return render(request, 'registrazione.html', context)

        if not controlloPassword(password):
            context['error_message'] = "La password deve essere lunga almeno 12 caratteri e contenere almeno: una lettera maiuscola, una minuscola, un numero e un carattere speciale."
            return render(request, 'registrazione.html', context)

        if Cittadino.objects.filter(email=email).exists():
            context['error_message'] = "Cittadino già registrato"
            return render(request, 'registrazione.html', context)

        if (password != passwordConfermata):
            context['error_message'] = "Le due password non coincidono"
            return render(request, 'registrazione.html', context)



        elif(ruolo == 'altro'):
            occupazione = request.POST.get('occupazione')
            # Diventa True o False. In Django le checkbox di html vengono passate con 'on' se vengono spuntate

            # notifiche_ email = aggiornamentiEmail == 'on' è l'equivalente di:
            # if aggiornamentoEmail == 'on':
            #    notifiche_email = True
            # else:
            #   notifiche_email = False


            cittadino = Cittadino(nome=nome, cognome=cognome, email=email, password=hashed_password, codice_postale=municipalita, data_nascita=data_nascita_str, occupazione=occupazione, notifiche_email=notifiche_email)
            cittadino.save()
            context['success'] = "Registrazione avvenuta con successo"
            return render(request, 'login.html', context)



        elif (ruolo == 'urbanista'):

            livello = request.POST.get('livello')
            qualifica = request.POST.get('qualifica')

            hashed_password = make_password(password)
            cittadino = Cittadino(nome=nome, cognome=cognome,email=email, password=hashed_password, codice_postale=municipalita,  occupazione=ruolo, data_nascita=data_nascita_str)
            cittadino.save()
            urbanista = Urbanista(cittadino=cittadino, tipo=livello, qualifica=qualifica)
            urbanista.save()
            context['success'] = "Registrazione avvenuta con successo"
            return render(request, 'login.html', context)

        elif(ruolo == 'tecnico_comunale'):

            specializzazione = request.POST.get('specializzazione')
            numero_matricola = request.POST.get('matricola')
            emailUfficio = request.POST.get('emailUfficio')
            telefono_ufficio = request.POST.get('telefono')

            hashed_password = make_password(password)
            cittadino = Cittadino(nome=nome, cognome=cognome,email=email, password=hashed_password, codice_postale=municipalita,  occupazione=ruolo, data_nascita=data_nascita_str)
            cittadino.save()

            if not telefono_ufficio:
                tecnico = TecnicoComunale(cittadino = cittadino,specializzazione = specializzazione, numero_matricola=numero_matricola, email_ufficio= emailUfficio)
                tecnico.save()
                context['success'] = "Registrazione avvenuta con successo"
                return render(request, 'login.html', context)
            else:
                tecnico = TecnicoComunale(cittadino=cittadino, specializzazione=specializzazione, numero_matricola=numero_matricola, email_ufficio=emailUfficio, telefono_ufficio=telefono_ufficio)
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
        if Cittadino.objects.filter(email=email).exists():
            cittadino = Cittadino.objects.get(email=email)  # Recupera l'istanza dell'cittadino

            # Verifica la password hashata
            if check_password(password, cittadino.password) and cittadino.occupazione == 'urbanista':
                request.session['cittadino_email'] = cittadino.email
                return redirect('home_urbanista')



            elif check_password(password, cittadino.password) and cittadino.occupazione == 'tecnico_comunale':
                request.session['cittadino_email'] = cittadino.email
                return redirect('home_tecnico')

            elif check_password(password, cittadino.password) and (cittadino.occupazione == 'impiegato' or cittadino.occupazione == 'studente' or cittadino.occupazione == 'libero_professionista' or cittadino.occupazione == 'disoccupato' or cittadino.occupazione == 'pensionato' or cittadino.occupazione == 'casalinga' or cittadino.occupazione == 'altro'):
                request.session['cittadino_email'] = cittadino.email
                return redirect('homepage_cittadino')

            else:
                # Password errata
                return render(request, 'login.html', {"error_message": "Password errata"})
        else:
            # Cittadino non trovato
            return render(request, 'login.html', {"error_message": "Cittadino non esistente"})

    # GET: Visualizza il form di login
    return render(request, 'login.html')

def progetti_votabili(request):

    email = request.session.get('cittadino_email')

    if not email:
        return redirect('login')

    cittadino = Cittadino.objects.get(email=email)
    cittadino_codice = cittadino.codice_postale

    if cittadino.occupazione == 'urbanista':
        urbanista = Urbanista.objects.get(cittadino=cittadino)

        lista_progetti = Progetto.objects.filter(stato='approvato').exclude(urbanista=urbanista)

        context = {
        'lista_progetti': lista_progetti,
        'cittadino': cittadino,
        'urbanista': urbanista
        }

        return render(request, 'progetti_votabili.html', context)

    if cittadino.occupazione == 'impiegato' or cittadino.occupazione == 'studente' or cittadino.occupazione == 'libero_professionista' or cittadino.occupazione == 'disoccupato' or cittadino.occupazione == 'pensionato' or cittadino.occupazione == 'casalinga' or cittadino.occupazione == 'altro':

        lista_progetti = Progetto.objects.filter(stato='in_votazione',codice_postale_id=cittadino_codice)
        context = {
        'lista_progetti': lista_progetti,
        'cittadino': cittadino,
        }

        return render(request, 'progetti_votabili.html', context)

def profilo_urbanista_pubblico(request, email):
    email_sessione = request.session.get('cittadino_email')
    urbanista_selezionato = get_object_or_404(Urbanista, cittadino__email=email)
    cittadino = Cittadino.objects.get(email=email_sessione)
    ruolo = cittadino.occupazione

    # Prova a cercare un oggetto Urbanista collegato a un Cittadino che ha quella email.
    # Se lo trova, lo salva nella variabile urbanista_selezionato.

    context = {

        'urbanista': urbanista_selezionato,
        'ruolo': ruolo
    }
    return render(request, 'profilo_urbanista_pubblico.html', context)

def home_tecnico(request):
    email = request.session.get('cittadino_email')

    if not email:
        return redirect('login')

    cittadino = Cittadino.objects.get(email=email)
    tecnico = TecnicoComunale.objects.get(cittadino=cittadino)
    municipalita = tecnico.cittadino.codice_postale



    # Seleziona solo i progetti che:
    # - sono stati proposti da urbanisti il cui cittadino è nella stessa municipalità del tecnico
    # - sono nello stato "in_valutazione"
    progetti_in_valutazione = Progetto.objects.filter(codice_postale=municipalita, stato = "in_valutazione")

    context = {
        'progetti': progetti_in_valutazione,
        'cittadino': tecnico.cittadino
    }
    return render(request, 'home_tecnico.html', context)

def profilo_tecnico(request):
    email = request.session.get('cittadino_email')
    if not email:
        return redirect('login')

    cittadino = Cittadino.objects.get(email=email)
    tecnico = TecnicoComunale.objects.get(cittadino=cittadino)

    context = {
        'cittadino': cittadino,
        'tecnico': tecnico

    }

    return render(request, 'profilo_tecnico.html', context)

def valuta_progetto(request):
    email = request.session.get('cittadino_email')
    if not email:
        return redirect('login')

    if request.method == 'POST':
        progetto_id = request.POST.get('progetto_id')
        azione = request.POST.get('azione')



        if(azione == 'approva'):
            progetto = Progetto.objects.get(ID_Progetto=progetto_id)
            progetto.stato = 'in_votazione'
            progetto.save()
            return redirect( 'home_tecnico')

        if (azione == 'rifiuta'):
            progetto = Progetto.objects.get(ID_Progetto=progetto_id)
            progetto.stato = 'rifiutato'
            progetto.save()

        return redirect('home_tecnico')


def vota_progetto(request):

    if request.method == 'POST':

        email = request.session.get('cittadino_email')
        if not email:
            return redirect('login')

        cittadino = Cittadino.objects.get(email=email)
        progetto_id = request.POST.get('progetto_id')
        progetto = Progetto.objects.get(ID_Progetto=progetto_id)

        esiste = Votazione.objects.filter(cittadino=cittadino,
                                          progetto=progetto).exists()  # Esiste una votazione dove questo cittadino ha votato questo progetto?

        if not esiste:
            progetto = Progetto.objects.get(ID_Progetto=progetto_id)
            progetto.totale_voti = progetto.totale_voti + 1
            progetto.save()
            Votazione.objects.create(cittadino=cittadino, progetto=progetto)
            messages.success(request, "Progetto votato con successo!")
            return redirect('progetti_votabili')
        else:
            messages.error(request, "Hai già votato per questo progetto!")
            return redirect('progetti_votabili')


def progetti_approvati(request):
    email = request.session.get('cittadino_email')
    if not email:
        redirect('login')

    cittadino = Cittadino.objects.get(email=email)
    tecnico = TecnicoComunale.objects.get(cittadino=cittadino)

    municipalita = tecnico.cittadino.codice_postale

    progetti = Progetto.objects.filter(codice_postale_id=municipalita, stato = "in_votazione")

    context = {
            'progetti': progetti,
            'cittadino': cittadino
    }

    return render(request, 'progetti_approvati.html', context)


def gestione_fasi(request, progetto_id):

    email = request.session.get('cittadino_email')
    if not email:
        redirect('login')

    cittadino = Cittadino.objects.get(email=email)
    progetto_gestito = Progetto.objects.get(ID_Progetto=progetto_id)
    FasiProgettoGestito = FaseProgetto.objects.filter(progetto=progetto_gestito)

    context = {
        'progetto_gestito': progetto_gestito,
        'cittadino': cittadino,
        'titoli_fase': FaseProgetto.FASI,
        'fasi': FasiProgettoGestito
    }

    if request.method == 'POST':


        titolo_fase = request.POST.get('Titolo_FaseProgetto')
        data_inizio = request.POST.get('data_inizio')
        data_fine = request.POST.get('data_fine')
        data_inizioFaseStimata = request.POST.get('data_inizioFase_stimata')
        data_fineFaseStimata = request.POST.get('data_fineFase_stimata')
        descrizione = request.POST.get('descrizione_fase')
        note_tecniche = request.POST.get('note_tecniche')



        fase_progetto = FaseProgetto(Titolo_FaseProgetto=titolo_fase, descrizione_fase=descrizione, data_inizioFase_stimata = data_inizioFaseStimata, data_fineFase_stimata = data_fineFaseStimata, data_Inizio = data_inizio, data_Fine = data_fine, note_tecniche = note_tecniche, progetto = progetto_gestito)
        fase_progetto.save()

        redirect('gestione_fasi', progetto_id=progetto_id)

    return render(request, 'gestione_fasi.html', context)



def segna_fase_completata(request, fase_id):
    email = request.session.get('cittadino_email')
    if not email:
        return redirect('login')

    if request.method == 'POST':

        fase_progetto = FaseProgetto.objects.get(ID_FaseProgetto=fase_id)

        fase_progetto.completata = True
        fase_progetto.save()



        return redirect('gestione_fasi', progetto_id=fase_progetto.progetto.ID_Progetto)