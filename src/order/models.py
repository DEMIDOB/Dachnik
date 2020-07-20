import json

from django.db import models

# Create your models here.
class Order(models.Model):
    json  = models.TextField(default=json.dumps({}))
    name  = models.CharField(default="", max_length=50)
    email = models.CharField(default="", max_length=150)