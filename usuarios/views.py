from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            # En caso de error, renderizar login.html con bandera de error
            return render(request, 'usuarios/login.html', {
                'form': form,
                'login_error': True  # esta bandera activará SweetAlert2 en el template
            })

    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('usuarios:login')


def registro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/registro.html', {
                'usuario_existente': True
            })

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'usuarios/registro.html', {
                'registro_exitoso': True
            })
        else:
            return render(request, 'usuarios/registro.html', {
                'registro_error': True
            })

    return render(request, 'usuarios/registro.html')

