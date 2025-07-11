from django.db import models


from datetime import timedelta
# Create your models here.


class Municipalita(models.Model):

    nome = models.CharField(max_length=50)
    codice_postale = models.CharField(max_length=5, primary_key=True)

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------

class Cittadino(models.Model):
    class Ruolo(models.TextChoices):
        URBANISTA = 'Urbanista'
        Tecnico_Comunale = 'Tecnico_Comunale'



    OCCUPAZIONI = [
        ('studente', 'Studente'),
        ('impiegato', 'Impiegato'),
        ('libero_professionista', 'Libero Professionista'),
        ('disoccupato', 'Disoccupato'),
        ('pensionato', 'Pensionato'),
        ('casalinga', 'Casalinga/o'),
        ('altro', 'Altro')
    ]

    Livelli = [
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('esperto', 'Esperto'),

    ]

    QUALIFICHE_URBANISTA = [
        ("laurea_triennale_urbanistica", "Laurea triennale in Urbanistica"),
        ("laurea_magistrale_pianificazione", "Laurea magistrale in Pianificazione Territoriale"),
        ("master_urbanistica", "Master in Urbanistica e Pianificazione Urbana"),
        ("dottorato_scienze_urbanistiche", "Dottorato in Scienze Urbanistiche"),
        ("abilitazione_professionale", "Abilitazione professionale all’esercizio della professione di Urbanista"),
        ("certificazione_gis", "Certificazione in GIS (Geographic Information Systems)"),
        ("corso_rigenerazione", "Corso di specializzazione in Rigenerazione Urbana"),
        ("esperto_sostenibilita", "Esperto in Sostenibilità e Pianificazione Ambientale"),
        ("esperto_mobilita", "Esperto in Mobilità Urbana e Trasporti"),
        ("certificazione_pmp", "Certificazione in Project Management (es. PMP)"),
        ("esperto_politiche_abitative", "Esperto in Politiche Abitative e Sociali"),
        ("esperto_normativa", "Esperto in Normativa Urbanistica e Edilizia"),

    ]

    SPECIALIZZAZIONI_TECNICO = [
        ("manutenzione", "Manutenzione Infrastrutturale"),
        ("energia", "Gestione Energetica"),
        ("ambiente", "Gestione Rifiuti e Ambiente"),
        ("qualita", "Controllo Qualità di Aria e Acqua"),
        ("smart_city", "Sistemi Smart City"),
        ("edilizia_pubblica", "Tecnico per l’Edilizia Pubblica"),
        ("informatica", "Tecnologie Informatiche"),
        ("videosorveglianza", "Sicurezza e Videosorveglianza"),
        ("mobilita", "Mobilità e Trasporti"),
        ("emergenze", "Tecnico per l’Emergenza e Protezione Civile"),
    ]


    # Attributi Cittadino
    nome = models.CharField(max_length=70)
    cognome = models.CharField(max_length=70)
    email = models.EmailField(max_length=150, primary_key=True)
    password = models.CharField(max_length=128)
    codice_postale = models.ForeignKey(Municipalita, on_delete=models.CASCADE)
    occupazione = models.CharField(max_length=70, choices=OCCUPAZIONI, default=OCCUPAZIONI[0], null=True)
    data_nascita = models.DateField()
    data_registrazione = models.DateTimeField(auto_now_add=True)
    notifiche_email = models.BooleanField(default=False, null=True)
    punteggio_attivita = models.IntegerField(default=0)
    ruolo = models.CharField(max_length=30, choices=Ruolo.choices, default="Cittadino")

    #Attributi Tecnico
    specializzazione = models.CharField(max_length=155, choices=SPECIALIZZAZIONI_TECNICO, null=True)
    numero_matricola = models.CharField(max_length=16, null=True)
    email_ufficio = models.EmailField(null=True)
    telefono_ufficio = models.CharField(max_length=15, null=True)

    #Attributi Urbanista
    tipo = models.CharField(max_length=100, choices=Livelli, null=True)
    qualifica = models.CharField(max_length=120, choices=QUALIFICHE_URBANISTA, null=True)
    bio = models.TextField(null=True)
    valutazione_media = models.FloatField(default=0, null=True)



# ----------------------------------------------------------------------------------------------------------------------

class Progetto(models.Model):

    STATO = [

    ('in_valutazione', 'In valutazione'),
    ('in_votazione', 'In votazione'),
    ('concluso', 'Concluso'),
    ('in_corso', 'In Corso'),
    ('approvato', 'Approvato'),
    ('rifiutato', 'Rifiutato'),
]


    ID_Progetto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descrizione = models.TextField()
    budget = models.FloatField()
    stato = models.CharField(max_length=20, choices=STATO, default='in_valutazione')
    data_pubblicazione = models.DateField(auto_now_add=True)
    data_inizio = models.DateField(null=True)
    data_fine = models.DateField(null=False)
    urbanista = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='progetti_urbanista') # quindi potrei usare urbanista.progetti
    codice_postale = models.ForeignKey(Municipalita, on_delete=models.CASCADE, related_name='progetti')
    immagine = models.ImageField(upload_to='progetti/' , null=True, blank=True)
    totale_voti = models.PositiveIntegerField(default=0)
    data_fine_effettiva = models.DateField(default=None, null=True)
    tecnico_approvatore = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='progetti_tecnico_approvatore', default=None, null=True) # Inizialmente non abbiamo un tecnico approvato, quando viene aggiunto il progetto

# ----------------------------------------------------------------------------------------------------------------------




class FaseProgetto(models.Model):

    FASI = [

        ('Progettazione_dettagliata', 'Progettazione dettagliata'),
        ('Approvazione_e_autorizzazioni', 'Approvazione e autorizzazioni'),
        ('Esecuzione_lavori', 'Esecuzione lavori'),
        ('Controllo_qualità_collaudo', 'Controllo qualità e collaudo'),
        ('Consegna_progetto', 'Consegna e chiusura progetto'),
    ]


    ID_FaseProgetto = models.AutoField(primary_key=True)
    Titolo_FaseProgetto = models.CharField(max_length=70, choices=FASI)
    descrizione_fase = models.TextField()
    data_inizioFase_stimata = models.DateField()
    data_fineFase_stimata = models.DateField()
    data_Inizio = models.DateField(null=True)
    data_Fine = models.DateField(null=True)
    completata = models.BooleanField(default=False)
    note_tecniche = models.TextField(null=True)
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name='fasi') # oppure, progetto.fasi

# ----------------------------------------------------------------------------------------------------------------------

class Gestisce(models.Model):
    fase = models.ForeignKey(FaseProgetto, on_delete=models.CASCADE, related_name='gestioni') # fase.gestioni
    tecnico = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='gestioni') # tecnico.gestioni

    class Meta:
        unique_together = ('fase', 'tecnico')    

# ----------------------------------------------------------------------------------------------------------------------

class Vota(models.Model):
    ID_Votazione = models.AutoField(primary_key=True)
    cittadino = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='votazioni') # cittadino.votazioni
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name='votazioni') # progetto.votazioni
    data_voto = models.DateField(auto_now_add=True)

# ----------------------------------------------------------------------------------------------------------------------

class Recensisce(models.Model):

    STATO_RECENSIONE = [
        ("recensito", "Recensito"),
        ("non_recensito", "Non Recensito"),

    ]


    ID_Recensione = models.AutoField(primary_key=True)
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name='recensioni')
    cittadino = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='recensioni')
    voto = models.IntegerField()
    descrizione = models.TextField(null=True)
    stato_recensione = models.CharField(choices=STATO_RECENSIONE, max_length=20, default="non_recensito")



class Badge(models.Model):

    ID_Badge = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=255)
    soglia_punti = models.IntegerField()


class Ottiene(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='ottiene')
    cittadino = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='ottiene')
