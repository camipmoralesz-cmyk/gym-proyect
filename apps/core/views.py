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