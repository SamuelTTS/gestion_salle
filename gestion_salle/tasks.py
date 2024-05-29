from celery import shared_task

@shared_task
def annuler_reservation(reservation_id):
    from .models import Reservation  # Importation paresseuse pour éviter la boucle
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.terminee = True
        reservation.save()
    except Reservation.DoesNotExist:
        pass
