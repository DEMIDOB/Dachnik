import json

from django.db import models

# Create your models here.
class Cart(models.Model):
    id = models.TextField(default="", primary_key=True)
    json = models.TextField(default=json.dumps({}))
