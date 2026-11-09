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
#LOGIN
#-------------------------------
def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            # Validación: solo entra si es administrador o staff
            if user.is_staff or user.is_superuser:
                login(request, user)
                # Ojo aquí: asegúrate de que el nombre de la ruta sea el mismo que tienes en tus urls.py (ej. 'dashboard' o 'core:dashboard')
                return redirect('core:dashboard') 
            else:
                messages.error(request, 'Acceso denegado. No tienes permisos de administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            
    return render(request, 'core/login.html')

#-------------------------------
# PANTALLA PRINCIPAL
#-------------------------------
@login_required(login_url='login')
def dashboard_view(request):
    if not request.user.is_staff:
        logout(request)
        return redirect('login')
        
    # --- 1. Obtener estadísticas reales de la BD ---
    # Usuarios activos 
    total_usuarios_activos = User.objects.filter(is_active=True, is_staff=False).count()
    
    # Ejemplo para las demás tarjetas 
    membresias_por_vencer = 0  
    maquinas_operativas = "0/0"  

    # Contar el total de máquinas registradas
    total_maquinas = Maquina.objects.count()

    # Contar cuántas están operativas 
    operativas = Maquina.objects.filter(estadoDisponible=True).count()

    # Formatear para que muestre el formato operativas o no
    maquinas_operativas = f"{operativas}/{total_maquinas}"

    ofertas_activas = 0
    
    renovaciones_pendientes = 0
    reportes_maquinas = 0
    
    # Nuevos registros hoy 
    total_nuevos_hoy = User.objects.filter(date_joined__date=timezone.now().date()).count()
    # total_nuevos_hoy = 0 

    # --- 2. Obtener la lista de clientes registrados ---
    # Traemos a los usuarios que son clientes 
    clientes_registrados = User.objects.filter(is_staff=False).order_by('-date_joined')[:10] # Últimos 10

    context = {
        'titulo_seccion': 'Panel de Control e Información Institucional',
        'admin_name': request.user.username,
        # Estadísticas
        'total_usuarios_activos': total_usuarios_activos,
        'membresias_por_vencer': membresias_por_vencer,
        'maquinas_operativas': maquinas_operativas,
        'ofertas_activas': ofertas_activas,
        'renovaciones_pendientes': renovaciones_pendientes,
        'reportes_maquinas': reportes_maquinas,
        'total_nuevos_hoy': total_nuevos_hoy,
        # Lista de clientes para la tabla
        'clientes_registrados': clientes_registrados,
    }
    
    return render(request, 'core/dashboard.html', context)

#-------------------------------
# CERRAR SESION
#-------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')