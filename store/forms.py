
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Product


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico"
        })
    )

    is_seller = forms.BooleanField(
        label="Quiero registrarme como vendedor",
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "is_seller",
            "password1",
            "password2"
        ]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre de usuario"
            })
        }


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Contraseña"
        })
    )


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "name",
            "image",
            "description",
            "price",
            "condition",
            "stock",
            "categories"
        ]

        labels = {
            "name": "Nombre del producto",
            "image": "Fotografía",
            "description": "Descripción",
            "price": "Precio",
            "condition": "Estado",
            "stock": "Existencias",
            "categories": "Categorías"
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),
            "condition": forms.Select(attrs={
                "class": "form-select"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),
            "categories": forms.CheckboxSelectMultiple()
        }
