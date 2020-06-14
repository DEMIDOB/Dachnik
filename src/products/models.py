from django.db import models

# Create your models here.
class Product(models.Model):
    title       = models.CharField(max_length=150, default='Новый продукт')
    description = models.TextField(default='Описаниие продукта')
    category    = models.CharField(max_length=150, default='Фрукты')
    price       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount    = models.IntegerField(default=0)
    producer    = models.CharField(default="Неизвестный", max_length=50)
    icon        = models.CharField(default="http://demidob.site/dch/imgs/none.jpg", max_length=150)
    article     = models.CharField(max_length=25, default='0', primary_key=True)
    amount      = models.IntegerField(default=0)
    isAvailable = models.BooleanField(default=False)