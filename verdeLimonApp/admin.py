from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    Usuario, CategoriaProducto, Direccion, CentroDistribucion, Producto, 
    ProductoValorNutricional, Inventario, HistorialInventario, 
    ContactoCentro, Proveedor, FavoritoCliente
)

# -----------------------------------
# Admin de Usuario
# -----------------------------------
class UsuarioAdmin(UserAdmin):
    list_display = (
        'usuario_email', 'usuario_nombre', 'usuario_apellido', 'usuario_rut', 'usuario_rol', 'is_staff'
    )
    list_filter = ('usuario_rol', 'is_staff', 'is_active')
    search_fields = ('usuario_email', 'usuario_nombre', 'usuario_apellido', 'usuario_rut')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {'fields': ('usuario_nombre', 'usuario_apellido', 'usuario_rut', 'usuario_rol')}), 
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personal', {'fields': ('usuario_nombre', 'usuario_apellido', 'usuario_rut', 'usuario_rol')}), 
    )

# -----------------------------------
# Admin de CategoriaProducto
# -----------------------------------
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('categoria_nombre', 'categoria_descripcion')
    search_fields = ('categoria_nombre',)

# -----------------------------------
# Admin de Direccion
# -----------------------------------
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('direccion_calle', 'direccion_ciudad', 'direccion_region', 'direccion_pais')
    list_filter = ('direccion_region', 'direccion_pais')
    search_fields = ('direccion_calle', 'direccion_ciudad')

# -----------------------------------
# Admin de CentroDistribucion
# -----------------------------------
class CentroDistribucionAdmin(admin.ModelAdmin):
    list_display = ('centro_nombre', 'centro_tipo', 'get_direccion', 'imagen_preview')
    list_filter = ('centro_tipo',)
    search_fields = ('centro_nombre', 'centro_descripcion')
    fields = ('centro_nombre', 'centro_tipo', 'centro_descripcion', 'centro_imagen')  # CAMBIO: eliminado id_direccion

    def get_direccion(self, obj):
        # CAMBIO: usamos los campos simples que reemplazan la relación
        return f"{getattr(obj, 'direccion_calle', 'N/A')}, {getattr(obj, 'direccion_ciudad', 'N/A')}"
    get_direccion.short_description = "Dirección"

    def imagen_preview(self, obj):
        if obj.centro_imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.centro_imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Imagen'

# -----------------------------------
# Admin de Producto
# -----------------------------------
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("producto_nombre", "producto_precio", "producto_estado", "imagen_preview")
    list_filter = ('producto_estado',)
    search_fields = ('producto_nombre', 'producto_descripcion')

    def imagen_preview(self, obj):
        if obj.producto_imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.producto_imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Imagen'

# -----------------------------------
# Admin de ProductoValorNutricional
# -----------------------------------
class ProductoValorNutricionalAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'valor_calorias', 'valor_proteinas', 'valor_carbohidratos', 'valor_grasas', 'valor_fibra', 'valor_sodio', 'valor_azucar')
    search_fields = ('id_producto',)  # CAMBIO: antes era __producto_nombre, ahora solo el ID

# -----------------------------------
# Admin de Inventario
# -----------------------------------
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'id_centro', 'inventario_cantidad')  # CAMBIO: usamos IDs simples
    list_filter = ('id_centro',)
    search_fields = ('id_producto', 'id_centro')

# -----------------------------------
# Admin de HistorialInventario
# -----------------------------------
class HistorialInventarioAdmin(admin.ModelAdmin):
    list_display = ('id_inventario', 'id_usuario', 'historial_tipo_movimiento', 'historial_cantidad', 'historial_fecha')
    list_filter = ('historial_tipo_movimiento', 'historial_fecha')
    search_fields = ('id_inventario', 'id_usuario')
    date_hierarchy = 'historial_fecha'

# -----------------------------------
# Admin de ContactoCentro
# -----------------------------------
class ContactoCentroAdmin(admin.ModelAdmin):
    list_display = ('id_centro', 'contacto_tipo', 'contacto_valor')
    list_filter = ('contacto_tipo',)
    search_fields = ('id_centro', 'contacto_valor')

# -----------------------------------
# Admin de Proveedor
# -----------------------------------
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('proveedor_nombre', 'proveedor_rut', 'proveedor_email', 'proveedor_telefono', 'id_direccion')  # CAMBIO: id_direccion como campo simple
    search_fields = ('proveedor_nombre', 'proveedor_rut', 'proveedor_email')

# -----------------------------------
# Admin de FavoritoCliente
# -----------------------------------
class FavoritoClienteAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'id_producto', 'fecha_agregado')  # CAMBIO: usamos IDs simples
    list_filter = ('fecha_agregado',)
    search_fields = ('id_usuario', 'id_producto')
    date_hierarchy = 'fecha_agregado'

# -----------------------------------
# Registrar todos los modelos
# -----------------------------------
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(CategoriaProducto, CategoriaProductoAdmin)
admin.site.register(Direccion, DireccionAdmin)
admin.site.register(CentroDistribucion, CentroDistribucionAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ProductoValorNutricional, ProductoValorNutricionalAdmin)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(HistorialInventario, HistorialInventarioAdmin)
admin.site.register(ContactoCentro, ContactoCentroAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(FavoritoCliente, FavoritoClienteAdmin)

# -----------------------------------
# Personalización del admin
# -----------------------------------
admin.site.site_header = "Administración Verde Limón"
admin.site.site_title = "Verde Limón Admin"
admin.site.index_title = "Panel de Administración"
