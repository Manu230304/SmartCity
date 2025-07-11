**Sistema Informativo per la Gestione di Progetti Urbanistici – Smart City Napoli**

Questo progetto mira a realizzare un sistema informativo completo per **modernizzare la gestione dei progetti urbanistici** e **favorire la partecipazione attiva dei cittadini** nella vita della città di Napoli. La web application, sviluppata con il **framework Django** e un **database SQL**, gestisce dinamicamente i dati, autentica gli utenti e offre funzionalità personalizzate in base al ruolo.

Il sistema presenta un elenco dettagliato dei progetti urbanistici, suddivisi per stato (attivi, conclusi, aperti alle votazioni), e include informazioni essenziali quali nome, descrizione, municipalità, date previste, stato e budget. Ogni progetto è associato a una specifica municipalità per riflettere la suddivisione amministrativa del territorio e limitare l'interazione dei cittadini ai progetti della propria zona.

&nbsp;**Indice**

- [Modello Entità/Relazione](https://www.google.com/search?q=%23modello-entit%C3%A0relazione)
- [Funzionalità Principali](https://www.google.com/search?q=%23funzionalit%C3%A0-principali)
- [Tecnologie Utilizzate](https://www.google.com/search?q=%23tecnologie-utilizzate)
- [Installazione](https://www.google.com/search?q=%23installazione)
- [Configurazione del Database](https://www.google.com/search?q=%23configurazione-del-database)
- [Utilizzo](https://www.google.com/search?q=%23utilizzo)
- [Sicurezza](https://www.google.com/search?q=%23sicurezza)
- [Implementazioni Future](https://www.google.com/search?q=%23implementazioni-future)
- [Licenza](https://www.google.com/search?q=%23licenza)

&nbsp;**Modello Entità/Relazione**

Il cuore del sistema è un **database SQL** progettato per centralizzare le informazioni. Inizialmente concepito con un'entità padre Cittadino e due entità figlie (Urbanista, Tecnico Comunale), il modello è stato ottimizzato per incorporare tutti i campi specifici direttamente nella tabella padre Cittadino. Questa scelta semplifica la gestione, migliora l'efficienza delle query (evitando join automatici di Django) e mantiene il controllo logico attraverso un campo ruolo che funge da discriminatore. Gli attributi non pertinenti al ruolo del cittadino vengono lasciati nulli.

**Entità Principali:**

- Municipalità
- Cittadino (con attributi per Urbanista e Tecnico Comunale)
- Progetto
- FaseProgetto
- Badge

**Relazioni:** Sono presenti diverse relazioni N:M e 1:N che garantiscono la coerenza dei dati e la logica operativa del sistema. Tutte i vincoli referenziali sono impostati con l'opzione **ON DELETE CASCADE** per mantenere l'integrità dei dati.

&nbsp;**Funzionalità Principali**

Il sistema supporta un accesso differenziato in base al ruolo dell'utente (Cittadino, Urbanista, Tecnico Comunale), offrendo interfacce e funzionalità personalizzate.

&nbsp;**Registrazione e Autenticazione**

Il sistema permette la **registrazione** e il **login** con gestione dei ruoli. La pagina di registrazione è divisa in tre schede per credenziali, dati personali e dettagli ruolo. Le password sono hashate con SHA-256 e devono rispettare requisiti di sicurezza specifici (min. 12 caratteri, maiuscole, minuscole, numeri, simboli).

&nbsp;**Gestione Progetti Urbanistici**

- **Urbanisti:** Possono proporre e pubblicare nuovi progetti, specificando nome, descrizione, budget, date stimate e municipalità di appartenenza. Possono anche ricevere recensioni che contribuiscono alla loro reputazione.
- **Tecnici Comunali:** Responsabili della gestione dell'avanzamento dei progetti, documentando le fasi. Possono approvare o rifiutare progetti nella loro municipalità, e aprire/chiudere le votazioni. Hanno accesso alle segnalazioni dei Cittadini e possono assegnare fasi di progetto ad altri tecnici del proprio comune.

&nbsp;**Interazione dei Cittadini**

- **Votazione:** I cittadini possono votare per i progetti della propria municipalità che sono aperti alle votazioni. Ogni cittadino può votare una sola volta per progetto. Gli Urbanisti non possono votare i propri progetti.
- **Recensione:** I cittadini possono rilasciare recensioni (con voto e commento) sui progetti conclusi o sugli Urbanisti. Ogni cittadino può lasciare una sola recensione per ciascun progetto, influenzando la valutazione media dell'Urbanista.
- **Segnalazioni:** In caso di avvio dei lavori, i cittadini possono inviare segnalazioni (ritardi, criticità, difformità).
- **Punti Attività e Badge:** Recensioni e voti generano "punti attività". Accumulando punti, i cittadini possono ricevere "badge speciali" e partecipare a "eventi particolari".

&nbsp;**Homepage Personalizzate**

- **Cittadino:** Visualizza il numero di progetti votati, recensioni ricevute e il proprio punteggio attività. Accesso al profilo, ai progetti votabili e alle recensioni.
- **Urbanista:** Oltre alle card del cittadino, visualizza la "Valutazione Media" e l'elenco dei progetti pubblicati.
- **Tecnico Comunale:** Visualizza i progetti in attesa di approvazione nella propria municipalità, può approvarli/rifiutarli e gestire le fasi dei progetti approvati.

**Tecnologie Utilizzate**

| Componente | Tecnologia |
| --- | --- |
| Backend | Django (Python) |
| Database | SQLite |
| Sicurezza | Hashing SHA-256, Sessioni via cookie, Decoratori per permessi, Prevenzione SQL Injection |

&nbsp;**Installazione**

Assicurarsi di avere **Python** installato. **SQLite** è incluso di default con Python e Django.

1. Clonare il repository del progetto.
2. Creare e attivare un ambiente virtuale (raccomandato):
3. Installare le dipendenze:

pip install -r requirements.txt

(Assicurati che un file requirements.txt sia presente nella root del progetto con tutte le dipendenze.)

1. Eseguire le migrazioni del database per creare le tabelle:

python manage.py makemigrations

python manage.py migrate

&nbsp;**Configurazione del Database**

La struttura del database è definita nel file models.py e le tabelle vengono generate automaticamente tramite le migrazioni di Django nel file db.sqlite3 (database di default per SQLite con Django). La tabella Cittadino gestisce i diversi ruoli (Cittadino "base", Urbanista, Tecnico Comunale) tramite un campo ruolo, con attributi specifici che possono essere nulli se non pertinenti al ruolo.

&nbsp;**Utilizzo**

Dopo l'installazione e la configurazione del database, si potrà avviare il server di sviluppo Django:

python manage.py runserver

Bisogna poi aprire il browser all'indirizzo: [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)

Si potrà quindi:

- Creare un nuovo account (Cittadino, Urbanista, Tecnico Comunale).
- Effettuare il login e accedere alle homepage personalizzate per il proprio ruolo.
- **Cittadini:** Votare progetti, recensire progetti conclusi, monitorare il proprio punteggio attività.
- **Urbanisti:** Proporre nuovi progetti, monitorare i propri progetti pubblicati e la propria valutazione media.
- **Tecnici Comunali:** Approvare/rifiutare progetti, gestire le fasi di avanzamento, aprire/chiudere votazioni e risolvere segnalazioni.

&nbsp;**Sicurezza**

Il sistema implementa diverse misure di sicurezza:

- **Hashing delle password:** Le password degli utenti sono hashate utilizzando l'algoritmo **SHA-256** prima di essere memorizzate nel database.
- **Gestione Sessioni:** Utilizzo di sessioni personalizzate per un accesso sicuro e controllato, basato sul ruolo dell'utente autenticato. Le informazioni chiave (is_authenticated, ruolo, cittadino_email) sono salvate in request.session.
- **Controllo degli accessi:** Un decoratore role_required(allowed_roles) viene usato per proteggere le viste, verificando l'autenticazione e il ruolo dell'utente. Se l'accesso non è consentito, viene restituita una risposta 403 Forbidden o l'utente viene reindirizzato alla pagina di login.
- **Prevenzione SQL Injection:** Il sistema evita l'iniezione SQL utilizzando gli **ORM (Object-Relational Mapping)** di Django, che costruiscono query sicure parametrizzando i dati utente e prevenendo l'interpretazione di codice malevolo. È stata implementata anche una login_vulnerabile a scopo di test didattico per dimostrare questo tipo di attacco.

&nbsp;**Implementazioni Future**

Il progetto prevede i seguenti sviluppi futuri:

- Invio automatico di notifiche agli utenti (es. aggiornamenti su progetti votati, nuove proposte, esiti votazioni).
- Implementazione di una sezione di discussione per ogni progetto, permettendo ai cittadini di lasciare opinioni e suggerimenti.
- Definizione di soglie di punti per il raggiungimento di diversi livelli di badge.
- Sviluppo di un sistema per l'assegnazione automatica di badge speciali ai Cittadini che superano le soglie predefinite.

&nbsp;**Licenza**

Questo progetto è stato sviluppato da Emanuele Musto a scopo didattico nell’ambito del corso di Basi di Dati presso l’Università degli Studi di Napoli Parthenope, A.A. 2024/2025. Non è destinato alla distribuzione commerciale.