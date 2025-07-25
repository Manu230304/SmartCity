"""
URL configuration for ProgettoBasi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from SmartCity.views import *

urlpatterns = [
    path('registrazione', registrazione, name="registrazione"),

    path('admin/', admin.site.urls),
    path('login', login, name="login"),

    path('homepage_cittadino', homepage_cittadino, name="homepage_cittadino"),

    path('home_urbanista', home_urbanista, name="home_urbanista"),

    path('aggiungi_progetto', aggiungi_progetto, name="aggiungi_progetto"),
    path('profilo_urbanista', profilo_urbanista, name="profilo_urbanista"),
    path('logout/', logout_view, name='logout'),
    path('salva_bio', salva_bio, name="salva_bio"),

    path('progetti_votabili', progetti_votabili, name="progetti_votabili"),

    path('home_tecnico', home_tecnico, name="home_tecnico"),

    path('profilo_tecnico', profilo_tecnico, name="profilo_tecnico"),
    path('valuta_progetto', valuta_progetto, name="valuta_progetto"),

    path('vota_progetto', vota_progetto, name="vota_progetto"),
    path('gestione_progetti', gestione_progetti, name='gestione_progetti'),

    # URL per vedere il profilo pubblico di un urbanista usando la sua email
    path('profilo_urbanista_pubblico/<str:email>', profilo_urbanista_pubblico, name="profilo_urbanista_pubblico"),
    path('gestione_fasi/<int:progetto_id>', gestione_fasi, name="gestione_fasi"),
    path('gestione_fasi', gestione_fasi, name="gestione_fasi"),

    path('segna_progetto_completato/<int:progetto_id>', segna_progetto_completato, name="segna_progetto_completato"),

    path('progetti_completati', progetti_completati, name='progetti_completati'),

    path('progetti_votabili_tecnico', progetti_votabili_tecnico, name='progetti_votabili_tecnico'),

    path('toggle_votazione/<int:progetto_id>', toggle_votazione, name="toggle_votazione"),

    path('prendi_piu_votato', prendi_piu_votato, name="prendi_piu_votato"),
    path('recensioni', recensioni, name="recensioni"),

    path('recensisci_progetto', recensisci_progetto, name="recensisci_progetto"),
path('recensioni_pagina_urbanista', recensioni_pagina_urbanista, name="recensioni_pagina_urbanista"),

    # path('login_vulnerabile', login_vulnerabile, name="login_vulnerabile"),

    path('recensioni_pagina_tecnico', recensioni_pagina_tecnico, name="recensioni_pagina_tecnico"),

    path('segna_fase_completata/<int:fase_id>' , segna_fase_completata, name="segna_fase_completata"),



    path('', homepage, name="homepage")


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
