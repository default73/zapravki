from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BankCard


class ExpirationDateWidget(forms.DateInput):
    input_type = 'text'
    format="%m/%y"


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Обязательное поле. Введите действующий email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BankCardForm(forms.ModelForm):
    expiration_date = forms.DateField(
        widget=ExpirationDateWidget(),
        input_formats=['%m/%y']
    )
    class Meta:
        model = BankCard
        fields = ['card_number', 'expiration_date', 'cvv_code']