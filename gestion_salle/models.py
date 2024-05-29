from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django_celery_beat.models import PeriodicTask, ClockedSchedule
import json
# Create your models here.

class Salle(models.Model):
    numero = models.CharField(max_length=50)
    capacite = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)

class Reservation(models.Model):
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    professeur = models.CharField(max_length=100)
    matiere = models.CharField(max_length=100)
    terminee=models.BooleanField(default=False)

    def schedule_annulation(self):
        # Importation paresseuse
        from .tasks import annuler_reservation
        annulation_time = timezone.make_aware(
            datetime.datetime.combine(self.date, self.heure_fin),
            timezone.get_current_timezone()
        )

        clocked_schedule, created = ClockedSchedule.objects.get_or_create(clocked_time=annulation_time)

        PeriodicTask.objects.create(
            clocked=clocked_schedule,
            name=f"Annulation de la réservation {self.id} à {annulation_time}",
            task='gestion_salle.tasks.annuler_reservation',
            args=json.dumps([self.id]),
            one_off=True
        )