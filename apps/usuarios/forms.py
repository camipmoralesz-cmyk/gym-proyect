import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil


def normalizar_rut(valor):
    valor = valor.strip()
    if not re.fullmatch(r'\d{7,8}[0-9kK]', valor):
        return None
    cuerpo, dv = valor[:-1], valor[-1].upper()

    suma, mult = 0, 2
    for d in reversed(cuerpo):
        suma += int(d) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    esperado = 'K' if resto == 10 else '0' if resto == 11 else str(resto)
    if dv != esperado:
        return None

    return f"{int(cuerpo):,}".replace(',', '.') + f"-{dv}"


def normalizar_telefono(valor):
    digitos = re.sub(r'\D', '', valor)  # deja solo los números
    if len(digitos) != 9 or not digitos.startswith('9'):
        return None
    return f"{digitos[0]} {digitos[1:5]} {digitos[5:]}"
class PerfilCleanMixin:
    """Validaciones clean_() compartidas (RUT, teléfono, correo único)."""

def clean_rut(self):
    rut = normalizar_rut(self.cleaned_data.get('rut', ''))
    if rut is None:
        raise forms.ValidationError(
            'RUT inválido. Escríbelo solo con números, sin puntos ni guion. Ejemplo: 123456785'
        )
    # Único, ignorando al propio usuario cuando se edita
    if Perfil.objects.filter(rut=rut).exclude(user_id=self.instance.pk).exists():
        raise forms.ValidationError('Este RUT ya está registrado.')
    return rut

    def clean_telefono(self):
        tel = normalizar_telefono(self.cleaned_data.get('telefono', ''))
        if tel is None:
            raise forms.ValidationError('Celular inválido. Ejemplo: 9 8765 4321')
        return tel

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(username=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

def _campo_fecha():
    return forms.DateField(
        required=False, label='Vencimiento de membresía (solo clientes)',
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}))


def _ctl(placeholder=''):
    return forms.TextInput(attrs={'class': 'form-control', 'placeholder': placeholder})


# ============================================================
# Registro: usa UserCreationForm (valida y encripta la contraseña)
# El correo se usa también como username.
# ============================================================
class RegistroForm(PerfilCleanMixin, UserCreationForm):
    first_name = forms.CharField(label='Nombre', widget=_ctl('Nombre'))
    last_name = forms.CharField(label='Apellido', widget=_ctl('Apellido'))
    email = forms.EmailField(label='Correo', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.cl'}))
    rut = forms.CharField(label='RUT', widget=_ctl('123456785-9'))
    telefono = forms.CharField(label='Teléfono', widget=_ctl('9 8765 4321'))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre in ('password1', 'password2'):
            self.fields[nombre].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email          # el correo es el usuario
        user.save()
        Perfil.objects.create(user=user, rut=self.cleaned_data['rut'],
                              telefono=self.cleaned_data['telefono'])
        return user



# HITO 3: crear desde la gestión (agrega rol)

class UsuarioAdminForm(RegistroForm):
    ROLES = [('cliente', 'Cliente'), ('administrador', 'Administrador')]
    PERMISOS = [('', '---------'), ('Acceso Total', 'Acceso Total'),
                ('Acceso Recepción', 'Acceso Recepción')]

    rol = forms.ChoiceField(choices=ROLES, label='Rol',
                            widget=forms.Select(attrs={'class': 'form-select'}))
    nivelPermiso = forms.ChoiceField(choices=PERMISOS, required=False,
                                     label='Nivel de permiso (solo administradores)',
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    fechaVencimientoMembrecia = _campo_fecha()
    def clean(self):
        cleaned = super().clean()
        if cleaned.get('rol') == 'administrador' and not cleaned.get('nivelPermiso'):
            self.add_error('nivelPermiso', 'Indica el nivel de permiso del administrador.')
        return cleaned


# ============================================================
# HITO 4: editar (sin cambio de rol ni contraseña)
# ============================================================
class UsuarioEditarForm(PerfilCleanMixin, forms.ModelForm):
    rut = forms.CharField(label='RUT', widget=_ctl())
    telefono = forms.CharField(label='Teléfono', widget=_ctl())
    nivelPermiso = forms.ChoiceField(choices=UsuarioAdminForm.PERMISOS, label='Nivel de permiso',
                                     widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'first_name': 'Nombre', 'last_name': 'Apellido', 'email': 'Correo'}
        widgets = {'first_name': _ctl(), 'last_name': _ctl(),
                   'email': forms.EmailInput(attrs={'class': 'form-control'})}

    fechaVencimientoMembrecia = _campo_fecha()

    def __init__(self, *args, es_admin=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not es_admin:      # el permiso solo existe en administradores
            del self.fields['nivelPermiso']
        else:                 # la membresía solo existe en clientes
            del self.fields['fechaVencimientoMembrecia']