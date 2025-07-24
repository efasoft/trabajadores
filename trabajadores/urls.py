from django.urls import path
from . import views

app_name = 'trabajadores'

urlpatterns = [
    path('listar/', views.listar_trabajadores, name='listar'),
    path('crear/', views.crear_trabajador, name='crear'),
    path('editar/<int:trabajador_id>/', views.editar_trabajador, name='editar'),
    path('eliminar/<int:trabajador_id>/', views.eliminar_trabajador, name='eliminar'),
]



