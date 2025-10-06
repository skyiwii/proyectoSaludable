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
    id_direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    centro_tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    centro_descripcion = models.TextField(blank=True, null=True, help_text="Descripción de los productos que se venden en este centro")
    centro_imagen = models.ImageField(upload_to='centros_distribucion/', blank=True, null=True)

    def __str__(self):
        return self.centro_nombre

class Producto(models.Model):
    producto_nombre = models.CharField(max_length=100)
    producto_descripcion = models.TextField(blank=True, null=True)
    id_categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
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
    id_producto = models.OneToOneField(Producto, on_delete=models.CASCADE, primary_key=True)
    valor_calorias = models.IntegerField(blank=True, null=True)
    valor_proteinas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_carbohidratos = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_grasas = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_fibra = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_sodio = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valor_azucar = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return f"Nutrición de {self.id_producto.producto_nombre} ({self.valor_calorias} kcal)"

class Inventario(models.Model):
    id_centro = models.ForeignKey(CentroDistribucion, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    inventario_cantidad = models.IntegerField()

    class Meta:
        unique_together = ("id_centro", "id_producto")

    def __str__(self):
        return f"{self.id_producto.producto_nombre} en {self.id_centro.centro_nombre}"

class HistorialInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = (
        ("agregar", "Agregar"),
        ("retirar", "Retirar"),
        ("traslado", "Traslado"),
    )
    id_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    historial_tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    id_centro_destino = models.ForeignKey(CentroDistribucion, on_delete=models.SET_NULL, blank=True, null=True, related_name="movimientos_destino")
    historial_cantidad = models.IntegerField()
    historial_fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movimiento de {self.historial_cantidad} de {self.id_inventario.id_producto.producto_nombre}"



class ContactoCentro(models.Model):
    TIPO_CHOICES = (
        ("telefono", "Teléfono"),
        ("correo", "Correo"),
        ("whatsapp", "WhatsApp"),
    )
    id_centro = models.ForeignKey(CentroDistribucion, on_delete=models.CASCADE)
    contacto_tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    contacto_valor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.contacto_tipo}: {self.contacto_valor} ({self.id_centro.centro_nombre})"

class Proveedor(models.Model):
    proveedor_nombre = models.CharField(max_length=100)
    proveedor_rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    proveedor_email = models.EmailField(max_length=100, blank=True, null=True)
    proveedor_telefono = models.CharField(max_length=50, blank=True, null=True)
    id_direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, blank=True, null=True, related_name='proveedores')

    def __str__(self):
        return self.proveedor_nombre

class FavoritoCliente(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("id_usuario", "id_producto")

    def __str__(self):
        return f"{self.id_usuario.usuario_email} - {self.id_producto.producto_nombre}"

