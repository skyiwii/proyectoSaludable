from django.core.management.base import BaseCommand
from verdeLimonApp.models import (
    Usuario, CategoriaProducto, Direccion, CentroDistribucion, Producto, 
    ProductoValorNutricional, Inventario, HistorialInventario, 
    ContactoCentro, Proveedor, FavoritoCliente
)
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Tests CRUD operations for all models in verdeLimonApp'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting CRUD tests...'))

        # Test CategoriaProducto
        self.stdout.write(self.style.SUCCESS('Testing CategoriaProducto CRUD...'))
        categoria = CategoriaProducto.objects.create(categoria_nombre='Frutas', categoria_descripcion='Frutas frescas y orgánicas')
        self.stdout.write(self.style.SUCCESS(f'Created CategoriaProducto: {categoria}'))
        categoria.categoria_nombre = 'Vegetales'
        categoria.save()
        self.stdout.write(self.style.SUCCESS(f'Updated CategoriaProducto: {categoria}'))
        categoria.delete()
        self.stdout.write(self.style.SUCCESS('Deleted CategoriaProducto'))

        # Test Direccion
        self.stdout.write(self.style.SUCCESS('Testing Direccion CRUD...'))
        direccion = Direccion.objects.create(
            direccion_calle='Calle Falsa 123',
            direccion_ciudad='Ciudad Ficticia',
            direccion_region='Region Imaginaria',
            direccion_pais='Pais Inventado',
            direccion_codigo_postal='12345'
        )
        self.stdout.write(self.style.SUCCESS(f'Created Direccion: {direccion}'))
        direccion.direccion_ciudad = 'Ciudad Real'
        direccion.save()
        self.stdout.write(self.style.SUCCESS(f'Updated Direccion: {direccion}'))
        direccion.delete()
        self.stdout.write(self.style.SUCCESS('Deleted Direccion'))

        # Test CentroDistribucion
        self.stdout.write(self.style.SUCCESS('Testing CentroDistribucion CRUD...'))
        direccion_centro = Direccion.objects.create(
            direccion_calle='Avenida Siempre Viva 742',
            direccion_ciudad='Springfield',
            direccion_region='Central',
            direccion_pais='USA',
            direccion_codigo_postal='98765'
        )
        centro = CentroDistribucion.objects.create(
            centro_nombre='Centro Principal',
            id_direccion=direccion_centro,
            centro_tipo='distribuidor',
            centro_descripcion='Centro de distribución principal'
        )
        self.stdout.write(self.style.SUCCESS(f'Created CentroDistribucion: {centro}'))
        centro.centro_nombre = 'Centro Secundario'
        centro.save()
        self.stdout.write(self.style.SUCCESS(f'Updated CentroDistribucion: {centro}'))
        centro.delete()
        direccion_centro.delete() # Clean up associated direction
        self.stdout.write(self.style.SUCCESS('Deleted CentroDistribucion'))

        # Test Producto
        self.stdout.write(self.style.SUCCESS('Testing Producto CRUD...'))
        categoria_prod = CategoriaProducto.objects.create(categoria_nombre='Bebidas', categoria_descripcion='Bebidas naturales')
        producto = Producto.objects.create(
            producto_nombre='Jugo de Naranja',
            producto_descripcion='Jugo 100% natural sin azúcares añadidos',
            id_categoria=categoria_prod,
            producto_precio=2.50,
            producto_estado='activo'
        )
        self.stdout.write(self.style.SUCCESS(f'Created Producto: {producto}'))
        producto.producto_precio = 3.00
        producto.save()
        self.stdout.write(self.style.SUCCESS(f'Updated Producto: {producto}'))
        producto.delete()
        categoria_prod.delete() # Clean up associated category
        self.stdout.write(self.style.SUCCESS('Deleted Producto'))

        # Test ProductoValorNutricional
        self.stdout.write(self.style.SUCCESS('Testing ProductoValorNutricional CRUD...'))
        categoria_nut = CategoriaProducto.objects.create(categoria_nombre='Snacks', categoria_descripcion='Snacks saludables')
        producto_nut = Producto.objects.create(
            producto_nombre='Barra de Cereal',
            producto_descripcion='Barra energética con frutos secos',
            id_categoria=categoria_nut,
            producto_precio=1.80,
            producto_estado='activo'
        )
        nutricional = ProductoValorNutricional.objects.create(
            id_producto=producto_nut,
            valor_calorias=150,
            valor_proteinas=5.0,
            valor_carbohidratos=20.0,
            valor_grasas=8.0,
            valor_fibra=3.0,
            valor_sodio=10,
            valor_azucar=10.0
        )
        self.stdout.write(self.style.SUCCESS(f'Created ProductoValorNutricional: {nutricional}'))
        nutricional.valor_calorias = 160
        nutricional.save()
        self.stdout.write(self.style.SUCCESS(f'Updated ProductoValorNutricional: {nutricional}'))
        nutricional.delete()
        producto_nut.delete() # Clean up associated product
        categoria_nut.delete() # Clean up associated category
        self.stdout.write(self.style.SUCCESS('Deleted ProductoValorNutricional'))

        # Test Inventario
        self.stdout.write(self.style.SUCCESS('Testing Inventario CRUD...'))
        categoria_inv = CategoriaProducto.objects.create(categoria_nombre='Lácteos', categoria_descripcion='Productos lácteos')
        producto_inv = Producto.objects.create(
            producto_nombre='Yogur Natural',
            producto_descripcion='Yogur sin azúcar',
            id_categoria=categoria_inv,
            producto_precio=1.20,
            producto_estado='activo'
        )
        direccion_inv = Direccion.objects.create(
            direccion_calle='Calle del Sol 456',
            direccion_ciudad='Pueblo Alegre',
            direccion_region='Norte',
            direccion_pais='Chile',
            direccion_codigo_postal='54321'
        )
        centro_inv = CentroDistribucion.objects.create(
            centro_nombre='Almacén Central',
            id_direccion=direccion_inv,
            centro_tipo='tienda',
            centro_descripcion='Almacén principal de productos'
        )
        inventario = Inventario.objects.create(
            id_centro=centro_inv,
            id_producto=producto_inv,
            inventario_cantidad=100
        )
        self.stdout.write(self.style.SUCCESS(f'Created Inventario: {inventario}'))
        inventario.inventario_cantidad = 90
        inventario.save()
        self.stdout.write(self.style.SUCCESS(f'Updated Inventario: {inventario}'))
        inventario.delete()
        centro_inv.delete()
        direccion_inv.delete()
        producto_inv.delete()
        categoria_inv.delete()
        self.stdout.write(self.style.SUCCESS('Deleted Inventario'))

        # Test Usuario (creation only, update/delete handled by Django auth)
        self.stdout.write(self.style.SUCCESS('Testing Usuario creation...'))
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser@example.com', # Using email as username
            email='testuser@example.com',
            password='testpassword123',
            usuario_nombre='Test',
            usuario_apellido='User',
            usuario_rut='11111111-1',
            usuario_rol='cliente'
        )
        self.stdout.write(self.style.SUCCESS(f'Created Usuario: {user}'))
        user.delete() # Clean up test user
        self.stdout.write(self.style.SUCCESS('Deleted Usuario'))

        # Test HistorialInventario (requires existing Inventario and Usuario)
        self.stdout.write(self.style.SUCCESS('Testing HistorialInventario CRUD...'))
        user_hist = User.objects.create_user(
            username='histuser@example.com',
            email='histuser@example.com',
            password='histpassword123',
            usuario_nombre='Hist',
            usuario_apellido='User',
            usuario_rut='22222222-2',
            usuario_rol='admin'
        )
        categoria_hist = CategoriaProducto.objects.create(categoria_nombre='Panadería', categoria_descripcion='Productos de panadería')
        producto_hist = Producto.objects.create(
            producto_nombre='Pan Integral',
            producto_descripcion='Pan de masa madre',
            id_categoria=categoria_hist,
            producto_precio=3.00,
            producto_estado='activo'
        )
        direccion_hist = Direccion.objects.create(
            direccion_calle='Calle de la Luna 789',
            direccion_ciudad='Villa Serena',
            direccion_region='Sur',
            direccion_pais='Chile',
            direccion_codigo_postal='67890'
        )
        centro_hist = CentroDistribucion.objects.create(
            centro_nombre='Panadería Central',
            id_direccion=direccion_hist,
            centro_tipo='tienda',
            centro_descripcion='Panadería principal'
        )
        inventario_hist = Inventario.objects.create(
            id_centro=centro_hist,
            id_producto=producto_hist,
            inventario_cantidad=50
        )
        historial = HistorialInventario.objects.create(
            id_inventario=inventario_hist,
            id_usuario=user_hist,
            historial_tipo_movimiento='agregar',
            historial_cantidad=10
        )
        self.stdout.write(self.style.SUCCESS(f'Created HistorialInventario: {historial}'))
        historial.historial_cantidad = 15
        historial.save()
        self.stdout.write(self.style.SUCCESS(f'Updated HistorialInventario: {historial}'))
        historial.delete()
        inventario_hist.delete()
        centro_hist.delete()
        direccion_hist.delete()
        producto_hist.delete()
        categoria_hist.delete()
        user_hist.delete()
        self.stdout.write(self.style.SUCCESS('Deleted HistorialInventario'))

        # Test ContactoCentro
        self.stdout.write(self.style.SUCCESS('Testing ContactoCentro CRUD...'))
        direccion_cont = Direccion.objects.create(
            direccion_calle='Plaza Mayor 1',
            direccion_ciudad='Centro',
            direccion_region='Metropolitana',
            direccion_pais='Chile',
            direccion_codigo_postal='10000'
        )
        centro_cont = CentroDistribucion.objects.create(
            centro_nombre='Oficina Central',
            id_direccion=direccion_cont,
            centro_tipo='distribuidor',
            centro_descripcion='Oficina administrativa'
        )
        contacto = ContactoCentro.objects.create(
            id_centro=centro_cont,
            contacto_tipo='telefono',
            contacto_valor='+56912345678'
        )
        self.stdout.write(self.style.SUCCESS(f'Created ContactoCentro: {contacto}'))
        contacto.contacto_valor = 'contacto@oficina.cl'
        contacto.contacto_tipo = 'correo'
        contacto.save()
        self.stdout.write(self.style.SUCCESS(f'Updated ContactoCentro: {contacto}'))
        contacto.delete()
        centro_cont.delete()
        direccion_cont.delete()
        self.stdout.write(self.style.SUCCESS('Deleted ContactoCentro'))

        # Test Proveedor
        self.stdout.write(self.style.SUCCESS('Testing Proveedor CRUD...'))
        direccion_prov = Direccion.objects.create(
            direccion_calle='Ruta 5 Norte Km 10',
            direccion_ciudad='Zona Industrial',
            direccion_region='Coquimbo',
            direccion_pais='Chile',
            direccion_codigo_postal='20000'
        )
        proveedor = Proveedor.objects.create(
            proveedor_nombre='Proveedores SA',
            proveedor_rut='99888777-6',
            proveedor_email='contacto@proveedores.cl',
            proveedor_telefono='+56223456789',
            id_direccion=direccion_prov
        )
        self.stdout.write(self.style.SUCCESS(f'Created Proveedor: {proveedor}'))
        proveedor.proveedor_nombre = 'Proveedores Ltda.'
        proveedor.save()
        self.stdout.write(self.style.SUCCESS(f'Updated Proveedor: {proveedor}'))
        proveedor.delete()
        direccion_prov.delete()
        self.stdout.write(self.style.SUCCESS('Deleted Proveedor'))

        # Test FavoritoCliente
        self.stdout.write(self.style.SUCCESS('Testing FavoritoCliente CRUD...'))
        user_fav = User.objects.create_user(
            username='favuser@example.com',
            email='favuser@example.com',
            password='favpassword123',
            usuario_nombre='Fav',
            usuario_apellido='User',
            usuario_rut='33333333-3',
            usuario_rol='cliente'
        )
        categoria_fav = CategoriaProducto.objects.create(categoria_nombre='Frutos Secos', categoria_descripcion='Mezcla de frutos secos')
        producto_fav = Producto.objects.create(
            producto_nombre='Mix Energético',
            producto_descripcion='Mix de almendras, nueces y pasas',
            id_categoria=categoria_fav,
            producto_precio=5.00,
            producto_estado='activo'
        )
        favorito = FavoritoCliente.objects.create(
            id_usuario=user_fav,
            id_producto=producto_fav
        )
        self.stdout.write(self.style.SUCCESS(f'Created FavoritoCliente: {favorito}'))
        # No direct update for FavoritoCliente, as it's a simple relationship
        favorito.delete()
        producto_fav.delete()
        categoria_fav.delete()
        user_fav.delete()
        self.stdout.write(self.style.SUCCESS('Deleted FavoritoCliente'))

        self.stdout.write(self.style.SUCCESS('All CRUD tests completed successfully!'))

