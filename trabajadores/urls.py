from django.urls import path
from . import views

app_name = 'trabajadores'

urlpatterns = [
    # TRABAJADORES (ya existen)    
    path('listar/', views.listar_trabajadores, name='listar'),
    path('crear/', views.crear_trabajador, name='crear'),
    path('editar/<int:trabajador_id>/', views.editar_trabajador, name='editar'),
    path('eliminar/<int:trabajador_id>/', views.eliminar_trabajador, name='eliminar'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),

    # PROVINCIAS
    path("provincias/", views.listar_provincias, name="listar_provincias"),
    path("provincias/crear/", views.crear_provincia, name="crear_provincia"),
    path("provincias/editar/<int:id>/", views.editar_provincia, name="editar_provincia"),
    path("provincias/eliminar/<int:id>/", views.eliminar_provincia, name="eliminar_provincia"),

    # CIUDADES
    path("ciudades/", views.listar_ciudades, name="listar_ciudades"),
    path("ciudades/crear/", views.crear_ciudad, name="crear_ciudad"),
    path("ciudades/editar/<int:id>/", views.editar_ciudad, name="editar_ciudad"),
    path("ciudades/eliminar/<int:id>/", views.eliminar_ciudad, name="eliminar_ciudad"),

]
