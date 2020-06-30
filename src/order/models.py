import json

from django.db import models

# Create your models here.
class Order(models.Model):
    json = models.TextField(default=json.dumps({}))