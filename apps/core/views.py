# Utilidades de Django para renderizar páginas HTML y redirigir al usuario
from django.shortcuts import render, redirect

# Herramientas de autenticación y seguridad (necesarias para el login de clientes)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
#from apps.catalogo.models import Maquina


def login_view(request):
    """
    Vista unificada: sirve tanto para clientes como para administradores.
    """
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            login(request, user)
            
            # Si es Administrador o Staff, va al Dashboard
            if user.is_staff or user.is_superuser:
                return redirect('core:dashboard')
            else:
                # Si es un cliente normal, va al portal de horarios
                return redirect('registro_horas:horarios')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            
    return render(request, 'core/login.html')
#-------------------------------
# LOGIN DE ADMINISTRADORES
#-------------------------------
#-------------------------------
# LOGIN DE ADMINISTRADORES
#-------------------------------
#def admin_login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('core:dashboard')
            else:
                messages.error(request, 'No tienes permisos de administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.') # <--- Esto es vital
            
    return render(request, 'core/login.html')
    """
    Vista para el login unificado del admin.
    """
    if request.method == 'POST':
        # Aquí puedes dejar la lógica del admin o ajustarla si procesa POST real
        return redirect('core:dashboard')
    return render(request, 'core/login.html')

#-------------------------------
# LOGIN DE CLIENTES (Separado del admin)
#-------------------------------
#def login_cliente_view(request):
    """
    Vista exclusiva para que los clientes inicien sesión y entren a su portal.
    """
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            # Validamos que NO sea staff (es un cliente)
            if not user.is_staff and not user.is_superuser:
                login(request, user)
                return redirect('registro_horas:horarios') # Lo mandamos a su portal de cliente
            else:
                messages.error(request, 'Esta sección es exclusiva para clientes.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            
    return render(request, 'core/login.html')

#-------------------------------
# DASHBOARD ADMINISTRATIVO
#-------------------------------
def dashboard_core_view(request):
    """
    Vista para el Dashboard del Core administrativo.
    """
    context = {
        'titulo_seccion': 'Panel de Control e Información Institucional'
    }
    return render(request, 'core/dashboard.html', context)

#-------------------------------
# REGISTRO DE NUEVOS CLIENTES
#-------------------------------
def registro_view(request):
    """
    Vista para el formulario de registro de nuevos clientes.
    """
    if request.method == 'POST':
        # Aquí procesarás los datos del registro más adelante
        return redirect('core:login') # Redirige al login tras enviar
    return render(request, 'core/registro.html')

#-------------------------------
# VISTA CLIENTE
#-------------------------------
def test_cliente_view(request):
    """
    Vista temporal para revisar la base y el diseño del cliente.
    """
    return render(request, 'registro_horas/horarios.html')
