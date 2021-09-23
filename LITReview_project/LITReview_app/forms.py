from django import forms

from .models import UserFollows


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)



class LoginForm(forms.ModelForm):
    pass
