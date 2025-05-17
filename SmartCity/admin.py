from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Utente, Municipalita

class UtenteAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.save()

admin.site.register(Utente, UtenteAdmin)
# Voglio che il modello Utente compaia nel pannello di amministrazione, e voglio gestirlo usando la configurazione definita nella classe UtenteAdmin

admin.site.register(Municipalita)