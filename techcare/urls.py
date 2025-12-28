from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # <--- Ось це підключає всі наші сторінки
]

# Цей блок потрібен, щоб Django міг показувати завантажені фото (Активи)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)