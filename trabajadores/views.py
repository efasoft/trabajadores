from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TrabajadorForm
from .models import Trabajador
from .validators import TrabajadorModel  # ✅ Añadir esta línea
from django.contrib import messages

from django.core.exceptions import ValidationError



@login_required
def home(request):
    trabajadores = Trabajador.objects.all()
    total = trabajadores.count()
    activos = trabajadores.filter(activo=True).count()
    inactivos = trabajadores.filter(activo=False).count()

    if trabajadores:
        promedio = sum(t.sueldo_bruto for t in trabajadores) / len(trabajadores)
    else:
        promedio = 0

    context = {
        'total': total,
        'activos': activos,
        'inactivos': inactivos,
        'promedio': round(promedio, 2)
    }
    return render(request, 'trabajadores/home.html', context)

@login_required
def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trabajadores:listar')
        # Si hay errores de validación, se renderiza con errores
        return render(request, 'trabajadores/form.html', {'form': form, 'accion': 'Crear'})
    else:
        form = TrabajadorForm()
        return render(request, 'trabajadores/form.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, request.FILES, instance=trabajador)

        if form.is_valid():
            try:
                data = form.cleaned_data.copy()

                # ⚠️ Mantener imagen actual si no se sube nueva
                if not request.FILES.get('foto'):
                    data['foto'] = trabajador.foto

                # Validación con Pydantic
                validated_data = TrabajadorModel(**data)

                # No asignar sueldo_bruto (ya es una property calculada)
                form.save()
                messages.success(request, 'Trabajador actualizado correctamente.')
                return redirect('trabajadores:listar')

            except ValidationError as e:
                errores = [error['msg'] for error in e.errors()]
                return render(request, 'trabajadores/form.html', {
                    'form': form,
                    'accion': 'Editar',
                    'errores': errores
                })
    else:
        form = TrabajadorForm(instance=trabajador)

    return render(request, 'trabajadores/form.html', {'form': form, 'accion': 'Editar'})





@login_required
def listar_trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'trabajadores/lista.html', {'trabajadores': trabajadores})

@login_required
def eliminar_trabajador(request, trabajador_id):
    try:
        trabajador = Trabajador.objects.get(pk=trabajador_id)
        trabajador.delete()
        messages.success(request, "Trabajador eliminado correctamente.")
    except Trabajador.DoesNotExist:
        messages.error(request, "El trabajador no existe.")
    return HttpResponseRedirect(reverse('trabajadores:listar'))    

"""
@login_required
def editar_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, pk=trabajador_id)
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, request.FILES, instance=trabajador)
        if form.is_valid():
            data = form.cleaned_data.copy()

            # Formatear fecha si es string
            if isinstance(data['fecha'], str):
                try:
                    data['fecha'] = datetime.strptime(data['fecha'], "%d-%m-%Y").date()
                except ValueError:
                    messages.error(request, "Formato de fecha inválido. Use DD-MM-AAAA.")
                    return render(request, 'trabajadores/form.html', {'form': form, 'accion': 'Editar'})

            # Foto nueva o mantener actual
            foto = request.FILES.get('foto')
            data['foto'] = foto.name if foto else trabajador.foto.name

            try:
                TrabajadorModel(**data)
                trabajador = form.save(commit=False)
                trabajador.sueldo_bruto = trabajador.sueldo_base + trabajador.comision
                trabajador.save()
                messages.success(request, 'Trabajador actualizado correctamente.')                
                return redirect('listar_trabajadores')
            except Exception as e:
                sweet_error(request, str(e).replace("Value error,", ""))
    else:
        form = TrabajadorForm(instance=trabajador)
    return render(request, 'trabajadores/form.html', {'form': form, 'accion': 'Editar'})


@login_required
def eliminar_trabajador(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    trabajador.delete()
    return redirect('listar_trabajadores')
  
"""






