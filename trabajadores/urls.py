from django.urls import path
from . import views

app_name = 'trabajadores'

urlpatterns = [
    path('', views.TrabajadorListView.as_view(), name='listar'),
    path('crear/', views.TrabajadorCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', views.TrabajadorUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', views.TrabajadorDeleteView.as_view(), name='eliminar'),
]
