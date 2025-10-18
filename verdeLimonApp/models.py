from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
    )

    usuario_nombre = models.CharField(max_length=50, blank=True)
    usuario_apellido = models.CharField(max_length=50, blank=True)
    usuario_rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    usuario_email = models.EmailField(unique=True)
    usuario_rol = models.CharField(max_length=10, choices=ROLES, default='cliente')

    USERNAME_FIELD = 'usuario_email'
    REQUIRED_FIELDS = ["username", "usuario_nombre", "usuario_apellido", "usuario_rut", "usuario_rol"]

    def __str__(self):
        return self.usuario_email




class Direccion(models.Model):
    direccion_calle = models.CharField(max_length=255)
    direccion_ciudad = models.CharField(max_length=100)
    direccion_region = models.CharField(max_length=100)
    direccion_pais = models.CharField(max_length=100)
    direccion_codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.direccion_calle}, {self.direccion_ciudad}"

class CategoriaProducto(models.Model):
    categoria_nombre = models.CharField(max_length=100)
    categoria_descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.categoria_nombre

class CentroDistribucion(models.Model):
    TIPO_CHOICES = (
        ("distribuidor", "Distribuidor"),
        ("quiosco", "Quiosco"),
        ("tienda", "Tienda"),
    )
    centro_nombre = models.CharField(max_length=100)
    id_direccion = models.IntegerField(null=True, blank=True)  # antes era foreingKey(Direccion)
    centro_tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    centro_descripcion = models.TextField(blank=True, null=True, help_text="Descripción de los productos que se venden en este centro")
    centro_imagen = models.ImageField(upload_to='centros_distribucion/', blank=True, null=True)

    def __str__(self):
        return self.centro_nombre

class Producto(models.Model):
    producto_nombre = models.CharField(max_length=100)
    producto_descripcion = models.TextField(blank=True, null=True)
    id_categoria = models.IntegerField(null=True, blank=True)  # antes era foreingKey(CategoriaProducto)
    producto_precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00) # Added default value for new field, to avoid issues with existing data
    ESTADO_CHOICES = (
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    )
    producto_estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="activo")
    producto_imagen = models.ImageField(upload_to='productos/', blank=True, null=True)


    def __str__(self):
        return self.producto_nombre

class ProductoValorNutricional(models.Model):
    id_producto = models.IntegerField(null=True, blank=True)  # antes era onetoOneField(Producto)
    valor_calorias = models.IntegerField(blank=True, null=True)
    valor_proteinas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_carbohidratos = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_grasas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_fibra = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_sodio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_azucar = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


    def __str__(self):
        # ya no podemos acceder a self.id_producto.producto_nomrbre porque no hay relacion
        return f"Nutrición del producto {self.id_producto} ({self.valor_calorias or 0} kcal)"

class Inventario(models.Model):
    id_centro = models.IntegerField(null=True, blank=True)  # antes era foreingKey(CentroDistribucion)
    id_producto = models.IntegerField(null=True, blank=True)  # antes era foreingKey(Producto)
    inventario_cantidad = models.IntegerField()

    class Meta:
        # Ya no hay relaciones, pero mantenemos la restricción de unicidad de los IDs
        unique_together = ("id_centro", "id_producto")

    def __str__(self):
        # ya no podemos acceder a los nombresd de los modelos relacionados
        return f"Producto {self.id_producto} en centro {self.id_centro}"

class HistorialInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = (
        ("agregar", "Agregar"),
        ("retirar", "Retirar"),
        ("traslado", "Traslado"),
    )
    id_inventario = models.IntegerField(null=True, blank=True)  # antes era foreingKey(Inventario)
    id_usuario = models.IntegerField(null=True, blank=True)  # antes era foreingKey(Usuario)    
    historial_tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    id_centro_destino = models.IntegerField(null=True, blank=True)  # antes era foreingKey(CentroDistribucion)
    historial_cantidad = models.IntegerField()
    historial_fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # ya no puede acceder a producto.nombre ni otras relaciones
        return f"Movimiento de {self.historial_cantidad} unidades (Inventario {self.id_inventario})"



class ContactoCentro(models.Model):
    TIPO_CHOICES = (
        ("telefono", "Teléfono"),
        ("correo", "Correo"),
        ("whatsapp", "WhatsApp"),
    )
    id_centro = models.IntegerField(null=True, blank=True)  # antes era foreingKey(CentroDistribucion) 
    contacto_tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    contacto_valor = models.CharField(max_length=255)

    def __str__(self):
        # ya no podemos usar seld.id_centro.centro_nombre
        return f"{self.contacto_tipo}: {self.contacto_valor} (Centro{self.id_centro})"

class Proveedor(models.Model):
    proveedor_nombre = models.CharField(max_length=100)
    proveedor_rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    proveedor_email = models.EmailField(max_length=100, blank=True, null=True)
    proveedor_telefono = models.CharField(max_length=50, blank=True, null=True)
    id_direccion = models.IntegerField(null=True, blank=True)  # antes era foreingKey(Direccion)

    def __str__(self):
        return self.proveedor_nombre

class FavoritoCliente(models.Model):
    id_usuario = models.IntegerField(null=True, blank=True)  # antes era foreingKey(Usuario)
    id_producto = models.IntegerField(null=True, blank=True)  # antes era foreingKey(Producto)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("id_usuario", "id_producto") # sigue funcionando, pero con IDs simples

    def __str__(self):
        # ya no podemos acceder a usuario_email ni producto_nombre
        return f"favorito del usuario {self.id_usuario} - Prodcuto {self.id_producto}"

