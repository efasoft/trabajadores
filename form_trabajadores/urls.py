from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('trabajadores.urls', 'trabajadores'), namespace='trabajadores')),
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

