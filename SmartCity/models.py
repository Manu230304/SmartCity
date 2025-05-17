from django.db import models

# Create your models here.


class Municipalita(models.Model):

    nome = models.CharField(max_length=50)
    codice_postale = models.CharField(max_length=5, primary_key=True)

# ----------------------------------------------------------------------------------------------------------------------

class Utente(models.Model):

    Ruoli = [
        ('cittadino','Cittadino'),
        ('urbanista','Urbanista'),
        ('tecnico', 'Tecnico')
    ]

    # -----------------------------------------------------------------------
    # Lista di tuple `Ruoli`: definisce le scelte disponibili per il campo `ruolo`.
    # Ogni tupla contiene una coppia: il nome del valore memorizzato nel database
    # e il valore da visualizzare nell'interfaccia front-end (ad esempio, un form).
    # ------------------------------------------------------------------------

    nome = models.CharField(max_length=70)
    cognome = models.CharField(max_length=70)
    email = models.EmailField(max_length=150, primary_key=True)
    password = models.CharField(max_length=50)
    codice_postale = models.ForeignKey(Municipalita, on_delete=models.CASCADE, related_name='utenti')
    ruolo = models.CharField(max_length=20, choices=Ruoli)

    # Il parametro 'choices' definisce una lista di opzioni possibili per il campo.
    # Ogni opzione è una tupla (valore_salvato, valore_visualizzato).
    # Nel database viene salvato il primo elemento (valore_salvato),
    # mentre nei form o nell'admin Django mostra il secondo elemento (valore_visualizzato),
    # limitando così i valori ammessi a quelli specificati nella lista 'Ruoli'.


# ----------------------------------------------------------------------------------------------------------------------

class Cittadino(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, primary_key=True, related_name='cittadino') # OneToOne crea una relazione 1 a 1. Quindi collego le specializzazioni alla tabella padre "Utente"
                                                                                                                # Posso usare quindi per esempio: Cittadino.utente.email, Urbanista.utente.codice_postale ecc...
                                                                                                                # Mettendo il related name posso anche fare Utente.cittadino ecc...
    data_nascita = models.DateField()
    data_registrazione = models.DateField()
    numero_cellulare = models.CharField(max_length=20, null=True)
    notifiche_sms = models.BooleanField(default=False, null=True)
    punteggio_attivita = models.IntegerField(default=0)

# ----------------------------------------------------------------------------------------------------------------------

class Urbanista(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, primary_key=True, related_name='urbanista')
    tipo = models.CharField(max_length=100)
    qualifica = models.CharField(max_length=120)
    bio = models.TextField()
    valutazione_media = models.FloatField(default=0)

# ----------------------------------------------------------------------------------------------------------------------

class TecnicoComunale(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, primary_key=True, related_name='tecnicocomunale')
    specializzazione = models.CharField(max_length=155)
    numero_matricola = models.CharField(max_length=16)
    email_ufficio = models.EmailField()
    telefono_ufficio = models.CharField(max_length=20, null=True)

# ----------------------------------------------------------------------------------------------------------------------

class Progetto(models.Model):
    ID_Progetto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descrizione = models.TextField()
    budget = models.FloatField()
    stato = models.CharField(max_length=20)
    approvato = models.BooleanField()
    data_pubblicazione = models.DateField()
    data_inizio = models.DateField(null=True)
    data_fine = models.DateField(null=True)
    urbanista = models.ForeignKey(Urbanista, on_delete=models.CASCADE, related_name='progetti') # quindi potrei usare urbanista.progetti
    codice_postale = models.ForeignKey(Municipalita, on_delete=models.CASCADE, related_name='progetti')

# ----------------------------------------------------------------------------------------------------------------------

class FaseProgetto(models.Model):
    ID_FaseProgetto = models.AutoField(primary_key=True)
    Titolo_FaseProgetto = models.CharField(max_length=40)
    descrizione_fase = models.TextField()
    data_inizioFase_stimata = models.DateField()
    data_fineFase_stimata = models.DateField()
    data_Inizio = models.DateField(null=True)
    data_Fine = models.DateField(null=True)
    completata = models.BooleanField()
    note_tecniche = models.TextField(null=True)
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name='fasi') # oppure, progetto.fasi

# ----------------------------------------------------------------------------------------------------------------------

class Gestisce(models.Model):
    fase = models.ForeignKey(FaseProgetto, on_delete=models.CASCADE, related_name='gestioni') # fase.gestioni
    tecnico = models.ForeignKey(TecnicoComunale, on_delete=models.CASCADE, related_name='gestioni') # tecnico.gestioni

    class Meta:
        unique_together = ('fase', 'tecnico')    # Garantisce che per ogni fase di progetto un tecnico possa essere associato una sola volta,
                                                 # evitando duplicati nella tabella di gestione (relazione molti-a-molti tramite modello esplicito)

# ----------------------------------------------------------------------------------------------------------------------

class Votazione(models.Model):
    ID_Votazione = models.AutoField(primary_key=True)
    cittadino = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='votazioni') # cittadino.votazioni
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name='votazioni') # progetto.votazioni
    data_voto = models.DateField()
    scelta = models.BooleanField()

# ----------------------------------------------------------------------------------------------------------------------

class Recensione(models.Model):
    ID_Recensione = models.AutoField(primary_key=True)
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name='recensioni')
    cittadino = models.ForeignKey(Cittadino, on_delete=models.CASCADE, related_name='recensioni')
    voto = models.IntegerField()
    descrizione = models.TextField(null=True)

