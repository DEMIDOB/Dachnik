from django.db import models

# Create your models here.
class Reservation(models.Model):
    article = models.CharField(max_length=25, default='0', primary_key=True)
    amount  = models.IntegerField(default=0)