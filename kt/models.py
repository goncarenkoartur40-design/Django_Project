from django.db import models

# Create your models here.
class Kontakt(models.Model):
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=70)
    telefon = models.IntegerField()

