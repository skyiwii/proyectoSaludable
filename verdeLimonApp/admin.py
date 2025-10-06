from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    Usuario, CategoriaProducto, Direccion, CentroDistribucion, Producto, 
    ProductoValorNutricional, Inventario, HistorialInventario, 
    ContactoCentro, Proveedor, FavoritoCliente
)


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


class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('categoria_nombre', 'categoria_descripcion')
    search_fields = ('categoria_nombre',)


class DireccionAdmin(admin.ModelAdmin):
    list_display = ('direccion_calle', 'direccion_ciudad', 'direccion_region', 'direccion_pais')
    list_filter = ('direccion_region', 'direccion_pais')
    search_fields = ('direccion_calle', 'direccion_ciudad')


class CentroDistribucionAdmin(admin.ModelAdmin):
    list_display = ('centro_nombre', 'centro_tipo', 'get_direccion', 'imagen_preview')
    list_filter = ('centro_tipo',)
    search_fields = ('centro_nombre', 'centro_descripcion')
    fields = ('centro_nombre', 'id_direccion', 'centro_tipo', 'centro_descripcion', 'centro_imagen')
    
    def get_direccion(self, obj):
        return f"{obj.id_direccion.direccion_calle}, {obj.id_direccion.direccion_ciudad}"
    get_direccion.short_description = 'Dirección'
    
    def imagen_preview(self, obj):
        if obj.centro_imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.centro_imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Imagen'


class ProductoValorNutricionalInline(admin.StackedInline):
    model = ProductoValorNutricional
    extra = 0


class ProductoAdmin(admin.ModelAdmin):
    list_display = ("producto_nombre", "id_categoria", "producto_precio", "producto_estado", "imagen_preview")
    list_filter = ('id_categoria', 'producto_estado')
    search_fields = ('producto_nombre', 'producto_descripcion')
    inlines = [ProductoValorNutricionalInline]
    
    def imagen_preview(self, obj):
        if obj.producto_imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.producto_imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Imagen'


class ProductoValorNutricionalAdmin(admin.ModelAdmin):
    list_display = (
        'id_producto', 'valor_calorias', 'valor_proteinas', 'valor_carbohidratos', 'valor_grasas'
    )
    search_fields = ('id_producto__producto_nombre',)


class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'id_centro', 'inventario_cantidad')
    list_filter = ('id_centro',)
    search_fields = ('id_producto__producto_nombre', 'id_centro__centro_nombre')


class HistorialInventarioAdmin(admin.ModelAdmin):
    list_display = ('id_inventario', 'id_usuario', 'historial_tipo_movimiento', 'historial_cantidad', 'historial_fecha')
    list_filter = ('historial_tipo_movimiento', 'historial_fecha')
    search_fields = ('id_inventario__id_producto__producto_nombre', 'id_usuario__usuario_email')
    date_hierarchy = 'historial_fecha'



class ContactoCentroAdmin(admin.ModelAdmin):
    list_display = ('id_centro', 'contacto_tipo', 'contacto_valor')
    list_filter = ('contacto_tipo',)
    search_fields = ('id_centro__centro_nombre', 'contacto_valor')


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('proveedor_nombre', 'proveedor_rut', 'proveedor_email', 'proveedor_telefono')
    search_fields = ('proveedor_nombre', 'proveedor_rut', 'proveedor_email')


class FavoritoClienteAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'id_producto', 'fecha_agregado')
    list_filter = ('fecha_agregado',)
    search_fields = ('id_usuario__usuario_email', 'id_producto__producto_nombre')
    date_hierarchy = 'fecha_agregado'


# Registrar los modelos con sus respectivos admins
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

# Personalizar el título del sitio de administración
admin.site.site_header = "Administración Verde Limón"
admin.site.site_title = "Verde Limón Admin"
admin.site.index_title = "Panel de Administración"
