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

from SmartCity.views import *

urlpatterns = [
    path('registrazione', registrazione, name="registrazione"),

    path('admin/', admin.site.urls),
    path('login', login, name="login"),

    path('home_cittadino', home_cittadino, name="home_cittadino"),

    path('home_urbanista', home_urbanista, name="home_urbanista"),

    path('aggiungi_progetto', aggiungi_progetto, name="aggiungi_progetto"),
    path('logout/', logout_view, name='logout'),

    path('', homepage, name="homepage")
]
