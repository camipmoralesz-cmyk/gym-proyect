from django.shortcuts import render, redirect

def admin_login_view(request):
    """
    Vista para el login unificado.
    """
    if request.method == 'POST':
        return redirect('core:dashboard')
    return render(request, 'core/login.html')

def dashboard_core_view(request):
    """
    Vista para el Dashboard del Core administrativo.
    """
    context = {
        'titulo_seccion': 'Panel de Control e Información Institucional'
    }
    return render(request, 'core/dashboard.html', context)
def registro_view(request):
    """
    Vista para el formulario de registro de nuevos clientes.
    """
    if request.method == 'POST':
        # Aquí procesarás los datos del registro más adelante
        return redirect('core:login') # Redirige al login tras enviar
    return render(request, 'core/registro.html')