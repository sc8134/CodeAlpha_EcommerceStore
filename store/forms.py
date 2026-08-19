from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal code'}))

    # Payment (demo — no real processing)
    card_number = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456', 'autocomplete': 'off'}))
    card_expiry = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))
    card_cvv = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'CVV', 'autocomplete': 'off'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
