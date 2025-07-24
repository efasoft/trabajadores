from django.contrib import admin
from django.urls import path, include
from trabajadores import views as t_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', t_views.home, name='home'),
    path('', include(('trabajadores.urls', 'trabajadores'))),
    path('usuarios/', include(('usuarios.urls', 'usuarios'))),
]





