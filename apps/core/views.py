# Utilidades de Django para renderizar páginas HTML y redirigir al usuario
from django.shortcuts import render, redirect

# Herramientas de autenticación y seguridad (control de acceso y verificación de identidad)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from apps.catalogo.models import Maquina

#-------------------------------
# LOGIN UNIFICADO
#-------------------------------
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
# DASHBOARD ADMINISTRATIVO (Con estadísticas reales)
#-------------------------------
@login_required(login_url='login')
def dashboard_core_view(request):
    """
    Vista para el Dashboard del Core administrativo.
    """
    if not request.user.is_staff and not request.user.is_superuser:
        logout(request)
        return redirect('core:login')
        
    # --- 1. Obtener estadísticas reales de la BD ---
    total_usuarios_activos = User.objects.filter(is_active=True, is_staff=False).count()
    
    membresias_por_vencer = 0  
    maquinas_operativas = "0/0"  

    # Contar el total de máquinas registradas y operativas
    total_maquinas = Maquina.objects.count()
    operativas = Maquina.objects.filter(estadoDisponible=True).count()
    maquinas_operativas = f"{operativas}/{total_maquinas}"

    ofertas_activas = 0
    renovaciones_pendientes = 0
    reportes_maquinas = 0
    
    # Nuevos registros hoy 
    total_nuevos_hoy = User.objects.filter(date_joined__date=timezone.now().date()).count()

    # --- 2. Obtener la lista de clientes registrados ---
    clientes_registrados = User.objects.filter(is_staff=False).order_by('-date_joined')[:10] # Últimos 10

    context = {
        'titulo_seccion': 'Panel de Control e Información Institucional',
        'admin_name': request.user.username,
        'total_usuarios_activos': total_usuarios_activos,
        'membresias_por_vencer': membresias_por_vencer,
        'maquinas_operativas': maquinas_operativas,
        'ofertas_activas': ofertas_activas,
        'renovaciones_pendientes': renovaciones_pendientes,
        'reportes_maquinas': reportes_maquinas,
        'total_nuevos_hoy': total_nuevos_hoy,
        'clientes_registrados': clientes_registrados,
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
        return redirect('core:login')
    return render(request, 'core/registro.html')

#-------------------------------
# VISTA CLIENTE
#-------------------------------
def test_cliente_view(request):
    """
    Vista temporal para revisar la base y el diseño del cliente.
    """
    return render(request, 'registro_horas/horarios.html')

#-------------------------------
# CERRAR SESION
#-------------------------------
def logout_view(request):
    logout(request)
    return redirect('core:login')