# gestion_salles/urls.py
from django.urls import path
from .views import (
    reserver_salle,
    liberer_salle,
    liste_salles,
    ajouter_salle,
    new_salles,acceuil,
    login1,logout1
)

urlpatterns = [
    path("reserver/", reserver_salle, name="reserver_salle"),
    path("liberer/", liberer_salle, name="liberer_salle"),
    path("liste_salles/", liste_salles, name="liste_salles"),
    path("ajouter_salles/", ajouter_salle, name="ajouter_salles"),
    path("new_salles/", new_salles, name="new_salles"),
    path('login/', login1, name='login1'),
    path('logout/',logout1, name='logout1'),
    path("", acceuil, name="acceuil"),
]
