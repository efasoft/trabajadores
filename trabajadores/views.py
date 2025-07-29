from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trabajador
from .forms import TrabajadorForm
from .validators import TrabajadorModel
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

@login_required
def home(request):
    trabajadores = Trabajador.objects.all()
    total = trabajadores.count()
    activos = trabajadores.filter(activo=True).count()
    inactivos = trabajadores.filter(activo=False).count()
    promedio = round(sum(t.sueldo_bruto for t in trabajadores) / total, 2) if total else 0

    context = {
        'total': total,
        'activos': activos,
        'inactivos': inactivos,
        'promedio': promedio
    }
    return render(request, 'trabajadores/home.html', context)


@login_required
def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            # Extraer y convertir fecha
            try:
                fecha_str = request.POST.get('fecha')
                data['fecha'] = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            except Exception:
                return JsonResponse({
                    'success': False,
                    'errors': ['Formato de fecha inválido. Use DD/MM/AAAA.']
                })

            data['foto'] = request.FILES.get('foto')

            try:
                validated_data = TrabajadorModel(**data)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'errors': [str(e).replace("Value error,", "").strip()]
                })

            Trabajador.objects.create(**validated_data.model_dump())
            return JsonResponse({
                'success': True,
                'message': 'Trabajador creado correctamente.'
            })

        return JsonResponse({
            'success': False,
            'errors': [error for field in form for error in field.errors]
        })

    form = TrabajadorForm()
    return render(request, 'trabajadores/form.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, pk=trabajador_id)

    if request.method == 'POST':
        form = TrabajadorForm(request.POST, request.FILES, instance=trabajador)
        if form.is_valid():
            data = form.cleaned_data

            try:
                fecha_str = request.POST.get('fecha')
                data['fecha'] = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            except Exception:
                return JsonResponse({
                    'success': False,
                    'errors': ['Formato de fecha inválido. Usa DD/MM/AAAA.']
                })

            data['foto'] = request.FILES.get('foto') or trabajador.foto

            try:
                validated_data = TrabajadorModel(**data)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'errors': [str(e).replace("Value error,", "").strip()]
                })

            for attr, value in validated_data.model_dump().items():
                setattr(trabajador, attr, value)
            trabajador.save()

            return JsonResponse({
                'success': True,
                'message': 'Trabajador actualizado correctamente.'
            })

        return JsonResponse({
            'success': False,
            'errors': [error for field in form for error in field.errors]
        })

    form = TrabajadorForm(instance=trabajador)
    return render(request, 'trabajadores/form.html', {
        'form': form,
        'accion': 'Editar',
        'trabajador': trabajador
    })


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

@login_required
def exportar_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="trabajadores.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Activo', 'Sueldo Bruto'])

    for t in Trabajador.objects.all():
        writer.writerow([f"{t.nombres} {t.apellidos}", t.email, t.activo, t.sueldo_bruto])

    return response

@login_required
def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trabajadores.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, y, "Lista de Trabajadores")
    y -= 30

    p.setFont("Helvetica", 11)
    for t in Trabajador.objects.all():
        p.drawString(30, y, f"{t.nombres} {t.apellidos} | {t.email} | Activo: {'Sí' if t.activo else 'No'} | €{t.sueldo_bruto}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 40

    p.showPage()
    p.save()
    return response



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






