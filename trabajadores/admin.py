from django.contrib import admin
from .models import Trabajador

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'email', 'telefono_movil', 'sueldo_bruto', 'eliminado')
    list_filter = ('eliminado',)
    search_fields = ('nombres', 'apellidos', 'email')

