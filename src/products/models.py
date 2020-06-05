from django.db import models

# Create your models here.
class Product(models.Model):
    title       = models.CharField(max_length=150, default='Новый продукт')
    description = models.TextField(default='Описаниие продукта')
    category    = models.CharField(max_length=150, default='Фрукты')
    price       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    article     = models.CharField(max_length=25, default='0')
    amount      = models.IntegerField(default=0)
    isAvailable = models.BooleanField(default=False)