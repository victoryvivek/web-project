from django import forms
from .models import UserInfo,User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput())
    
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username', 'password', 'first_name','last_name', 'email',]
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput()
        }

class AnswerForm(forms.Form):
    answer=forms.CharField(max_length=100, required=True)
