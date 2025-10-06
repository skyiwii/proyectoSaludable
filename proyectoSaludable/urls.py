"""
URL configuration for proyectoSaludable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(\'\', views.home, name=\'home\')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(\'\', Home.as_view(), name=\'home\')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path(\'blog/\', include(\'blog.urls\'))
"""
from django.contrib import admin
from django.urls import path
from verdeLimonApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('productos/', views.productos, name="productos"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('contacto/', views.contacto, name="contacto"),
    path("distribucion/", views.distribucion, name="distribucion"),
<<<<<<< Updated upstream
    path('dashboard/', views.dashboard_view, name='dashboard'),
]

=======
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    path("add-to-favorites/", views.add_to_favorites, name="add_to_favorites"),
    path("remove-from-favorites/", views.remove_from_favorites, name="remove_from_favorites"),
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # URLs para CategoriaProducto
    path("categorias/", views.CategoriaProductoListView.as_view(), name="categoria_list"),
    path("categorias/add/", views.CategoriaProductoCreateView.as_view(), name="categoria_add"),
    path("categorias/<int:pk>/edit/", views.CategoriaProductoUpdateView.as_view(), name="categoria_edit"),
    path("categorias/<int:pk>/delete/", views.CategoriaProductoDeleteView.as_view(), name="categoria_delete"),

    # URLs para Direccion
    path("direcciones/", views.DireccionListView.as_view(), name="direccion_list"),
    path("direcciones/add/", views.DireccionCreateView.as_view(), name="direccion_add"),
    path("direcciones/<int:pk>/edit/", views.DireccionUpdateView.as_view(), name="direccion_edit"),
    path("direcciones/<int:pk>/delete/", views.DireccionDeleteView.as_view(), name="direccion_delete"),

    # URLs para CentroDistribucion
    path("centros-distribucion/", views.CentroDistribucionListView.as_view(), name="centro_distribucion_list"),
    path("centros-distribucion/add/", views.CentroDistribucionCreateView.as_view(), name="centro_distribucion_add"),
    path("centros-distribucion/<int:pk>/edit/", views.CentroDistribucionUpdateView.as_view(), name="centro_distribucion_edit"),
    path("centros-distribucion/<int:pk>/delete/", views.CentroDistribucionDeleteView.as_view(), name="centro_distribucion_delete"),

    # URLs para Producto
    path("productos-crud/", views.ProductoListView.as_view(), name="producto_list"),
    path("productos-crud/add/", views.ProductoCreateView.as_view(), name="producto_add"),
    path("productos-crud/<int:pk>/edit/", views.ProductoUpdateView.as_view(), name="producto_edit"),
    path("productos-crud/<int:pk>/delete/", views.ProductoDeleteView.as_view(), name="producto_delete"),

    # URLs para ProductoValorNutricional
    path("valores-nutricionales/", views.ProductoValorNutricionalListView.as_view(), name="producto_valor_nutricional_list"),
    path("valores-nutricionales/add/", views.ProductoValorNutricionalCreateView.as_view(), name="producto_valor_nutricional_add"),
    path("valores-nutricionales/<int:pk>/edit/", views.ProductoValorNutricionalUpdateView.as_view(), name="producto_valor_nutricional_edit"),
    path("valores-nutricionales/<int:pk>/delete/", views.ProductoValorNutricionalDeleteView.as_view(), name="producto_valor_nutricional_delete"),

    # URLs para Inventario
    path("inventario/", views.InventarioListView.as_view(), name="inventario_list"),
    path("inventario/add/", views.InventarioCreateView.as_view(), name="inventario_add"),
    path("inventario/<int:pk>/edit/", views.InventarioUpdateView.as_view(), name="inventario_edit"),
    path("inventario/<int:pk>/delete/", views.InventarioDeleteView.as_view(), name="inventario_delete"),

    # URLs para HistorialInventario
    path("historial-inventario/", views.HistorialInventarioListView.as_view(), name="historial_inventario_list"),
    path("historial-inventario/add/", views.HistorialInventarioCreateView.as_view(), name="historial_inventario_add"),
    path("historial-inventario/<int:pk>/edit/", views.HistorialInventarioUpdateView.as_view(), name="historial_inventario_edit"),
    path("historial-inventario/<int:pk>/delete/", views.HistorialInventarioDeleteView.as_view(), name="historial_inventario_delete"),



    # URLs para ContactoCentro
    path("contactos-centros/", views.ContactoCentroListView.as_view(), name="contacto_centro_list"),
    path("contactos-centros/add/", views.ContactoCentroCreateView.as_view(), name="contacto_centro_add"),
    path("contactos-centros/<int:pk>/edit/", views.ContactoCentroUpdateView.as_view(), name="contacto_centro_edit"),
    path("contactos-centros/<int:pk>/delete/", views.ContactoCentroDeleteView.as_view(), name="contacto_centro_delete"),

    # URLs para Proveedor
    path("proveedores/", views.ProveedorListView.as_view(), name="proveedor_list"),
    path("proveedores/add/", views.ProveedorCreateView.as_view(), name="proveedor_add"),
    path("proveedores/<int:pk>/edit/", views.ProveedorUpdateView.as_view(), name="proveedor_edit"),
    path("proveedores/<int:pk>/delete/", views.ProveedorDeleteView.as_view(), name="proveedor_delete"),

    # URLs para FavoritoCliente
    path("favoritos-clientes/", views.FavoritoClienteListView.as_view(), name="favorito_cliente_list"),
    path("favoritos-clientes/add/", views.FavoritoClienteCreateView.as_view(), name="favorito_cliente_add"),
    path("favoritos-clientes/<int:pk>/edit/", views.FavoritoClienteUpdateView.as_view(), name="favorito_cliente_edit"),
    path("favoritos-clientes/<int:pk>/delete/", views.FavoritoClienteDeleteView.as_view(), name="favorito_cliente_delete"),
]



from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

>>>>>>> Stashed changes
