from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Salle, Reservation
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from datetime import datetime

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Salle, Reservation

def reserver_salle(request):
    result = None
    if request.method == "POST":
        salle_id = request.POST.get("salle")
        date_reservation = request.POST.get("date")
        heure_debut = request.POST.get("heure_debut")
        heure_fin = request.POST.get("heure_fin")
        professeur = request.POST.get("professeur")
        matiere = request.POST.get("matiere")

        try:
            salle = Salle.objects.get(pk=salle_id)
            
            # Conversion des chaînes de caractères en objets datetime
            date_reservation = datetime.strptime(date_reservation, "%Y-%m-%d").date()
            heure_debut = datetime.strptime(heure_debut, "%H:%M").time()
            heure_fin = datetime.strptime(heure_fin, "%H:%M").time()

            reservation = Reservation.objects.create(
                salle=salle,
                date=date_reservation,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                professeur=professeur,
                matiere=matiere,
            )

            if reservation:
                salle.disponible = False
                salle.save()

                # Planifier l'annulation de la réservation
                reservation.schedule_annulation()

                result = f"Salle {salle.numero} réservée avec succès!"
            else:
                result = "Erreur: La réservation n'a pas pu être créée."
        except Salle.DoesNotExist:
            result = "Erreur: Salle non trouvée."
        except Exception as e:
            result = f"Erreur: {str(e)}"

        return HttpResponse(result)

    salles = Salle.objects.filter(disponible=True)
    return render(request, "reservation.html", {"salles": salles, "result": result})


def liberer_salle(request):
    result = None

    if request.method == "POST":
        salle_id = request.POST.get("salle")

        if salle_id:
            salle = get_object_or_404(Salle, id=salle_id)

            reservation_en_cours = Reservation.objects.filter(
                salle=salle, terminee=False
            ).first()

            if reservation_en_cours:

                reservation_en_cours.terminee = True
                reservation_en_cours.save()

                salle.disponible = True
                salle.save()

                result = f"Salle {salle.numero} libérée avec succès!"
            else:
                result = f"Aucune réservation en cours pour la salle {salle.numero} à cette heure."

        else:
            result = "Erreur: Tous les champs doivent être remplis."

    salles_non_disponibles = Salle.objects.filter(disponible=False)

    return render(
        request, "liberation.html", {"salles": salles_non_disponibles, "result": result}
    )


def liste_salles(request):
    salles_disponibles = Salle.objects.all()
    reservations = Reservation.objects.all()
    context = {
        "salles_disponibles": salles_disponibles,
        "reservations": reservations,
    }

    return render(request, "liste_salles.html", context)


def new_salles(request):
    return render(request, "ajouter_salles.html")


def acceuil(request):
    return render(request, "acceuil.html")


def ajouter_salle(request):
    if request.method == "POST":

        numero = request.POST.get("numero")
        capacite = request.POST.get("capaciter")
        if Salle.objects.filter(numero=numero).exists():
            messages.error(request, "Cette salle existe déja.")
            return redirect("new_salles")
        else:
            Salle.objects.create(numero=numero, capacite=capacite)
            messages.success(request, "salle creer avec succes.")

    return redirect("liste_salles")


def login1(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("liste_salles")
        else:
            messages.error(request, "username ou mot de passe incorrect.")
    return render(request, "connexion.html")


def logout1(request):
    logout(request)
    return redirect("login")


def tris(request):
    Salle.objects.filter(request)