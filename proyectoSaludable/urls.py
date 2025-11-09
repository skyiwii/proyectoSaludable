from django.contrib import admin
from django.urls import path
from verdeLimonApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas principales
    path('', views.index, name="index"),
    path('productos/', views.productos, name="productos"),
    path('nosotros/', views.nosotros, name="nosotros"),
    path('contacto/', views.contacto, name="contacto"),
    path("distribucion/", views.distribucion, name="distribucion"),

    # Dashboards
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),

    # Favoritos AJAX
    path("add-to-favorites/", views.add_to_favorites, name="add_to_favorites"),
    path("remove-from-favorites/", views.remove_from_favorites, name="remove_from_favorites"),

    # Autenticación
    path("registro/", views.registro_view, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Categoría producto
    path("categorias/", views.CategoriaProductoListView.as_view(), name="categoria_list"),
    path("categorias/add/", views.CategoriaProductoCreateView.as_view(), name="categoria_add"),
    path("categorias/<int:pk>/edit/", views.CategoriaProductoUpdateView.as_view(), name="categoria_edit"),
    path("categorias/<int:pk>/delete/", views.CategoriaProductoDeleteView.as_view(), name="categoria_delete"),

    # Dirección
    path("direcciones/", views.DireccionListView.as_view(), name="direccion_list"),
    path("direcciones/add/", views.DireccionCreateView.as_view(), name="direccion_add"),
    path("direcciones/<int:pk>/edit/", views.DireccionUpdateView.as_view(), name="direccion_edit"),
    path("direcciones/<int:pk>/delete/", views.DireccionDeleteView.as_view(), name="direccion_delete"),

    # Centro de Distribución
    path("centros-distribucion/", views.CentroDistribucionListView.as_view(), name="centro_distribucion_list"),
    path("centros-distribucion/add/", views.CentroDistribucionCreateView.as_view(), name="centro_distribucion_add"),
    path("centros-distribucion/<int:pk>/edit/", views.CentroDistribucionUpdateView.as_view(), name="centro_distribucion_edit"),
    path("centros-distribucion/<int:pk>/delete/", views.CentroDistribucionDeleteView.as_view(), name="centro_distribucion_delete"),

    # Producto
    path("productos-crud/", views.ProductoListView.as_view(), name="producto_list"),
    path("productos-crud/add/", views.ProductoCreateView.as_view(), name="producto_add"),
    path("productos-crud/<int:pk>/edit/", views.ProductoUpdateView.as_view(), name="producto_edit"),
    path("productos-crud/<int:pk>/delete/", views.ProductoDeleteView.as_view(), name="producto_delete"),

    # Valor Nutricional
    path("valores-nutricionales/", views.ProductoValorNutricionalListView.as_view(), name="producto_valor_nutricional_list"),
    path("valores-nutricionales/add/", views.ProductoValorNutricionalCreateView.as_view(), name="producto_valor_nutricional_add"),
    path("valores-nutricionales/<int:pk>/edit/", views.ProductoValorNutricionalUpdateView.as_view(), name="producto_valor_nutricional_edit"),
    path("valores-nutricionales/<int:pk>/delete/", views.ProductoValorNutricionalDeleteView.as_view(), name="producto_valor_nutricional_delete"),

    # Inventario
    path("inventario/", views.InventarioListView.as_view(), name="inventario_list"),
    path("inventario/add/", views.InventarioCreateView.as_view(), name="inventario_add"),
    path("inventario/<int:pk>/edit/", views.InventarioUpdateView.as_view(), name="inventario_edit"),
    path("inventario/<int:pk>/delete/", views.InventarioDeleteView.as_view(), name="inventario_delete"),

    # Historial Inventario
    path("historial-inventario/", views.HistorialInventarioListView.as_view(), name="historial_inventario_list"),
    path("historial-inventario/add/", views.HistorialInventarioCreateView.as_view(), name="historial_inventario_add"),
    path("historial-inventario/<int:pk>/edit/", views.HistorialInventarioUpdateView.as_view(), name="historial_inventario_edit"),
    path("historial-inventario/<int:pk>/delete/", views.HistorialInventarioDeleteView.as_view(), name="historial_inventario_delete"),

    # Contactos
    path("contactos-centros/", views.ContactoCentroListView.as_view(), name="contacto_centro_list"),
    path("contactos-centros/add/", views.ContactoCentroCreateView.as_view(), name="contacto_centro_add"),
    path("contactos-centros/<int:pk>/edit/", views.ContactoCentroUpdateView.as_view(), name="contacto_centro_edit"),
    path("contactos-centros/<int:pk>/delete/", views.ContactoCentroDeleteView.as_view(), name="contacto_centro_delete"),

    # Proveedor
    path("proveedores/", views.ProveedorListView.as_view(), name="proveedor_list"),
    path("proveedores/add/", views.ProveedorCreateView.as_view(), name="proveedor_add"),
    path("proveedores/<int:pk>/edit/", views.ProveedorUpdateView.as_view(), name="proveedor_edit"),
    path("proveedores/<int:pk>/delete/", views.ProveedorDeleteView.as_view(), name="proveedor_delete"),

    # Favoritos Clientes
    path("favoritos-clientes/", views.FavoritoClienteListView.as_view(), name="favorito_cliente_list"),
    path("favoritos-clientes/add/", views.FavoritoClienteCreateView.as_view(), name="favorito_cliente_add"),
    path("favoritos-clientes/<int:pk>/edit/", views.FavoritoClienteUpdateView.as_view(), name="favorito_cliente_edit"),
    path("favoritos-clientes/<int:pk>/delete/", views.FavoritoClienteDeleteView.as_view(), name="favorito_cliente_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
