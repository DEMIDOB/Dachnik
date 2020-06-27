import datetime

from django.db import models


# Create your models here.
class BlogPost(models.Model):
    title     = models.CharField(default="Заголовок", max_length=50)
    topic     = models.CharField(default="Тема", max_length=50)
    icon      = models.CharField(default="http://demidob.site/dch/imgs/none.jpg", max_length=150)
    date_time = models.DateTimeField(auto_now=True)
    body      = models.TextField(default="Текст блога")
