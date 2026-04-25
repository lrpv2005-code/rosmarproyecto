from django import forms
from django.contrib.auth.models import User
from .models import Resena

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmacion = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('password')
        pwd2 = cleaned_data.get('password_confirmacion')

        if pwd1 != pwd2:
            self.add_error('password_confirmacion', "Las contraseñas no coinciden.")
        return cleaned_data

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
