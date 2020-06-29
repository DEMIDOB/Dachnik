from django import forms
from phone_field import PhoneField

# My forms:
class OrderForm(forms.Form):
    name    = forms.CharField(label='Имя', max_length=50, required=True)
    phone   = forms.CharField(label='Телефон', max_length=12, required=True)
    email   = forms.EmailField(label='E-Mail', required=True)
    comment = forms.CharField(label='Комментарий к заказу', max_length=500, required=True, widget=forms.Textarea)