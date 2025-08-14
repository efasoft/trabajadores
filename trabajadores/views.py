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
@login_required
def exportar_pdf(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=1 * cm,
        rightMargin=1 * cm,
        topMargin=3.5 * cm,  # espacio para encabezado repetido
        bottomMargin=1.5 * cm,
    )

    estilos = getSampleStyleSheet()
    elementos = []

    # Filtro de búsqueda
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

    # Datos de tabla
    encabezado = [
        "NOMBRES", "APELLIDOS", "EMAIL", "EDAD", "FECHA",
        "TEL. CASA", "TEL. MOVIL", "SUELDO BRUTO €", "ACTIVO"
    ]
    data = [encabezado]
    for t in trabajadores:
        data.append([
            Paragraph(f"<u>{t.nombres}</u>", estilos['Normal']),
            Paragraph(f"<u>{t.apellidos}</u>", estilos['Normal']),
            t.email,
            t.edad,
            t.fecha.strftime("%d/%m/%Y") if t.fecha else "",
            t.telefono_casa,
            t.telefono_movil,
            f"{t.sueldo_bruto:,.2f}",
            "SI" if t.activo else "NO"
        ])
    # Total
    data.append(["", "", "", "", "", "", "", "", f"{trabajadores.count()}"])

    col_widths = [4*cm, 4*cm, 6*cm, 2*cm, 3*cm, 3*cm, 3*cm, 3*cm, 2*cm]
    tabla = Table(data, repeatRows=1, colWidths=col_widths)

    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2F4F2F")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.whitesmoke, colors.HexColor("#EDEDED")]),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.green),
        ('ALIGN', (3, 1), (3, -2), 'CENTER'),  # edad
        ('ALIGN', (4, 1), (4, -2), 'CENTER'),  # fecha
        ('ALIGN', (7, 1), (7, -2), 'RIGHT'),   # sueldo
        ('ALIGN', (8, 1), (8, -2), 'CENTER'),  # activo
        ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (-1, -1), (-1, -1), 'CENTER'),
    ])
    tabla.setStyle(estilo)

    elementos.append(tabla)

    # Encabezado repetido en cada página
    def encabezado_pdf(canvas, doc):
        canvas.saveState()
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'efa_soft.jpg')
        if os.path.exists(logo_path):
            canvas.drawImage(logo_path, 1 * cm, A4[0] - 2.5 * cm, width=4 * cm, height=2 * cm, preserveAspectRatio=True)
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(10 * cm, A4[0] - 1.2 * cm, "RELACIÓN DE TRABAJADORES")
        canvas.setFont("Helvetica", 10)
        canvas.drawString(10 * cm, A4[0] - 2.0 * cm, "Datos por Ubicación")
        canvas.setFont("Helvetica", 8)
        fecha_str = datetime.now().strftime('%d/%m/%Y')
        canvas.drawRightString(A4[1] - 2 * cm, A4[0] - 1.2 * cm, f"Emitido : {fecha_str}")
        canvas.drawRightString(A4[1] - 2 * cm, A4[0] - 2.0 * cm, f"Página : {doc.page} de ")

        canvas.restoreState()

    doc.build(elementos, onFirstPage=encabezado_pdf, onLaterPages=encabezado_pdf)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = "reporte_trabajadores.pdf"
    if request.GET.get('descargar') == '1':
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
    else:
        response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response
