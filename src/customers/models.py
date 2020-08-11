import json

from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50, default="-1")

    def getCart(self):
        from cart.get import cartForUserWithID
        return cartForUserWithID(self.id)

    def getRepr(self):
        return {
            "name": self.name,
            "uid": self.id
        }
