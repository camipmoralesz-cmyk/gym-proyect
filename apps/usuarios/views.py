from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import RegistroForm, LoginForm
from .models import Usuario, Cliente


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Se le crea automáticamente su ficha de cliente asociada
            Cliente.objects.create(idUsuario=usuario)
            messages.success(request, 'Usuario registrado con éxito. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['contrasena']

            try:
                usuario = Usuario.objects.get(correo=correo)
                if check_password(password, usuario.contrasena):
                    # Guardamos los datos de la sesión del usuario
                    request.session['usuario_id'] = usuario.idUsuario
                    request.session['usuario_nombre'] = usuario.nombre
                    messages.success(request, f'Bienvenido, {usuario.nombre}!')
                    return redirect('perfil')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'El correo no se encuentra registrado.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login')


def perfil_view(request):
    # Verificamos si hay sesión activa
    if 'usuario_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para acceder.')
        return redirect('login')

    usuario = Usuario.objects.get(idUsuario=request.session['usuario_id'])
    return render(request, 'usuarios/perfil.html', {'usuario': usuario})