from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50, required=True)
    topic = forms.CharField(label='Тема обращения', max_length=100, required=True)
    body = forms.CharField(label='Тело', max_length=500, required=True, widget=forms.Textarea)
    email = forms.EmailField(label='E-Mail', required=True)