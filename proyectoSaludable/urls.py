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
from django.urls import path

from django.contrib import admin
from django.urls import path
from verdeLimonApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("productos/", views.productos, name="productos"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path("contacto/", views.contacto, name="contacto"),
    path("distribucion/", views.distribucion, name="distribucion"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path("add-to-favorites/", views.add_to_favorites, name="add_to_favorites"),
    path("remove-from-favorites/", views.remove_from_favorites, name="remove_from_favorites"),
]
