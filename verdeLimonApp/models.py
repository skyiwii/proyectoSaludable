from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/")

    def __str__(self):
        return self.nombre


class Favorito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorito: {self.producto.nombre}"
