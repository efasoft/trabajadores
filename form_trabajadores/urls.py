from django.contrib import admin
from django.urls import path, include
from trabajadores import views as t_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', t_views.home, name='home'),
    path('', include(('trabajadores.urls', 'trabajadores'))),
    path('usuarios/', include(('usuarios.urls', 'usuarios'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




