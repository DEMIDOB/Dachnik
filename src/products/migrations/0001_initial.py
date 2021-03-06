# Generated by Django 3.0.7 on 2020-06-06 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Новый продукт', max_length=150)),
                ('description', models.TextField(default='Описаниие продукта')),
                ('category', models.CharField(default='Фрукты', max_length=150)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.IntegerField(default=0)),
                ('article', models.CharField(default='0', max_length=25)),
                ('amount', models.IntegerField(default=0)),
                ('isAvailable', models.BooleanField(default=False)),
            ],
        ),
    ]
