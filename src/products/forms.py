from django import forms

class OrderProductForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50, required=True)
    article = forms.CharField(label='article', max_length=, required=True)
    amount = forms.IntegerField(label='Количество', required=True)
    text
    phone = forms.forms.CharField(label='Телефон (не обязательно)', max_length=25, required=False)