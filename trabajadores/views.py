from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings  # <-- ESTA ES LA CLAVE
from django.contrib.auth.decorators import login_required
from .models import Trabajador
from .forms import TrabajadorForm
from .validators import TrabajadorModel
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

import csv

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
import os
import io
from django.http import FileResponse
from django.contrib.auth.decorators import login_required

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

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
    filtro = request.GET.get('q', '').lower()

    trabajadores = Trabajador.objects.all()
    if filtro:
        trabajadores = trabajadores.filter(
            nombres__icontains=filtro
        ) | trabajadores.filter(
            apellidos__icontains=filtro
        ) | trabajadores.filter(
            email__icontains=filtro
        )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Trabajadores"

    # Estilo encabezado
    encabezados = [
        "NOMBRES", "APELLIDOS", "EMAIL", "ACTIVO", "SUELDO BRUTO",
        "FECHA", "EDAD", "TEL. CASA", "TEL. MÓVIL"
    ]

    bold_font = Font(bold=True, color="FFFFFF")
    fill = PatternFill(start_color="003C3C", end_color="003C3C", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin'),
    )

    for col_num, header in enumerate(encabezados, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = bold_font
        cell.fill = fill
        cell.alignment = center_align
        cell.border = border

    # Datos
    for row_num, t in enumerate(trabajadores, 2):
        row = [
            t.nombres,
            t.apellidos,
            t.email,
            "Sí" if t.activo else "No",
            f"{t.sueldo_bruto:,.2f}",
            t.fecha.strftime("%d/%m/%Y") if t.fecha else "",
            t.edad,
            t.telefono_casa,
            t.telefono_movil
        ]
        for col_num, valor in enumerate(row, 1):
            cell = ws.cell(row=row_num, column=col_num, value=valor)
            if col_num in [1, 2, 3]:
                cell.alignment = left_align
            elif col_num in [4, 6, 7, 8, 9]:
                cell.alignment = center_align
            elif col_num == 5:
                cell.alignment = right_align
            cell.border = border

    # Total al final
    total_row = len(trabajadores) + 2
    ws.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=8)
    cell_total = ws.cell(row=total_row, column=1, value="TOTAL TRABAJADORES")
    cell_total.font = Font(bold=True)
    cell_total.alignment = right_align

    count_cell = ws.cell(row=total_row, column=9, value=trabajadores.count())
    count_cell.font = Font(bold=True)
    count_cell.alignment = center_align

    # Ajustar ancho de columnas
    for i, col in enumerate(encabezados, 1):
        ws.column_dimensions[get_column_letter(i)].width = 18

    # Respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    disposition = 'inline' if request.GET.get('descargar') == '0' else 'attachment'
    response['Content-Disposition'] = f'{disposition}; filename="reporte_trabajadores.xlsx"'
    wb.save(response)
    return response

@login_required
def exportar_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    elementos = []

    # Logo
    logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'efa_soft.jpg')
    try:
        img = Image(logo_path, width=3 * cm, height=3 * cm)
    except:
        img = Paragraph("", getSampleStyleSheet()['Normal'])

    # Título y fecha
    estilos = getSampleStyleSheet()
    titulo = Paragraph("<b style='font-size:18pt;color:#003c3c;'>REPORTE GENERAL DE TRABAJADORES</b>", estilos['Title'])
    fecha = Paragraph(f"<para align='right'>Emitido: {datetime.now().strftime('%d/%m/%Y')}</para>", estilos['Normal'])

    header = Table([[img, titulo, fecha]], colWidths=[4*cm, 16*cm, 8*cm])
    header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
    ]))
    elementos.append(header)
    elementos.append(Spacer(1, 12))

    # Encabezado
    encabezado = [
        "NOMBRES", "APELLIDOS", "EMAIL", "ACTIVO", "SUELDO BRUTO",
        "FECHA", "EDAD", "TEL. CASA", "TEL. MÓVIL"
    ]

    data = [encabezado]
    # Aplicar filtro si viene desde búsqueda
    filtro = request.GET.get('q', '').lower()
    trabajadores = Trabajador.objects.all()
    if filtro:
        trabajadores = trabajadores.filter(
            nombres__icontains=filtro
        ) | trabajadores.filter(
            apellidos__icontains=filtro
        ) | trabajadores.filter(
            email__icontains=filtro
        )

    for t in trabajadores:
        data.append([
            t.nombres,
            t.apellidos,
            t.email,
            "Sí" if t.activo else "No",
            f"€{t.sueldo_bruto:,.2f}",
            t.fecha.strftime("%d/%m/%Y") if t.fecha else "",
            str(t.edad),
            t.telefono_casa,
            t.telefono_movil,
        ])

    # Total trabajadores
    total_row = ["", "", "", "", "", "", "", "", f"Total: {trabajadores.count()}"]
    data.append(total_row)

    col_just = ['LEFT', 'LEFT', 'LEFT', 'CENTER', 'RIGHT', 'CENTER', 'CENTER', 'CENTER', 'CENTER']
    tabla = Table(data, repeatRows=1, colWidths=[4.5*cm, 4.5*cm, 6*cm, 2*cm, 3*cm, 2*cm, 1.3*cm, 2.2*cm, 2.2*cm])

    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003c3c")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ROWBACKGROUNDS', (1, 1), (-1, -2), [colors.whitesmoke, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    # Alineación individual por columna
    for idx, align in enumerate(col_just):
        estilo.add('ALIGN', (idx, 1), (idx, -2), align)

    # Totales en negrita y alineados a la derecha
    estilo.add('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold')
    estilo.add('ALIGN', (-1, -1), (-1, -1), 'RIGHT')

    tabla.setStyle(estilo)
    elementos.append(tabla)

    doc.build(elementos)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    if request.GET.get('descargar') == '1':
        response['Content-Disposition'] = 'attachment; filename="reporte_trabajadores.pdf"'
    else:
        response['Content-Disposition'] = 'inline; filename="reporte_trabajadores.pdf"'

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






