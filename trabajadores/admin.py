from django.contrib import admin
from .models import Trabajador

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'apellidos', 'email', 'sueldo_bruto', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombres', 'apellidos', 'email')


