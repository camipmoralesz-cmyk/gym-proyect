from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario


class RegistroForm(forms.ModelForm):
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita la contraseña'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'contrasena']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.cl'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('contrasena')
        confirm_password = cleaned_data.get('confirmar_contrasena')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirmar_contrasena', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            usuario.save()
        return usuario


class LoginForm(forms.Form):
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        label="Correo"
    )
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label="Contraseña"
    )