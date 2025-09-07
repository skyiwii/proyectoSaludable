"""
URL configuration for proyectoSaludable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from verdeLimonApp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('verdeLimonAPP.url')),
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path("", views.index, name="index"),
    path("productos/", views.productos, name="productos"),
    path("productos/<int:producto_id>/", views.detalle_producto, name="detalle_producto"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path("contacto/", views.contacto, name="contacto"),
    path("distribucion/", views.distribucion, name="distribucion"),

    path('favoritos/', views.favoritos, name='favoritos'),
    path('favoritos/agregar/<int:producto_id/', views.agregar_favoritos, name='agregar_favoritos'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

